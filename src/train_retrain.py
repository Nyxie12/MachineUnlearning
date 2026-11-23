import hashlib
import json
import sys
from pathlib import Path
from time import perf_counter

import torch
from torch import nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

# 1. Locate the project and public model code.
project_root = Path(__file__).resolve().parents[1]
model_folder = project_root / "third_party" / "pytorch-cifar" / "models"
sys.path.insert(0, str(model_folder))
from resnet import ResNet18

# 2. Load our saved training and validation selections.
split_file = project_root / "data" / "splits" / "dog20_seed42.json"
split = json.loads(split_file.read_text())
training_indices = split["retain_indices"]
validation_indices = split["validation_indices"]

assert len(training_indices) == 44_100
assert set(training_indices).isdisjoint(split["forget_indices"])
assert len(validation_indices) == 5_000
assert set(training_indices).isdisjoint(validation_indices)

# 3. Set the random seed and select the GPU.
seed = split["seed"]
torch.manual_seed(seed)
generator = torch.Generator().manual_seed(seed)
device = torch.device("mps")

# 4. Prepare images using the public repository's settings.
mean = (0.4914, 0.4822, 0.4465)
std = (0.2023, 0.1994, 0.2010)

training_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean, std),
])

validation_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean, std),
])

training_data = datasets.CIFAR10(
    root=project_root / "data",
    train=True,
    download=False,
    transform=training_transform,
)

validation_data = datasets.CIFAR10(
    root=project_root / "data",
    train=True,
    download=False,
    transform=validation_transform,
)

training_loader = DataLoader(
    Subset(training_data, training_indices),
    batch_size=128,
    shuffle=True,
    generator=generator,
    num_workers=0,
)

validation_loader = DataLoader(
    Subset(validation_data, validation_indices),
    batch_size=256,
    shuffle=False,
    num_workers=0,
)

# 5. Create a fresh model and configure learning.
model = ResNet18().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.1,
    momentum=0.9,
    weight_decay=0.0005,
)

# 6. Configure the full baseline run.
epochs = 50
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=epochs
)

run_folder = project_root / "results" / "retrain_seed42"
run_folder.mkdir(parents=True, exist_ok=False)

config = {
    "model": "Public CIFAR ResNet-18",
    "model_commit": (
        project_root / "notes" / "model_commit.txt"
    ).read_text().strip(),
    "model_source_sha256": hashlib.sha256(
        (model_folder / "resnet.py").read_bytes()
    ).hexdigest(),
    "split_sha256": hashlib.sha256(
        split_file.read_bytes()
    ).hexdigest(),
    "seed": seed,
    "epochs": epochs,
    "device": str(device),
    "pytorch_version": str(torch.__version__),
    "training_images": len(training_indices),
    "validation_images": len(validation_indices),
    "optimizer": "SGD",
    "initial_learning_rate": 0.1,
    "momentum": 0.9,
    "weight_decay": 0.0005,
    "training_batch_size": 128,
    "scheduler": "CosineAnnealingLR",
    "checkpoint_selection": "Highest overall validation accuracy",
}

(run_folder / "config.json").write_text(
    json.dumps(config, indent=2) + "\n"
)

history = []
best_accuracy = -1.0
best_epoch = 0
class_count = len(training_data.classes)

# 7. Train and validate once per epoch.
for epoch in range(1, epochs + 1):
    print(f"Starting epoch {epoch}/{epochs}", flush=True)
    learning_rate = optimizer.param_groups[0]["lr"]

    model.train()
    loss_total = torch.zeros((), device=device)
    training_seen = 0

    torch.mps.synchronize()
    start = perf_counter()

    for images, labels in training_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad(set_to_none=True)
        loss = criterion(model(images), labels)
        loss.backward()
        optimizer.step()

        loss_total += loss.detach() * labels.size(0)
        training_seen += labels.size(0)

    torch.mps.synchronize()
    training_seconds = perf_counter() - start
    training_loss = loss_total.item() / training_seen

    assert training_seen == len(training_indices)
    assert torch.isfinite(torch.tensor(training_loss)).item()

    model.eval()
    class_correct = torch.zeros(class_count, dtype=torch.long)
    class_total = torch.zeros(class_count, dtype=torch.long)

    torch.mps.synchronize()
    start = perf_counter()

    with torch.inference_mode():
        for images, labels in validation_loader:
            predictions = model(images.to(device)).argmax(dim=1).cpu()

            class_total += torch.bincount(
                labels, minlength=class_count
            )
            class_correct += torch.bincount(
                labels[predictions == labels],
                minlength=class_count,
            )

    torch.mps.synchronize()
    validation_seconds = perf_counter() - start

    assert class_total.sum().item() == len(validation_indices)
    assert (class_total == 500).all().item()

    validation_accuracy = (
        class_correct.sum().item() / class_total.sum().item()
    )
    class_accuracy = {
        category: (
            class_correct[label].item() / class_total[label].item()
        )
        for label, category in enumerate(training_data.classes)
    }

    scheduler.step()

    record = {
        "epoch": epoch,
        "learning_rate": learning_rate,
        "training_loss": training_loss,
        "validation_accuracy": validation_accuracy,
        "validation_class_accuracy": class_accuracy,
        "training_seconds": training_seconds,
        "validation_seconds": validation_seconds,
    }
    history.append(record)

    temporary_history = run_folder / "history.tmp"
    temporary_history.write_text(
        json.dumps(history, indent=2) + "\n"
    )
    temporary_history.replace(run_folder / "history.json")

    if validation_accuracy > best_accuracy:
        temporary_checkpoint = run_folder / "best_checkpoint.tmp"

        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "validation_accuracy": validation_accuracy,
            "config": config,
        }, temporary_checkpoint)

        temporary_checkpoint.replace(
            run_folder / "best_checkpoint.pt"
        )
        best_accuracy = validation_accuracy
        best_epoch = epoch

    print(
        f"Epoch {epoch}/{epochs} | loss {training_loss:.4f} | "
        f"validation {validation_accuracy:.2%} | "
        f"dog {class_accuracy['dog']:.2%} | "
        f"train {training_seconds:.1f}s | "
        f"validation {validation_seconds:.1f}s",
        flush=True,
    )

print(
    f"Best validation accuracy: {best_accuracy:.2%}, "
    f"epoch {best_epoch}"
)
print("Saved model:", run_folder / "best_checkpoint.pt")

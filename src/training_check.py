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
training_indices = split["training_indices"]
validation_indices = split["validation_indices"]

assert len(training_indices) == 45_000
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

# 6. Train for one epoch.
print(f"Training one epoch: {len(training_indices):,} images.", flush=True)
model.train()
loss_total = torch.zeros((), device=device)
training_seen = 0

torch.mps.synchronize()
start = perf_counter()

for batch_number, (images, labels) in enumerate(training_loader, start=1):
    images = images.to(device)
    labels = labels.to(device)

    optimizer.zero_grad(set_to_none=True)
    outputs = model(images)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()

    loss_total += loss.detach() * labels.size(0)
    training_seen += labels.size(0)

    if batch_number % 50 == 0:
        print(f"Batch {batch_number}/{len(training_loader)}", flush=True)

torch.mps.synchronize()
training_seconds = perf_counter() - start
training_loss = loss_total.item() / training_seen

assert training_seen == len(training_indices)
assert torch.isfinite(torch.tensor(training_loss)).item()

# 7. Evaluate on validation images.
print("Evaluating validation images...", flush=True)
model.eval()
correct = torch.zeros((), dtype=torch.long, device=device)
validation_seen = 0

torch.mps.synchronize()
start = perf_counter()

with torch.inference_mode():
    for images, labels in validation_loader:
        images = images.to(device)
        labels = labels.to(device)

        predictions = model(images).argmax(dim=1)
        correct += (predictions == labels).sum()
        validation_seen += labels.size(0)

torch.mps.synchronize()
validation_seconds = perf_counter() - start

assert validation_seen == len(validation_indices)
validation_accuracy = correct.item() / validation_seen

# 8. Save the measurements.
results = {
    "purpose": "One-epoch training and timing check",
    "model": "Public CIFAR ResNet-18",
    "seed": seed,
    "device": str(device),
    "epochs": 1,
    "training_images": training_seen,
    "validation_images": validation_seen,
    "training_loss": training_loss,
    "validation_accuracy": validation_accuracy,
    "training_seconds": training_seconds,
    "validation_seconds": validation_seconds,
}

output_folder = project_root / "results"
output_folder.mkdir(exist_ok=True)
output_file = output_folder / "training_check.json"
output_file.write_text(json.dumps(results, indent=2) + "\n")

print(f"Training loss: {training_loss:.4f}")
print(f"Validation accuracy: {validation_accuracy:.2%}")
print(f"Training time: {training_seconds:.1f} seconds")
print(f"Validation time: {validation_seconds:.1f} seconds")
print("Results saved to:", output_file)
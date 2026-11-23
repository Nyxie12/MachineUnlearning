import hashlib
import json
import sys
from pathlib import Path

import torch
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

project_root = Path(__file__).resolve().parents[1]
model_folder = project_root / "third_party" / "pytorch-cifar" / "models"
sys.path.insert(0, str(model_folder))
from resnet import ResNet18

run_folder = project_root / "results" / "retrain_seed42"
checkpoint_file = run_folder / "best_checkpoint.pt"
split_file = project_root / "data" / "splits" / "dog20_seed42.json"

split = json.loads(split_file.read_text())
checkpoint = torch.load(
    checkpoint_file,
    map_location="cpu",
    weights_only=True,
)

config = checkpoint["config"]

# 2. Confirm we are evaluating the same experiment.
assert hashlib.sha256(split_file.read_bytes()).hexdigest() == (
    config["split_sha256"]
)
assert hashlib.sha256(
    (model_folder / "resnet.py").read_bytes()
).hexdigest() == config["model_source_sha256"]
assert str(torch.__version__) == config["pytorch_version"]
assert torch.backends.mps.is_available()

training_indices = set(split["training_indices"])
retain_indices = set(split["retain_indices"])
forget_indices = set(split["forget_indices"])
validation_indices = set(split["validation_indices"])

assert len(retain_indices) == 44_100
assert len(forget_indices) == 900
assert len(validation_indices) == 5_000
assert retain_indices.isdisjoint(forget_indices)
assert retain_indices | forget_indices == training_indices
assert training_indices.isdisjoint(validation_indices)

# 3. Prepare unchanged images for evaluation.
evaluation_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        (0.4914, 0.4822, 0.4465),
        (0.2023, 0.1994, 0.2010),
    ),
])

training_data = datasets.CIFAR10(
    root=project_root / "data",
    train=True,
    download=False,
    transform=evaluation_transform,
)
test_data = datasets.CIFAR10(
    root=project_root / "data",
    train=False,
    download=False,
    transform=evaluation_transform,
)

classes = training_data.classes
dog_label = classes.index("dog")
assert all(
    training_data.targets[index] == dog_label
    for index in forget_indices
)
assert len(test_data) == 10_000

# 4. Restore the trained model.
device = torch.device("mps")
model = ResNet18()
model.load_state_dict(checkpoint["model_state_dict"])
model = model.to(device)
model.eval()


# 5. Measure accuracy overall and for each class.
def evaluate(dataset):
    loader = DataLoader(
        dataset,
        batch_size=256,
        shuffle=False,
        num_workers=0,
    )
    correct = torch.zeros(len(classes), dtype=torch.long)
    total = torch.zeros(len(classes), dtype=torch.long)

    with torch.inference_mode():
        for images, labels in loader:
            predictions = model(images.to(device)).argmax(dim=1).cpu()

            total += torch.bincount(labels, minlength=len(classes))
            correct += torch.bincount(
                labels[predictions == labels],
                minlength=len(classes),
            )

    assert total.sum().item() == len(dataset)

    per_class = {}
    for label, category in enumerate(classes):
        count = total[label].item()
        hits = correct[label].item()
        per_class[category] = {
            "images": count,
            "correct": hits,
            "accuracy": hits / count if count else None,
        }

    return {
        "images": total.sum().item(),
        "correct": correct.sum().item(),
        "accuracy": correct.sum().item() / total.sum().item(),
        "per_class": per_class,
    }


# 6. Evaluate each group separately.
evaluation_sets = {
    "validation": Subset(training_data, split["validation_indices"]),
    "retain": Subset(training_data, split["retain_indices"]),
    "forget": Subset(training_data, split["forget_indices"]),
    "test": test_data,
}

results = {}
for name, dataset in evaluation_sets.items():
    print(f"Evaluating {name}: {len(dataset):,} images...", flush=True)
    result = evaluate(dataset)
    results[name] = result

    print(
        f"  Overall: {result['accuracy']:.2%} | "
        f"Dog: {result['per_class']['dog']['accuracy']:.2%}",
        flush=True,
    )

# Verify that loading the checkpoint reproduces its validation score.
assert abs(
    results["validation"]["accuracy"] - checkpoint["validation_accuracy"]
) < 1e-6

print("\nTest accuracy by class:")
for category, values in results["test"]["per_class"].items():
    print(f"  {category:<12} {values['accuracy']:.2%}")

# 7. Save the baseline measurements.
report = {
    "model": config["model"],
    "checkpoint_epoch": checkpoint["epoch"],
    "checkpoint_sha256": hashlib.sha256(
        checkpoint_file.read_bytes()
    ).hexdigest(),
    "split_sha256": config["split_sha256"],
    "pytorch_version": str(torch.__version__),
    "device": str(device),
    "method": "full_retrain",
    "training_images": config["training_images"],
    "results": results,
}

output_file = run_folder / "retrain_evaluation.json"
output_file.write_text(json.dumps(report, indent=2) + "\n")
print("\nResults saved to:", output_file)



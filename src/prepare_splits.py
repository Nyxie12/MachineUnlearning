import json
import random
from pathlib import Path

from torchvision.datasets import CIFAR10

project_root = Path(__file__).resolve().parents[1]
dataset = CIFAR10(
    root=project_root / "data",
    train=True,
    download=False,
)

seed = 42
rng = random.Random(seed)

training_indices = []
validation_indices = []

# Reserve 500 images per category for validation.
for label in range(len(dataset.classes)):
    indices = [
        index
        for index, target in enumerate(dataset.targets)
        if target == label
    ]
    rng.shuffle(indices)
    validation_indices.extend(indices[:500])
    training_indices.extend(indices[500:])

# Simulate a deletion request for 20% of the dog training images.
dog_label = dataset.class_to_idx["dog"]
dog_indices = [
    index
    for index in training_indices
    if dataset.targets[index] == dog_label
]
rng.shuffle(dog_indices)

forget_indices = dog_indices[:900]
forget_set = set(forget_indices)
retain_indices = [
    index for index in training_indices if index not in forget_set
]

assert len(training_indices) == 45_000
assert len(validation_indices) == 5_000
assert len(forget_indices) == 900
assert len(retain_indices) == 44_100
assert set(training_indices).isdisjoint(validation_indices)
assert set(retain_indices).isdisjoint(forget_indices)
assert set(retain_indices) | forget_set == set(training_indices)
assert all(dataset.targets[index] == dog_label for index in forget_indices)

manifest = {
    "dataset": "CIFAR-10",
    "scenario": "Deletion request for correctly labeled dog images",
    "seed": seed,
    "index_source": "Official CIFAR-10 training split",
    "training_indices": sorted(training_indices),
    "validation_indices": sorted(validation_indices),
    "forget_indices": sorted(forget_indices),
    "retain_indices": sorted(retain_indices),
}

output_folder = project_root / "data" / "splits"
output_folder.mkdir(parents=True, exist_ok=True)
output_file = output_folder / "dog20_seed42.json"

if output_file.exists():
    if json.loads(output_file.read_text()) != manifest:
        raise RuntimeError("Existing split file contains different selections.")
else:
    output_file.write_text(json.dumps(manifest, indent=2) + "\n")

print("Original training images:", len(training_indices))
print("Validation images:", len(validation_indices))
print("Requested deletions:", len(forget_indices))
print("Retained training images:", len(retain_indices))
print("Dog training images before removal:", len(dog_indices))
print("Dog training images after removal:", len(dog_indices) - len(forget_indices))
print("Split checks passed.")
print("Saved to:", output_file)

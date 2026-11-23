import csv
from collections import Counter
from pathlib import Path

from torchvision.datasets import CIFAR10

project_root = Path(__file__).resolve().parents[1]
data_folder = project_root / "data"

train_data = CIFAR10(root=data_folder, train=True, download=True)
test_data = CIFAR10(root=data_folder, train=False, download=True)

train_counts = Counter(train_data.targets)
test_counts = Counter(test_data.targets)

print(f"{'Category':<14}{'Training':>10}{'Test':>10}")

rows = []
for label, category in enumerate(train_data.classes):
    training = train_counts[label]
    testing = test_counts[label]

    print(f"{category:<14}{training:>10,}{testing:>10,}")
    rows.append([category, training, testing])

print(f"{'TOTA':<14}{len(train_data):>10,}{len(test_data):>10,}")

output_file = project_root / "notes" / "dataset_counts.csv"
with output_file.open("w", newline="") as file:
    writer=csv.writer(file)
    writer.writerow(["category", "training_images", "test_images"])
    writer.writerows(rows)

print("\nCounts saved to:", output_file)
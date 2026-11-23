import sys
from pathlib import Path

import torch

project_root = Path(__file__).resolve().parents[1]
model_folder = project_root / "third_party" / "pytorch-cifar" / "models"
sys.path.insert(0, str(model_folder))

from resnet import ResNet18

device = torch.device("mps")
model = ResNet18().to(device)
model.eval()

sample = torch.randn(1, 3, 32, 32, device=device)

with torch.inference_mode():
    output = model(sample)

assert output.shape == (1,10)
assert torch.isfinite(output).all().item()

print("Model: public CIFAR ResNet-18")
print("Device:", device)
print("Input shape:", tuple(sample.shape))
print("Output shape:", tuple(output.shape))
print("Parameters:", f"{sum(p.numel() for p in model.parameters()):,}")
print("Model check passed")

    
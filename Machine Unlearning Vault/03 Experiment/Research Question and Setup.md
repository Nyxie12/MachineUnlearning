---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Research Question and Setup

## Research question
Can public machine-unlearning methods remove the influence of 900 selected dog training images while preserving useful classification and costing less than full retraining?

## Model and hardware
- Public CIFAR ResNet-18, trained from random initialization.
- Architecture source: [kuangliu/pytorch-cifar](https://github.com/kuangliu/pytorch-cifar).
- Local Apple M3 Max using MPS.
- Python 3.12.3; project PyTorch 2.15.0 and TorchVision 0.29.2 as reported during setup.
- Seed 42 for the completed original and full-retrain pair.

## Training settings
50 epochs; batch size 128; SGD with initial learning rate 0.1, momentum 0.9, weight decay 0.0005; cosine learning-rate schedule. Random crop and horizontal flip during training, deterministic normalization for evaluation. Checkpoint selected by highest overall validation accuracy.

The validation and test groups remain fixed. Do not tune methods based on test outcomes. Seed repetition and unlearning implementations are pending.

See [[Dataset and Deletion Request]], [[Reproducibility and Timing]], and the copied configuration files in [[Sources and Evidence]].

---
[[00 Start Here|Vault home]]

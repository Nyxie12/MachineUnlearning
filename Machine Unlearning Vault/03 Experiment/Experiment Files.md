---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Experiment Files

Project root: `/Users/keithjohn/Documents/MachineUnlearning`.

| Location | Role |
|---|---|
| `src/` | User-run training, evaluation, and preparation scripts |
| `data/` | CIFAR-10 and saved selections |
| `third_party/pytorch-cifar/` | Public model architecture code |
| `results/baseline_seed42/` | Completed original model, history, configuration, evaluation |
| `results/retrain_seed42/` | Completed full retrain, history, configuration, evaluation |
| `notes/` | Setup notes and source commit records |
| `Machine Unlearning Vault/` | This Obsidian research vault |
| `report/` | Future report artifacts |

## Important scripts
`prepare_splits.py`, `training_check.py`, `train_baseline.py`, `evaluate_baseline.py`, `train_retrain.py`, and `evaluate_retrain.py`.

## Selection file
`data/splits/dog20_seed42.json` defines the original training, validation, deletion, and retained indices. It remains outside the vault; large arrays and model weights are not duplicated here.

## Saved checkpoints
Both completed runs use `best_checkpoint.pt` in their respective result folders. Original checkpoint: epoch 50; full-retrain checkpoint: epoch 44. Their evaluation JSON files contain checkpoint hashes.

Metadata snapshots are linked in [[Sources and Evidence]]. This vault adds documentation; it does not replace scripts, datasets, or authoritative results.

---
[[00 Start Here|Vault home]]

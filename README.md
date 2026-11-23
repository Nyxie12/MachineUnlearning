# KSU Machine Unlearning Research

A guided CIFAR-10 experiment asking whether selected training images' influence can be removed while preserving useful accuracy and saving compute compared with full retraining.

## Current status

- Original CIFAR ResNet-18: training and evaluation complete.
- Fresh retained-data retrain: training and evaluation complete.
- SSD authors' source downloaded and pinned; integration and experiments pending.
- SCRUB and SISA: implementation and experiments pending.

This repository contains the restarted ResNet-18 experiment. It does not claim completed SISA, SCRUB, or SSD benchmark results.

## Experiment

| Item | Setting |
|---|---|
| Dataset | CIFAR-10 |
| Architecture | Public CIFAR ResNet-18, trained from random initialization |
| Original training / validation / test images | 45,000 / 5,000 / 10,000 |
| Deletion request | 900 correctly labeled dog training images |
| Removal fraction | 20% of training dogs; 2% of original training images |
| Retained training images | 44,100 |
| Completed run seed | 42 |
| Training budget | 50 epochs per original/retrain run |
| Hardware | Apple M3 Max, MPS |

## Verified single-run results

| Measurement | Original | Full retrain |
|---|---:|---:|
| Overall test accuracy | 93.31% | 93.24% |
| Dog test accuracy | 90.10% | 86.80% |
| Deletion-image accuracy | 99.67% | 85.56% |

Correct classification of deletion images is not a failure-to-forget percentage: a model can recognize dogs using other examples. These single-run results do not establish statistical consistency or a privacy guarantee.

## Organization

- `src/`: dataset preparation, training, and evaluation scripts.
- `data/splits/`: exact saved image selections; downloaded image data is excluded.
- `results/`: small completed-run configuration, history, and evaluation files; weights are excluded.
- `notes/`: setup notes and pinned source commits.
- `Machine Unlearning Vault/`: linked Obsidian notes, roadmap, sources, and evidence snapshots. Open this folder as a vault and start at `00 Start Here.md`.
- `third_party/`: pinned Git submodules for public source code.
- `report/`: future report outputs.

## Setup

The current scripts require Apple's MPS backend; running them on CPU/CUDA requires an explicitly documented adaptation. Install Python 3.12 and uv, then clone with submodules:

```bash
git clone --recurse-submodules https://github.com/Nyxie12/MachineUnlearning.git
cd MachineUnlearning
uv sync --locked
```

For an existing clone:

```bash
git submodule update --init --recursive
```

The recorded environment uses Python 3.12.3, PyTorch 2.15.0, and TorchVision 0.29.2. The lockfile records dependency versions.

## Reproducing the completed reference runs

Review each script before running. `inspect_dataset.py` downloads CIFAR-10; `prepare_splits.py` regenerates the seed-42 selections. The selections already committed here define the reported experiment.

```bash
uv run python src/check_model.py
uv run python src/inspect_dataset.py
uv run python src/training_check.py
uv run python src/train_baseline.py
uv run python src/evaluate_baseline.py
uv run python src/train_retrain.py
uv run python src/evaluate_retrain.py
```

The training scripts intentionally refuse to overwrite an existing run folder. This repository includes completed result metadata in those folders, so reproduce in a copy with new output-folder names (updating the corresponding evaluator), or archive the existing metadata folders before training. Evaluators require locally generated checkpoints and verify source/split/software consistency.

## Public sources

- CIFAR-10: https://www.cs.toronto.edu/~kriz/cifar.html
- Model architecture: https://github.com/kuangliu/pytorch-cifar
- SSD: https://github.com/if-loops/selective-synaptic-dampening
- Planned SCRUB: https://github.com/meghdadk/SCRUB
- Planned SISA: https://github.com/cleverhans-lab/machine-unlearning

The authors' SSD experiment runners need adaptation for our checkpoint format, image selections, and MPS environment. We will record all adaptations before reporting method results. Third-party code retains its upstream license; see each submodule's LICENSE.

## What stays local

Downloaded datasets, installed environments, large model checkpoints, Obsidian workspace layouts, and archived incomplete runs are excluded from normal Git tracking. They are not backed up by this repository. Small result files, exact split indices, source versions, and the research vault are included.

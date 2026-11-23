---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Reproducibility and Timing

## Record for every run
Model source commit and hash, split hash, checkpoint hash, software versions, seed, optimizer/settings, checkpoint-selection rule, hardware, and all method-specific adaptations. The completed runs store several of these in config and evaluation JSON files.

## Fair training comparison
The original and full retrain use the same architecture, settings, and 50-epoch budget. Fewer retained images mean fewer updates per epoch. A fixed seed does not guarantee identical behavior across environments.

## Timing rules
- Report initial model training separately from deletion work.
- For SSD, include importance estimation or report it separately plus a total.
- For SCRUB, record all update phases and selected iteration budgets.
- For SISA, record initial shard training, storage/checkpoints, and replay work.
- Keep evaluation time separate from model-update time.
- Synchronize MPS before and after GPU timing so pending GPU work is included.
- Sum of training/validation fields excludes file saving and other setup; do not label it full end-to-end time.

## Observed slowdown
Before a Mac restart, baseline epochs took several minutes. After restart, the one-epoch checks returned to approximately 28 seconds in both tested Python environments. This establishes an observed recovery, not a verified root cause. The full-retrain timing differs from baseline; system conditions have not been controlled enough to explain that difference.

See [[Verified Results]] for recorded durations and [[Sources and Evidence]] for the actual logs.

---
[[00 Start Here|Vault home]]

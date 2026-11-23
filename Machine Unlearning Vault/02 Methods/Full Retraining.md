---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Full Retraining

**Blurb:** Train a fresh model using only retained images.

## Process
1. Start with randomly initialized weights.
2. Exclude the 900 requested dog images.
3. Train on the remaining 44,100 images.
4. Select the best checkpoint using overall validation accuracy.
5. Evaluate on the same groups used for the original model.

## Why include it?
It directly implements our training procedure without the requested images. It provides a behavioral reference and a cost reference for faster updates.

## Tradeoffs
It can be practical for a small experiment, but costly for large models or repeated deletion requests. Equal epoch budgets here mean slightly fewer optimization steps for the retained-data model because it has fewer images.

## Our status
Training and evaluation are complete. Best checkpoint: epoch 44 of 50. Test accuracy: **93.24%**; dog test accuracy: **86.80%**. See [[Verified Results]].

This was a fresh model, not continued training of the original checkpoint. See [[Reproducibility and Timing]].

---
[[00 Start Here|Vault home]]

---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Evaluation Plan

## Current evaluation
Use the same saved image selections, normalization, and category labels for every candidate. Evaluate saved checkpoints without updating weights. Keep random training augmentation out of evaluation.

Report validation, retain, forget, and test accuracy, plus per-class accuracy and image counts. Validation checks should reproduce the selected checkpoint's stored score.

## Planned forgetting diagnostics
| Diagnostic | Question | Limit |
|---|---|---|
| Forget-set accuracy | Does it classify deletion images correctly? | Not a removal score |
| Prediction agreement with retrain | Does it choose the same categories? | Agreement can hide probability differences |
| Probability divergence, such as JS | How different are prediction distributions? | Behavioral similarity is not a privacy proof |
| Membership-inference evaluation | Can a defined attack distinguish training members? | Depends on attack design, calibration, and controls |

Because deletion images are all dogs, membership controls should be class-matched. Do not let class imbalance masquerade as a membership signal. Define attack splits and validation-based settings before evaluating; do not use test outcomes to tune the unlearning method.

## Interpretation
Use multiple diagnostics alongside retained/test utility and compute cost. Compare multiple seeds where feasible; a single fresh retrain is only one realization of a stochastic process. For SISA, use its own matched reference in addition to the single-model comparison.

Current observations: [[Verified Results]]. Cost accounting: [[Reproducibility and Timing]].

---
[[00 Start Here|Vault home]]

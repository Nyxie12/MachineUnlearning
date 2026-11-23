---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Verified Results

Verified from the current saved evaluation reports on November 22, 2026. This is the restarted, ResNet-18 experiment, not the discarded earlier benchmark.

## Original versus full retrain
| Measurement | Original | Full retrain | Retrain minus original |
|---|---:|---:|---:|
| Validation overall | 94.38% | 94.26% | -0.12 pp |
| Retain overall | 99.95% | 99.90% | -0.05 pp |
| Forget overall | 99.67% | 85.56% | -14.11 pp |
| Test overall | 93.31% | 93.24% | -0.07 pp |
| Dog test | 90.10% | 86.80% | -3.30 pp |

`pp` means percentage points. Overall test accuracy dropped by 0.07 points; dog test accuracy dropped by 3.30 points. Neither observation establishes a statistically reliable effect with only one run per model.

## Checkpoint selection
Original: best overall validation checkpoint at epoch 50. Full retrain: best overall validation checkpoint at epoch 44. Both training histories contain all 50 epochs.

## Recorded duration totals
| Run | Epochs | Training seconds | Validation seconds |
|---|---:|---:|---:|
| Original | 50 | 1520.6 | 54.6 |
| Full retrain | 50 | 2021.1 | 76.0 |

These are sums of stored timing fields, not end-to-end runtime. No controlled speedup conclusion follows from these two runs alone. See [[Reproducibility and Timing]].

## Key interpretation
The retrained model correctly classified 770 of 900 deletion images (85.56%) without ever training on them. That illustrates generalization; the accuracy is not a percentage of forgetting.

See [[Class Results]], [[Accuracy and Forgetting]], and the raw snapshots in [[Sources and Evidence]]. SISA, SCRUB, and SSD results are still pending.

---
[[00 Start Here|Vault home]]

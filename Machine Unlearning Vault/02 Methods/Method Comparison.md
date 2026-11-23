---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Method Comparison

| Approach | Starting point | Deletion action | Main comparison concern |
|---|---|---|---|
| Original | Fresh single model | None | Pre-deletion reference |
| Full retrain | Fresh single model | Train using retained data only | Complete cost and single-run variability |
| SISA | Separately trained shard ensemble | Replay affected portions | Own matching sharded retrain and setup/storage costs |
| SCRUB | Original trained model | Teacher-student optimization | Settings and utility/forgetting balance |
| SSD | Original trained model | Importance-based parameter dampening | Preparation cost and actual parameter changes |

## What is complete?
Only the original and full-retrain rows have measurements in the restarted project. Do not import earlier discarded benchmark numbers into this experiment.

Details: [[Full Retraining]] · [[SISA]] · [[SCRUB]] · [[SSD]]. Results: [[Verified Results]]. Sources: [[Sources and Evidence]].

---
[[00 Start Here|Vault home]]

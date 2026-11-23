---
tags: [machine-unlearning]
updated: 2026-11-22
---

# SCRUB

**Blurb:** Adjust a model to move away from the original on deletion images while preserving retained knowledge.

## How it works
The original trained model acts as a teacher. An updated copy acts as a student. Optimization pushes the student away from teacher predictions on deletion examples and toward useful behavior on retained examples. The method balances these competing objectives.

## Tradeoffs
It uses additional optimization and settings that can trade off utility and forgetting. Divergence from the teacher on deletion images alone does not prove privacy. We must specify whether we use standard SCRUB or a variant such as the paper's rewinding procedure.

## Our planned use
Start from our original ResNet-18 checkpoint. Use the fixed retain/forget split, select settings with validation data, and compare against [[Full Retraining]].

## Status
Planned. The authors' public repository has been identified; it has not yet been integrated or run in this restarted experiment.

Source: [authors' SCRUB repository](https://github.com/meghdadk/SCRUB), [Towards Unbounded Machine Unlearning](https://arxiv.org/abs/2302.09880). See [[Evaluation Plan]].

---
[[00 Start Here|Vault home]]

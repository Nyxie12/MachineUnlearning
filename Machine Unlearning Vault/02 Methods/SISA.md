---
tags: [machine-unlearning]
updated: 2026-11-22
---

# SISA

**Blurb:** Organize training into groups; retrain affected portions after deletion.

SISA means **Sharded, Isolated, Sliced, and Aggregated**. Separate models learn from separate shards. Training is divided into slices, with checkpoints that allow replay from before an affected slice. Predictions from shard models are aggregated.

## Deletion process
Identify affected shards and slices, restore suitable earlier checkpoints, then replay affected training without the deleted examples. Unaffected shards can be reused.

## Tradeoffs
This structure can reduce deletion work, but introduces multiple models, checkpoint storage, and an accuracy/setup tradeoff. If deleted examples are spread across many shards, much of the ensemble may need updating.

> [!important] Fair reference
> Compare SISA with a fresh retrain of the **same sharded setup**, as well as reporting comparison to the single-model baseline. Matching an ensemble reference does not mean matching the single-model ResNet-18.

## Status
Planned. No SISA training, deletion results, shard count, or slice count has been established for this restarted experiment. Equivalence claims require documenting the training/replay procedure and its assumptions.

Source: [authors' SISA code](https://github.com/cleverhans-lab/machine-unlearning), [Machine Unlearning paper](https://arxiv.org/abs/1912.03817). See [[Method Comparison]] and [[Chronological Roadmap]].

---
[[00 Start Here|Vault home]]

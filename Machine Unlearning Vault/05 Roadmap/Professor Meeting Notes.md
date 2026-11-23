---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Professor Meeting Notes

## Short explanation of the project
We trained a public ResNet-18 on CIFAR-10, selected 900 dog training images for deletion, and built a fresh retained-data model as our reference. We will compare public SISA, SCRUB, and SSD methods for utility, deletion behavior, and cost.

## Questions to be ready for
**Where did the model come from?** Public CIFAR ResNet-18 code from kuangliu/pytorch-cifar. We trained the weights ourselves.

**Why dogs?** A targeted, reproducible deletion request lets us examine one category and check effects on the others.

**Does 85.56% on deletion images mean failure?** No. The reference never trained on those examples and can recognize dogs from other examples.

**Have the public unlearning methods been run?** Not in this restarted experiment. Their repositories are identified; integration and runs are next.

**What is completed?** Original training/evaluation and retained-data full retraining/evaluation.

**What limits the current conclusion?** One architecture, one dataset, one removal scenario, one seed per model, and no completed dedicated forgetting/privacy diagnostics.

**How will SISA be compared fairly?** Against its matching sharded retrain as well as the single-model reference, with setup/storage costs documented.

## Questions to settle before the final benchmark
- How many repeated seeds are practical?
- Which forgetting diagnostics should be required rather than optional?
- How much implementation adaptation is acceptable while staying faithful to public methods?

Sources and evidence: [[Sources and Evidence]]. Current values: [[Verified Results]].

---
[[00 Start Here|Vault home]]

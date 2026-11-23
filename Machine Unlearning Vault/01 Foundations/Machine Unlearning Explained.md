---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Machine Unlearning Explained

Machine unlearning aims to remove or reduce selected training examples' influence on a trained model. Ideally, it preserves useful performance and costs less than full retraining.

Deleting a source image only changes stored data. It does not automatically change model weights. Unlearning changes the trained model or rebuilds the relevant training process.

## Why request deletion?
A person might withdraw permission, data may have been included incorrectly, or a deletion obligation may apply. Our project uses a simulated deletion request for correctly labeled images; it is not a legal-compliance demonstration.

## What is the reference?
A fresh model trained without the requested examples is the practical reference. A meaningful comparison asks how close behavior is to that reference and what the process costs.

## Exact and approximate approaches
- Exact unlearning seeks equivalence to the specified training procedure without the deleted examples, often understood in terms of the distribution of possible trained models.
- Approximate methods seek sufficiently similar behavior or reduced influence under stated criteria. High accuracy alone does not establish that criterion.
- A single retrained model is an empirical reference, not a complete characterization of training randomness.

See [[Full Retraining]], [[Accuracy and Forgetting]], and the primary method papers in [[Sources and Evidence]].

---
[[00 Start Here|Vault home]]

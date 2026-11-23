---
tags: [machine-unlearning]
updated: 2026-11-22
---

# SSD

**Blurb:** Weaken selected weights especially important to deletion images.

SSD means **Selective Synaptic Dampening**. It estimates parameter importance on deletion examples and compares that with importance on the original training data. Selected parameters receive a dampening update.

## Tradeoffs
SSD avoids a conventional retraining loop for the update, but calculating importance still requires computation. Its selection and dampening settings matter. Parameters associated with deletion examples may also support retained knowledge.

## Our planned use
Start from the original checkpoint. Document the importance calculation, update settings, preparation time, update time, and the number of parameters changed.

> [!warning] Useful diagnostic
> If settings change zero weights, record that outcome. It is not evidence of successful forgetting merely because accuracy is preserved.

## Status
Planned. The authors' public repository has been identified; it has not yet been integrated or run in this restarted experiment.

Source: [authors' SSD repository](https://github.com/if-loops/selective-synaptic-dampening), [SSD paper](https://arxiv.org/abs/2308.07707). See [[Reproducibility and Timing]].

---
[[00 Start Here|Vault home]]

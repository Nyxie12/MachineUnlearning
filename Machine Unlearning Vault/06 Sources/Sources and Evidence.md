---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Sources and Evidence

## Primary online sources
Checked November 22, 2026. Repository links identify sources, not proof that their code has already been run locally.

- [Official CIFAR-10 description](https://www.cs.toronto.edu/~kriz/cifar.html): dataset structure and categories.
- [Public CIFAR ResNet code](https://github.com/kuangliu/pytorch-cifar): architecture used for our completed training runs. Exact local source commit: [[model_commit.txt]].
- [SISA repository](https://github.com/cleverhans-lab/machine-unlearning) and [Machine Unlearning paper](https://arxiv.org/abs/1912.03817).
- [SCRUB repository](https://github.com/meghdadk/SCRUB) and [Towards Unbounded Machine Unlearning](https://arxiv.org/abs/2302.09880).
- [SSD repository](https://github.com/if-loops/selective-synaptic-dampening) and [SSD paper](https://arxiv.org/abs/2308.07707).

## Evidence snapshots
Copied from the current project when this vault was created; future experiments will not automatically update these copies.

### Original model
[[baseline_evaluation.json]] · [[baseline_config.json]] · [[baseline_history.json]]

### Full retrain
[[retrain_evaluation.json]] · [[retrain_config.json]] · [[retrain_history.json]]

### Dataset and source
[[dataset_counts.csv]] · [[model_commit.txt]] · [[artifact_manifest.json]]

The manifest records original project-relative locations and SHA-256 hashes for copied evidence. Large images, datasets, index arrays, environments, and checkpoint weights are intentionally left in the project.

## Evidence boundaries
Current numerical claims come from the JSON files above. Earlier discarded experiment measurements are excluded. Concept explanations summarize the primary sources and research discussion; planned diagnostics and proposed execution order are explicitly labeled as plans.

See [[Experiment Files]] to locate authoritative project artifacts.

---
[[00 Start Here|Vault home]]

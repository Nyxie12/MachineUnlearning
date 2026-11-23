---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Chronological Roadmap

## Completed
- [x] Create the project folders and isolated Python environment.
- [x] Install PyTorch/TorchVision and confirm MPS works.
- [x] Obtain public CIFAR ResNet-18 and record the source commit.
- [x] Download CIFAR-10 and inspect per-class counts.
- [x] Save fixed training, validation, retain, and forget selections.
- [x] Run a one-epoch training/timing check.
- [x] Train the original model for 50 epochs.
- [x] Evaluate the original model on all four groups.
- [x] Train a fresh retained-data model for 50 epochs.
- [x] Evaluate the full-retrain reference on the same groups.
- [x] Organize current knowledge and results into this vault.

## Next: method implementation
- [ ] Review the authors' public implementations and licenses; record exact commits.
- [ ] Write down the evaluation/tuning rules before method experiments.
- [ ] Integrate SSD; record importance calculation, settings, parameter changes, and cost.
- [ ] Integrate SCRUB; document its objective, phases, settings, and any variant.
- [ ] Build the SISA shard/slice setup and its fresh matching retrain.
- [ ] Apply each method to the same deletion request and compare diagnostic results.

SSD then SCRUB then SISA is a practical proposed order, not a professor-imposed requirement. Any local adaptations must be clearly distinguished from authors' original code.

## Finish the study
- [ ] Repeat across agreed seeds and report variability.
- [ ] Compare accuracy, target-class effects, forgetting diagnostics, and costs.
- [ ] Create charts/tables and record limitations.
- [ ] Assemble and verify the final PDF.

See [[Professor Meeting Notes]], [[Method Comparison]], and [[Research Log]].

---
[[00 Start Here|Vault home]]

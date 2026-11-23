---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Learning Vocabulary

| Term | Plain-English meaning |
|---|---|
| Dataset | Labeled examples used for learning or evaluation |
| CIFAR-10 | Our dataset of small pictures in ten categories |
| Architecture | The structure of a model; ours is a public CIFAR ResNet-18 |
| Weights | Values adjusted during training |
| Training | Using examples to update weights |
| Batch | A group of examples processed together |
| Epoch | One pass through the training set |
| Optimizer | The rule for updating weights; ours is SGD |
| Learning rate | How large updates are allowed to be |
| Checkpoint | A saved model state |
| Validation set | Data used for selecting checkpoints and settings |
| Test set | Separate data used for reporting performance |
| Forget set | Original training examples requested for deletion |
| Retain set | Original training examples that remain allowed |
| Seed | A starting value for random-number generation |
| MPS | PyTorch's backend for Apple GPU computation |

## Model versus dataset
CIFAR-10 supplies images and category labels. The public repository supplies ResNet-18 code. We trained its weights from scratch; our trained model did not come bundled with CIFAR-10.

Our model has **11,173,962 parameters**. A fixed seed helps comparison but is not a promise of identical results across software versions or hardware.

See [[Research Question and Setup]] and [[Dataset and Deletion Request]].

---
[[00 Start Here|Vault home]]

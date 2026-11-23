---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Dataset and Deletion Request

CIFAR-10 contains ten categories: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, and truck. Images are 32 by 32 color pixels. [Official dataset description](https://www.cs.toronto.edu/~kriz/cifar.html).

## Our fixed selections
| Group | Total images | Dog images | Purpose |
|---|---:|---:|---|
| Original training | 45,000 | 4,500 | Train original model |
| Validation | 5,000 | 500 | Select checkpoints/settings |
| Retain | 44,100 | 3,600 | Training data still allowed |
| Forget | 900 | 900 | Selected training examples to remove |
| Official test | 10,000 | 1,000 | Shared performance evaluation |

The official 50,000-image training split was divided into 45,000 training and 5,000 validation examples, preserving equal class counts. Our forget set is contained inside the original training set. Retain and forget are disjoint, and together reproduce the original training selection.

## Why this request?
A simulated deletion request gives a clear reason to remove particular, correctly labeled images. We are not removing the entire dog category or introducing labeling errors. The 900 images are selected randomly **within the dog training group** with a fixed seed. Targeting dogs makes this a class-targeted request; it is not a claim that these exact images represent a real person's records.

The removal rate is 20% of training dogs and 2% of all training examples. The unchanged test set lets us examine both the targeted category and unrelated categories.

See [[Experiment Files]] for the authoritative selection file and [[Accuracy and Forgetting]] for interpreting deletion-image predictions.

---
[[00 Start Here|Vault home]]

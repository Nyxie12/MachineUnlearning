---
tags: [machine-unlearning]
updated: 2026-11-22
---

# Accuracy and Forgetting

## Accuracy
Accuracy is the fraction of pictures assigned the correct category. It measures classification usefulness.

## Forgetting
The question is whether selected training examples' influence has been removed, with a model trained without those examples as a reference.

> [!important] A deleted picture can still be recognizable
> Our fresh retrained model correctly classified 770 of the 900 deletion images, or **85.56%**, despite never training on them. It learned to recognize dogs from other pictures.

Making the model misclassify an image does not prove removal. Correct recognition does not prove that removal failed. Training-set accuracy also does not, on its own, prove memorization.

## Forget accuracy versus forget agreement
- **Forget accuracy:** correct category predictions on the deletion images.
- **Forget agreement:** how often a candidate model predicts the same category as the retrained reference on deletion images.

Neither is a percentage of data successfully erased. Even 100% agreement can hide differences in prediction probabilities, internal information, or privacy leakage.

See [[Evaluation Plan]] for probability comparisons and membership-inference diagnostics, and [[Verified Results]] for current measurements.

---
[[00 Start Here|Vault home]]

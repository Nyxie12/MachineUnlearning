# Experiment plan

## Research question

Can public unlearning methods remove the influence of 900 dog
training images while preserving classification performance,
at a lower cost than full retraining?

## Model

- Architecture: public CIFAR ResNet-18
- Repository: https://github.com/kuangliu/pytorch-cifar
- Commit: 49b7aa97b0c12fe0d4054e670403a16b6b834ddd
- Initialization: randomly initialized weights
- Device: Apple MPS

## Dataset

- Dataset: CIFAR-10
- Original training set: 45,000 images
- Validation set: 5,000 images
- Official test set: 10,000 images
- Forget set: 900 correctly labeled dog training images
- Retain set: 44,100 images
- Split file: data/splits/dog20_seed42.json
- Random seed: 42

## Initial training settings

- Optimizer: SGD
- Initial learning rate: 0.1
- Momentum: 0.9
- Weight decay: 0.0005
- Batch size: 128
- First run: one epoch to check training and measure speed
- Full training duration: to be chosen after the timing check

## Evaluation

- Use validation data to monitor training and select settings.
- Use the fixed test set for final evaluation.
- Report overall accuracy and accuracy for every category.
- Track changes in dog recognition and other categories.
- Compare unlearning with fresh remove-and-retrain references.
- Record runtime and method-specific preparation costs.
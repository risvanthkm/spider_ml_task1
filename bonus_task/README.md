# Bonus Task: Autoencoder Experimentation
--- 

## Overview
---

This bonus task explores the design and training of autoencoders in PyTorch with **MLP** architectures for both encoder and decoder,  and while we understand how **latent space dimensions** and **network depth** influence reconstruction quality on the FashionMNIST dataset.


### Impact of Latent Dimension Size
---


| Model | Latent Dim | Test Loss |
|-------|-----------|-----------|
| SpiderAutoEncoder256 | 256 | **0.0030** |
| SpiderAutoEncoder | 128 | 0.0055 |
| SpiderAutoEncoder32Shallow | 32 | 0.0088 |
| SpiderAutoEncoder32 | 32 | 0.0110 |

**Observation**: Larger latent dimensions preserve more information and produce better reconstructions. The model with 256-dimensional latent space achieved the lowest MSE loss (0.0030), while the 32-dimensional models suffered from information bottlenecks and produced poorer reconstructed images.

### Impact of Architecture Depth

---

**Shallow vs. Deep (Both with Latent Dim = 32)**:
- **Shallow Architecture**: Test Loss = 0.0088
- **Deep Architecture**: Test Loss = 0.0110

**Observation**: The shallow architecture outperformed the deeper architecture. This suggests:
- Gradient updates are more efficient in shallow networks
- Slower convergence in deeper architectures, requiring more epochs or higher learning rates
- Faster training convergence in the shallow model

## Training Configuration

---

- **Dataset**: FashionMNIST (60,000 training samples, 10,000 test samples)
- **Batch Size**: 100
- **Optimizer**: AdamW (lr=1e-3)
- **Loss Function**: Mean Squared Error (MSE)
- **Epochs**: 100

## Conclusions

---

1. **Larger Latent Spaces produce Better Reconstruction**: Increasing latent dimensionality improved reconstruction performance but reduces compression efficiency, indicating a trade-off between reconstruction quality and compression.

2. **Architecture Matters for Compression**: In our case, when using small latent dimensions, shallow architectures converge faster and achieve better performance than deep architectures. 

3. **Loss of features**: Smaller latent dimensions force aggressive compression, resulting in loss of information (blured reconstructions, missing feature characteristics).



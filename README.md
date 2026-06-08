# Spider ML Task 1

## Overview

This repository consists of three major sections:

- **base_task/** — Base ML task containing notebooks, CSV submissions, and trained models
- **bonus_task/** — Autoencoder implementation and reconstruction analysis
- **applied_ml_domain/chatbot_code/** — Full-stack RAG chatbot with backend and frontend implementation




## Repository Structure

```text
spider_ml_task1/
│
├── README.md                              # Repository overview
│
├── applied_ml_domain/                     # Applied ML Task (Research RAG System)
│   └── chatbot_code/
│       ├── README.md                      # RAG documentation
│       ├── ingestion_pipeline.py          # Ingestion pipeline
│       ├── backend/                       # FastAPI backend
│       └── frontend/                      # User interface
│
├── base_task/                             # Neural Network Task
│   ├── README.md
│   ├── base_task.ipynb
│   ├── CSV_files/                         # Dataset / outputs
│   └── saved_models/                      # Trained models
│
└── bonus_task/                            # Autoencoder Experiments
    ├── README.md
    ├── bonus_task.ipynb
    └── results/                           # Experiment outputs
```

## Base Task 
>This task focuses training a neural network with given architecture. The model is trained on FashionMNIST dataset , achieving an test accuracy of 86.13%. Task
includes visualization of validation accuracy, loss vs epochs.

[Base Task Documentation](./base_task/README.md)

## Bonus Task 
> Implemented an autoencoder with encoder and decoder based on MLP (Multi Layer Perceptron) architecture. This task also involves experimenting on various latent space dimensions and architectures.
This task depicts the influence of latent space and architecture on recontructed image.
Sample reconstructions of autoencoders are stored in the `results/` directory.

[Bonus Task Documentation](./bonus_task/README.md)

## Applied ML Task

> Built a Multimodel RAG system with a strong ingestion and retrieval pipeline. This system uses hybrid search to efficiently retrieve chunks when query has keywords in it. Also it implements an reranker to pick top 3 chunks from ~20 chunks retrieved from hybrid search.
The RAG system is capable of extracting images and tables.
>The frontend is built with `HTML` `CSS` `JS` and the backend with `python`.

[RAG System Code](./applied_ml_domain/chatbot_code/README.md)

## Thank You



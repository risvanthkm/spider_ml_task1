 # Base Task
 ---
 ## Overview
 
This base task implements an image classification pipeline for the FashionMNIST dataset using PyTorch.

The project trains a given Neural network architecture  to classify grayscale clothing images into 10 categories.

---
## Model Architecture
```mermaid
%%{
init: {
'theme':'base',
'themeVariables':{
'lineColor':'#FFFFFF',
'primaryBorderColor':'#FFFFFF',
'primaryTextColor':'#000000'
}
}
}%%

flowchart TD
    A["**INPUT LAYER**
    In: (None, 28, 28)
    Out: (None, 28, 28)"]

    B["**FLATTEN**
    In: (None, 28, 28)
    Out: (None, 784)"]

    C["**HIDDEN LAYER**
    In: (None, 784)
    Out: (None, 16)"]

    D["**HIDDEN LAYER**
    In: (None, 16)
    Out: (None, 8)"]

    E["**HIDDEN LAYER**
    In: (None, 16)
    Out: (None, 12)"]

    F["**HIDDEN LAYER**
    In: (None, 8)
    Out: (None, 8)"]

    G["**HIDDEN LAYER**
    In: (None, 12)
    Out: (None, 8)"]

    H["**SKIP CONNECTION ADD**
    In: (None, 8), (None, 8)
    Out: (None, 8)"]

    I["**CONCATENATE**
    In: (None, 8), (None, 8)
    Out: (None, 16)"]

    J["**OUTPUT LAYER**
    In: (None, 16)
    Out: (None, 10)"]

    A --> B --> C
    C --> D
    C --> E
    D --> F
    D -. skip .-> H
    F --> H
    E --> G
    H --> I
    G --> I
    I --> J
    
linkStyle default stroke:#FFFFFF,stroke-width:2px
```
---
## Hyperparameters

```text
Batch Size: 64

Optimizer: AdamW

Learning Rate: 1e-3

Loss Function: CrossEntropyLoss
```
---
## Files

| File | Description |
|------|-------------|
| `base_task.ipynb` | Training notebook — model definition, training loop, evaluation |
| `saved_models/best_model.pkl` | Best checkpoint, saved at lowest validation loss |
| `saved_models/model.pkl` | Saved at last validation loss |
| `CSV_files/submissions.csv` | Test set predictions with truth labels |
| `CSV_files/sub.xlsx` | Test images alongside their predicted classes |
---
## Results

| Model | Validation Accuracy | Test Accuracy |
|-------|-------------------|---------------|
| Best checkpoint (`best_model.pkl`) | 87.05% | 86.13%|
| Final epoch (`model.pkl`) | 86.6% | 86.09% |
---

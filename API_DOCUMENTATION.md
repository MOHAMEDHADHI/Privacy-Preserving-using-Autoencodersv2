# Cloud-Based Classifier Training API

## Overview
This API enables cloud-based training of classifiers on privacy-preserving latent vectors using both MLP and CNN architectures.

## Endpoints

### 1. Upload Latent Vectors and Train Classifiers

**POST** `/upload_latent`

Upload latent vectors and automatically train both MLP and CNN classifiers.

**Parameters:**
- `file` (file, required): .npy file containing latent vectors with labels
  - Format: numpy array with shape `(n_samples, latent_dim + 1)`
  - Last column must be integer labels
- `sigma` (float, optional): Privacy parameter sigma value (default: 1.0)

**Response:**
```json
{
  "status": "success",
  "dataset_id": 1,
  "mlp_results": {
    "accuracy": 0.95,
    "precision": 0.94,
    "recall": 0.95,
    "f1_score": 0.94,
    "sigma": 1.5,
    "model_type": "MLP"
  },
  "cnn_results": {
    "accuracy": 0.92,
    "precision": 0.91,
    "recall": 0.92,
    "f1_score": 0.91,
    "sigma": 1.5,
    "model_type": "CNN"
  },
  "comparison": {
    "mlp_accuracy": 0.95,
    "cnn_accuracy": 0.92,
    "better_model": "MLP"
  }
}
```

**Example Usage:**
```python
import requests
import numpy as np

# Prepare data
latent_vectors = np.random.randn(100, 64)  # 100 samples, 64-dim latent
labels = np.random.randint(0, 3, (100, 1))  # 3 classes
data = np.concatenate([latent_vectors, labels], axis=1)
np.save("latent_data.npy", data)

# Upload and train
with open("latent_data.npy", "rb") as f:
    files = {"file": f}
    params = {"sigma": 1.5}
    response = requests.post(
        "http://localhost:8000/upload_latent",
        files=files,
        data=params
    )
    
print(response.json())
```

### 2. Get Results for Specific Dataset

**GET** `/results/{dataset_id}`

Retrieve all training results for a specific dataset.

**Response:**
```json
{
  "dataset_id": 1,
  "results": [
    {
      "id": 1,
      "model_type": "MLP",
      "accuracy": 0.95,
      "precision": 0.94,
      "recall": 0.95,
      "f1_score": 0.94,
      "sigma": 1.5,
      "created_at": "2026-02-26T10:30:00"
    },
    {
      "id": 2,
      "model_type": "CNN",
      "accuracy": 0.92,
      "precision": 0.91,
      "recall": 0.92,
      "f1_score": 0.91,
      "sigma": 1.5,
      "created_at": "2026-02-26T10:30:05"
    }
  ]
}
```

### 3. Get All Results

**GET** `/results`

Retrieve all training results across all datasets.

**Response:**
```json
{
  "total_results": 4,
  "results": [
    {
      "id": 4,
      "dataset_id": 2,
      "model_type": "CNN",
      "accuracy": 0.88,
      "precision": 0.87,
      "recall": 0.88,
      "f1_score": 0.87,
      "sigma": 2.0,
      "created_at": "2026-02-26T11:00:00"
    }
  ]
}
```

## Model Architectures

### MLP Classifier
- Input: Latent vectors (1D)
- Architecture:
  - FC Layer: latent_dim → 128
  - ReLU + Dropout(0.3)
  - FC Layer: 128 → 64
  - ReLU + Dropout(0.3)
  - FC Layer: 64 → num_classes
- Training: 20 epochs, Adam optimizer, lr=0.001

### CNN Classifier
- Input: Reshaped latent vectors (2D grid)
- Architecture:
  - Conv2D: 1 → 32 channels, 3x3 kernel
  - MaxPool2D: 2x2
  - Conv2D: 32 → 64 channels, 3x3 kernel
  - MaxPool2D: 2x2
  - FC Layer: flattened → 128
  - Dropout(0.3)
  - FC Layer: 128 → num_classes
- Training: 20 epochs, Adam optimizer, lr=0.001

## Database Schema

### latent_vectors
- `id`: Primary key
- `dataset_id`: Foreign key to datasets
- `vector_data`: JSON serialized latent vectors
- `labels`: JSON serialized labels
- `sigma`: Privacy parameter
- `created_at`: Timestamp

### model_results
- `id`: Primary key
- `dataset_id`: Foreign key to datasets
- `model_type`: "MLP" or "CNN"
- `accuracy`: Float
- `precision`: Float
- `recall`: Float
- `f1_score`: Float
- `sigma`: Privacy parameter
- `result_data`: JSON with additional metrics
- `created_at`: Timestamp

## Setup Instructions

1. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Create database tables:
```bash
python backend/create_tables.py
```

3. Start the server:
```bash
python backend/main.py
```

4. Test the endpoint:
```bash
python backend/test_upload_latent.py
```

## Performance Metrics

All models report:
- **Accuracy**: Overall classification accuracy
- **Precision**: Weighted average precision across classes
- **Recall**: Weighted average recall across classes
- **F1 Score**: Weighted average F1 score across classes

Metrics are computed on a 20% held-out test set with stratified sampling.

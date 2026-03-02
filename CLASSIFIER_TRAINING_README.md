# Cloud-Based Classifier Training System

## Overview

This system enables privacy-preserving machine learning by training classifiers on latent representations in the cloud. It supports two architectures (MLP and CNN) and automatically compares their performance.

## Architecture

### System Flow
```
Local Environment                    Cloud Environment
─────────────────                    ─────────────────

1. Load Dataset
   ↓
2. Train Encoder
   (with privacy)
   ↓
3. Generate Latent
   Vectors (.npy)
   ↓
4. Upload ──────────────────────→  5. Store in PostgreSQL
                                      ↓
                                   6. Train MLP Classifier
                                      ↓
                                   7. Train CNN Classifier
                                      ↓
                                   8. Store Results
                                      ↓
9. Retrieve Results ←──────────────  10. Return Comparison
```

## Features

### 1. Dual Classifier Training
- **MLP**: 3-layer fully connected network for 1D latent vectors
- **CNN**: 2D convolutional network with automatic reshaping
- **Automatic Comparison**: Side-by-side performance metrics

### 2. Comprehensive Metrics
- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1 Score (weighted)

### 3. Privacy Tracking
- Sigma value stored with each result
- Enables privacy-utility tradeoff analysis
- Timestamp tracking for all experiments

### 4. Database Storage
- Latent vectors stored securely
- Training results persisted
- Query results by dataset or globally

## Quick Start

### Prerequisites
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Ensure PostgreSQL is running
# Default connection: postgresql://postgres:4305mh@localhost:5432/privacy_ml
```

### Setup
```bash
# 1. Create database tables
python backend/setup_database.py

# 2. Start the server
python backend/main.py
```

### Test
```bash
# Run automated test
python backend/test_upload_latent.py
```

## API Usage

### Upload and Train
```python
import requests
import numpy as np

# Prepare latent vectors with labels
latent_vectors = np.random.randn(100, 64)  # 100 samples, 64-dim
labels = np.random.randint(0, 3, (100, 1))  # 3 classes
data = np.concatenate([latent_vectors, labels], axis=1)

# Save to file
np.save("latent_data.npy", data)

# Upload
with open("latent_data.npy", "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload_latent",
        files={"file": f},
        data={"sigma": 1.5}
    )

result = response.json()
print(f"MLP Accuracy: {result['mlp_results']['accuracy']:.4f}")
print(f"CNN Accuracy: {result['cnn_results']['accuracy']:.4f}")
print(f"Better Model: {result['comparison']['better_model']}")
```

### Retrieve Results
```python
# Get results for specific dataset
response = requests.get("http://localhost:8000/results/1")
print(response.json())

# Get all results
response = requests.get("http://localhost:8000/results")
print(response.json())
```

## Model Details

### MLP Classifier
```
Input: (batch_size, latent_dim)
├─ Linear(latent_dim → 128)
├─ ReLU + Dropout(0.3)
├─ Linear(128 → 64)
├─ ReLU + Dropout(0.3)
└─ Linear(64 → num_classes)

Training:
- Optimizer: Adam (lr=0.001)
- Loss: CrossEntropyLoss
- Epochs: 20
- Batch Size: 32
```

### CNN Classifier
```
Input: (batch_size, 1, grid_size, grid_size)
├─ Conv2D(1 → 32, 3x3) + ReLU
├─ MaxPool2D(2x2)
├─ Conv2D(32 → 64, 3x3) + ReLU
├─ MaxPool2D(2x2)
├─ Flatten
├─ Linear(flattened → 128) + ReLU + Dropout(0.3)
└─ Linear(128 → num_classes)

Training:
- Same as MLP
- Automatic 1D → 2D reshaping
- Padding to square grid
```

## Database Schema

### latent_vectors
```sql
CREATE TABLE latent_vectors (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER REFERENCES datasets(id),
    vector_data TEXT,  -- JSON serialized
    labels TEXT,       -- JSON serialized
    sigma FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### model_results
```sql
CREATE TABLE model_results (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER REFERENCES datasets(id),
    model_type VARCHAR(50),  -- 'MLP' or 'CNN'
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    sigma FLOAT,
    result_data TEXT,  -- JSON with full metrics
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Example Output

```json
{
  "status": "success",
  "dataset_id": 1,
  "mlp_results": {
    "accuracy": 0.9500,
    "precision": 0.9423,
    "recall": 0.9500,
    "f1_score": 0.9445,
    "sigma": 1.5,
    "model_type": "MLP"
  },
  "cnn_results": {
    "accuracy": 0.9200,
    "precision": 0.9156,
    "recall": 0.9200,
    "f1_score": 0.9167,
    "sigma": 1.5,
    "model_type": "CNN"
  },
  "comparison": {
    "mlp_accuracy": 0.9500,
    "cnn_accuracy": 0.9200,
    "better_model": "MLP"
  }
}
```

## Performance Considerations

### MLP Advantages
- Faster training (fewer parameters)
- Better for high-dimensional latent spaces
- Direct processing of 1D vectors

### CNN Advantages
- Captures spatial patterns in reshaped data
- Better for structured latent representations
- Robust to local variations

## Troubleshooting

### Connection Error
```
Error: could not connect to server
```
**Solution**: Ensure PostgreSQL is running and credentials in `backend/database.py` are correct.

### Import Error
```
ModuleNotFoundError: No module named 'torch'
```
**Solution**: Install dependencies: `pip install -r backend/requirements.txt`

### Shape Error
```
Invalid data shape. Expected 2D array.
```
**Solution**: Ensure .npy file has shape (n_samples, latent_dim + 1) with labels in last column.

## Next Steps

1. **Frontend Integration**: Add UI for uploading latent vectors and viewing results
2. **Batch Processing**: Support multiple sigma values in one upload
3. **Model Persistence**: Save trained models for inference
4. **Privacy Attacks**: Implement membership inference attacks
5. **Visualization**: Add charts comparing MLP vs CNN across different sigma values

## Files Created

- `backend/main.py` - API endpoints
- `backend/classifiers.py` - MLP and CNN implementations
- `backend/models.py` - Database models
- `backend/setup_database.py` - Database setup script
- `backend/test_upload_latent.py` - Test script
- `API_DOCUMENTATION.md` - Complete API reference
- `QUICKSTART_CLASSIFIER.md` - Quick start guide
- `CLASSIFIER_TRAINING_README.md` - This file

## Support

For issues or questions:
1. Check `API_DOCUMENTATION.md` for detailed API specs
2. Run `python backend/test_upload_latent.py` to verify setup
3. Check database connection with `python backend/setup_database.py`

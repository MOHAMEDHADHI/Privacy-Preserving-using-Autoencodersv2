# Quick Start: Cloud-Based Classifier Training

## What's Implemented

✅ **POST /upload_latent** - Upload latent vectors and train classifiers
✅ **MLP Classifier** - 3-layer neural network for 1D latent vectors
✅ **CNN Classifier** - 2D convolutional network for reshaped latent vectors
✅ **PostgreSQL Storage** - Vectors and results stored in database
✅ **Automatic Comparison** - MLP vs CNN performance metrics
✅ **Results API** - Query training results by dataset or all results

## Quick Test

### Step 1: Start the Server
```bash
cd backend
python main.py
```

### Step 2: Run Test Script
```bash
python backend/test_upload_latent.py
```

This will:
1. Generate 100 sample latent vectors (64-dim, 3 classes)
2. Upload to `/upload_latent` with sigma=1.5
3. Train both MLP and CNN classifiers
4. Display comparison results

### Step 3: View Results
```bash
curl http://localhost:8000/results
```

## Manual Test with cURL

```bash
# Create test data
python -c "import numpy as np; data = np.concatenate([np.random.randn(50, 32), np.random.randint(0, 2, (50, 1))], axis=1); np.save('test.npy', data)"

# Upload and train
curl -X POST "http://localhost:8000/upload_latent?sigma=1.0" \
  -F "file=@test.npy"
```

## Expected Output

```json
{
  "status": "success",
  "dataset_id": 1,
  "mlp_results": {
    "accuracy": 0.95,
    "precision": 0.94,
    "recall": 0.95,
    "f1_score": 0.94
  },
  "cnn_results": {
    "accuracy": 0.92,
    "precision": 0.91,
    "recall": 0.92,
    "f1_score": 0.91
  },
  "comparison": {
    "better_model": "MLP"
  }
}
```

## Database Tables Created

- `latent_vectors` - Stores uploaded latent vectors
- `model_results` - Stores training metrics (accuracy, precision, recall, F1)
- Includes sigma value and timestamp for each result

## Next Steps

- Integrate with frontend for visual comparison
- Add more classifier architectures
- Implement privacy attack testing
- Add batch processing for multiple sigma values

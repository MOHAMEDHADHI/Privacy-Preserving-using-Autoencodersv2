# Quick Reference Card

## 🚀 Getting Started (4 Commands)

```bash
# 1. Setup database
python backend/setup_database.py

# 2. Migrate database (if upgrading)
python backend/migrate_database.py

# 3. Start server
python backend/main.py

# 4. Test system
python backend/test_upload_latent.py
```

## 📡 API Endpoints

### Upload Latent Vectors
```bash
POST /upload_latent
Content-Type: multipart/form-data

Parameters:
- file: .npy file (required)
- sigma: float (optional, default: 1.0)

Response: JSON with MLP & CNN results
```

### Get Results
```bash
# Specific dataset
GET /results/{dataset_id}

# All results
GET /results
```

## 💻 Code Examples

### Python Upload
```python
import requests
import numpy as np

# Prepare data
data = np.concatenate([vectors, labels], axis=1)
np.save("data.npy", data)

# Upload
with open("data.npy", "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload_latent",
        files={"file": f},
        data={"sigma": 1.5}
    )

print(response.json())
```

### cURL Upload
```bash
curl -X POST "http://localhost:8000/upload_latent?sigma=1.5" \
  -F "file=@latent_vectors.npy"
```

## 📊 Response Format

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

## 🗄️ Database Tables

### latent_vectors
- vector_data (JSON)
- labels (JSON)
- sigma (Float)
- created_at (DateTime)

### model_results
- model_type ("MLP" or "CNN")
- accuracy, precision, recall, f1_score
- sigma (Float)
- created_at (DateTime)

## 🏗️ Model Architectures

### MLP
```
Input → 128 → 64 → Classes
```

### CNN
```
Input → Conv(32) → Conv(64) → FC(128) → Classes
```

## 📁 Key Files

### Implementation
- `backend/main.py` - API endpoints
- `backend/classifiers.py` - MLP & CNN
- `backend/models.py` - Database models

### Utilities
- `backend/setup_database.py` - DB setup
- `backend/test_upload_latent.py` - Testing

### Documentation
- `API_DOCUMENTATION.md` - Full API reference
- `QUICKSTART_CLASSIFIER.md` - Quick start
- `CLASSIFIER_TRAINING_README.md` - Complete guide
- `SYSTEM_ARCHITECTURE.md` - Architecture diagrams

## 🔧 Troubleshooting

### Server won't start
```bash
# Check PostgreSQL is running
# Verify credentials in backend/database.py
```

### Import errors
```bash
pip install -r backend/requirements.txt
```

### Database errors
```bash
python backend/setup_database.py
```

### Test fails
```bash
# Ensure server is running first
python backend/main.py
# Then in another terminal:
python backend/test_upload_latent.py
```

## 📈 Performance Tips

- Use GPU for faster training (automatic)
- Batch size: 32 (configurable)
- Training epochs: 20 (configurable)
- Test split: 20% (stratified)

## 🎯 Next Steps

1. ✅ System is ready to use
2. Run test script to verify
3. Upload your own latent vectors
4. Analyze MLP vs CNN results
5. Experiment with different sigma values

## 📞 Documentation Links

- **API Docs**: `API_DOCUMENTATION.md`
- **Quick Start**: `QUICKSTART_CLASSIFIER.md`
- **Full Guide**: `CLASSIFIER_TRAINING_README.md`
- **Architecture**: `SYSTEM_ARCHITECTURE.md`
- **Summary**: `IMPLEMENTATION_SUMMARY.md`
- **Checklist**: `DELIVERY_CHECKLIST.md`

---

**Status**: ✅ Ready for Production
**Version**: 1.0
**Date**: February 26, 2026

"""
Test script for /upload_latent endpoint
"""
import numpy as np
import requests
from pathlib import Path

# Create sample latent vectors with labels
n_samples = 100
latent_dim = 64
n_classes = 3

# Generate random latent vectors
latent_vectors = np.random.randn(n_samples, latent_dim)

# Generate random labels
labels = np.random.randint(0, n_classes, size=(n_samples, 1))

# Combine vectors and labels
data = np.concatenate([latent_vectors, labels], axis=1)

# Save to .npy file
test_file = Path("test_latent_vectors.npy")
np.save(test_file, data)

print(f"Created test file: {test_file}")
print(f"Shape: {data.shape}")
print(f"Latent dim: {latent_dim}, Classes: {n_classes}, Samples: {n_samples}")

# Test upload
print("\nTesting /upload_latent endpoint...")
try:
    with open(test_file, "rb") as f:
        files = {"file": (test_file.name, f, "application/octet-stream")}
        data = {"sigma": 1.5}
        response = requests.post("http://localhost:8000/upload_latent", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Upload successful!")
        print(f"\nDataset ID: {result['dataset_id']}")
        print("\n📊 MLP Results:")
        print(f"  Accuracy:  {result['mlp_results']['accuracy']:.4f}")
        print(f"  Precision: {result['mlp_results']['precision']:.4f}")
        print(f"  Recall:    {result['mlp_results']['recall']:.4f}")
        print(f"  F1 Score:  {result['mlp_results']['f1_score']:.4f}")
        
        print("\n📊 CNN Results:")
        print(f"  Accuracy:  {result['cnn_results']['accuracy']:.4f}")
        print(f"  Precision: {result['cnn_results']['precision']:.4f}")
        print(f"  Recall:    {result['cnn_results']['recall']:.4f}")
        print(f"  F1 Score:  {result['cnn_results']['f1_score']:.4f}")
        
        print(f"\n🏆 Better Model: {result['comparison']['better_model']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure the server is running: python backend/main.py")

# Cleanup
test_file.unlink()
print(f"\nCleaned up test file: {test_file}")

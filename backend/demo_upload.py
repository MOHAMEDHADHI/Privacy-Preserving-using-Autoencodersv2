"""
Demo script showing realistic latent vector upload
"""
import numpy as np
import requests
import json

print("=" * 70)
print("CLOUD-BASED CLASSIFIER TRAINING DEMO")
print("=" * 70)

# Create more realistic latent vectors (better separable classes)
n_samples = 200
latent_dim = 32
n_classes = 3

print(f"\n📊 Generating synthetic latent vectors...")
print(f"   Samples: {n_samples}")
print(f"   Latent dimension: {latent_dim}")
print(f"   Classes: {n_classes}")

# Generate class-specific latent vectors with better separation
latent_vectors = []
labels = []

for class_id in range(n_classes):
    n_per_class = n_samples // n_classes
    # Each class has different mean
    mean = np.random.randn(latent_dim) * 3
    # Generate samples around that mean
    class_vectors = np.random.randn(n_per_class, latent_dim) * 0.5 + mean
    latent_vectors.append(class_vectors)
    labels.extend([class_id] * n_per_class)

latent_vectors = np.vstack(latent_vectors)
labels = np.array(labels).reshape(-1, 1)

# Shuffle
indices = np.random.permutation(len(latent_vectors))
latent_vectors = latent_vectors[indices]
labels = labels[indices]

# Combine
data = np.concatenate([latent_vectors, labels], axis=1)

# Save
filename = "demo_latent_vectors.npy"
np.save(filename, data)
print(f"   ✅ Saved to {filename}")

# Test different sigma values
sigma_values = [0.5, 1.0, 1.5]

print(f"\n🚀 Testing with different privacy levels (sigma values)...")
print("=" * 70)

results_summary = []

for sigma in sigma_values:
    print(f"\n📤 Uploading with sigma = {sigma}...")
    
    try:
        with open(filename, "rb") as f:
            files = {"file": (filename, f, "application/octet-stream")}
            data_params = {"sigma": sigma}
            response = requests.post(
                "http://localhost:8000/upload_latent",
                files=files,
                data=data_params
            )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"   ✅ Upload successful! Dataset ID: {result['dataset_id']}")
            print(f"\n   📊 MLP Classifier:")
            print(f"      Accuracy:  {result['mlp_results']['accuracy']:.4f}")
            print(f"      Precision: {result['mlp_results']['precision']:.4f}")
            print(f"      Recall:    {result['mlp_results']['recall']:.4f}")
            print(f"      F1 Score:  {result['mlp_results']['f1_score']:.4f}")
            
            print(f"\n   📊 CNN Classifier:")
            print(f"      Accuracy:  {result['cnn_results']['accuracy']:.4f}")
            print(f"      Precision: {result['cnn_results']['precision']:.4f}")
            print(f"      Recall:    {result['cnn_results']['recall']:.4f}")
            print(f"      F1 Score:  {result['cnn_results']['f1_score']:.4f}")
            
            print(f"\n   🏆 Better Model: {result['comparison']['better_model']}")
            
            results_summary.append({
                'sigma': sigma,
                'mlp_accuracy': result['mlp_results']['accuracy'],
                'cnn_accuracy': result['cnn_results']['accuracy'],
                'better_model': result['comparison']['better_model']
            })
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   {response.text}")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Summary
print("\n" + "=" * 70)
print("SUMMARY: Privacy-Utility Tradeoff Analysis")
print("=" * 70)
print(f"\n{'Sigma':<10} {'MLP Acc':<12} {'CNN Acc':<12} {'Winner':<10}")
print("-" * 70)
for r in results_summary:
    print(f"{r['sigma']:<10.1f} {r['mlp_accuracy']:<12.4f} {r['cnn_accuracy']:<12.4f} {r['better_model']:<10}")

print("\n💡 Observation:")
print("   - Lower sigma = Higher accuracy (less privacy)")
print("   - Higher sigma = Lower accuracy (more privacy)")
print("   - Trade-off between privacy and utility")

# Cleanup
import os
os.remove(filename)
print(f"\n🧹 Cleaned up {filename}")

print("\n" + "=" * 70)
print("DEMO COMPLETE")
print("=" * 70)

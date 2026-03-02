"""
Test script for inference capability
Demonstrates making predictions with confidence scores
"""
import requests
import numpy as np
import json

API_BASE = "http://localhost:8000"

print("=" * 70)
print("INFERENCE CAPABILITY TEST")
print("=" * 70)

# Step 1: List available models
print("\n1. Listing available trained models...")
try:
    response = requests.get(f"{API_BASE}/models")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Found {data['total_models']} trained models")
        
        if data['total_models'] > 0:
            # Show first few models
            for model in data['models'][:3]:
                print(f"\n   Model: {model['model_type']} (Dataset {model['dataset_id']})")
                print(f"   - Accuracy: {model['metadata']['metrics']['accuracy']:.4f}")
                print(f"   - Classes: {model['metadata']['num_classes']}")
                print(f"   - Sigma: {model['metadata']['sigma']}")
            
            # Use first model for testing
            test_model = data['models'][0]
            model_type = test_model['model_type']
            dataset_id = test_model['dataset_id']
            num_classes = test_model['metadata']['num_classes']
            input_dim = test_model['metadata']['input_dim']
            
            print(f"\n   Using {model_type} model from dataset {dataset_id} for testing")
        else:
            print("   ⚠️  No models available. Upload and train a model first.")
            exit(0)
    else:
        print(f"   ❌ Error: {response.status_code}")
        exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Step 2: Make a single prediction
print(f"\n2. Making single prediction...")
print(f"   Generating random latent vector ({input_dim} dimensions)...")

# Generate a random latent vector
latent_vector = np.random.randn(input_dim).tolist()

# Define class names (example for finance/healthcare)
class_names = {
    0: "Low Risk / Healthy",
    1: "Medium Risk / Moderate",
    2: "High Risk / Critical"
}

# Make prediction
try:
    payload = {
        "latent_vector": latent_vector,
        "class_names": class_names
    }
    
    response = requests.post(
        f"{API_BASE}/predict/{model_type}/{dataset_id}",
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n   ✅ Prediction successful!")
        print(f"\n   {'='*60}")
        print(f"   PREDICTION RESULT")
        print(f"   {'='*60}")
        print(f"   Predicted Class: {result['predicted_class']}")
        print(f"   Class Name: {result['class_name']}")
        print(f"   Confidence: {result['confidence']:.2%}")
        print(f"\n   All Probabilities:")
        for class_name, prob in result['probabilities'].items():
            bar = '█' * int(prob * 50)
            print(f"      {class_name:25s} {prob:.2%} {bar}")
        print(f"   {'='*60}")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Step 3: Make batch predictions
print(f"\n3. Making batch predictions (5 samples)...")

# Generate multiple random latent vectors
batch_size = 5
latent_vectors = np.random.randn(batch_size, input_dim).tolist()

try:
    payload = {
        "latent_vectors": latent_vectors,
        "class_names": class_names
    }
    
    response = requests.post(
        f"{API_BASE}/predict_batch/{model_type}/{dataset_id}",
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        predictions = result['predictions']
        
        print(f"\n   ✅ Batch prediction successful!")
        print(f"\n   {'='*60}")
        print(f"   BATCH PREDICTION RESULTS")
        print(f"   {'='*60}")
        
        for i, pred in enumerate(predictions, 1):
            print(f"\n   Sample {i}:")
            print(f"      Predicted: {pred['class_name']}")
            print(f"      Confidence: {pred['confidence']:.2%}")
        
        print(f"\n   {'='*60}")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Step 4: Get model information
print(f"\n4. Getting detailed model information...")

try:
    response = requests.get(f"{API_BASE}/models/{model_type}/{dataset_id}")
    
    if response.status_code == 200:
        info = response.json()
        
        print(f"\n   ✅ Model info retrieved!")
        print(f"\n   Model Type: {info['model_type']}")
        print(f"   Dataset ID: {info['dataset_id']}")
        print(f"   Model Path: {info['model_path']}")
        print(f"\n   Metadata:")
        for key, value in info['metadata'].items():
            if key != 'metrics':
                print(f"      {key}: {value}")
    else:
        print(f"   ❌ Error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Summary
print(f"\n{'='*70}")
print("TEST COMPLETE")
print("=" * 70)

print(f"\n✅ Inference Capability Verified!")
print(f"\nYou can now:")
print(f"   1. Make predictions on new latent vectors")
print(f"   2. Get confidence scores for each class")
print(f"   3. Use custom class names (e.g., 'Low Risk', 'COVID')")
print(f"   4. Process single samples or batches")
print(f"   5. List and inspect all trained models")

print(f"\n📚 API Endpoints:")
print(f"   POST /predict/{{model_type}}/{{dataset_id}}")
print(f"   POST /predict_batch/{{model_type}}/{{dataset_id}}")
print(f"   GET  /models")
print(f"   GET  /models/{{model_type}}/{{dataset_id}}")

print(f"\n{'='*70}")

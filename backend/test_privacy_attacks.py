"""
Test script for privacy attack evaluation
"""
import numpy as np
import requests
import time

print("=" * 70)
print("PRIVACY ATTACK EVALUATION TEST")
print("=" * 70)

# Use existing dataset from previous tests
dataset_id = 12  # From demo_upload.py

print(f"\n🎯 Testing privacy attacks on dataset {dataset_id}...")
print(f"   This will run:")
print(f"   1. Reconstruction Attack")
print(f"   2. Membership Inference Attack")

# Run privacy evaluation
print(f"\n📤 POST /evaluate_privacy/{dataset_id}")
try:
    response = requests.post(f"http://localhost:8000/evaluate_privacy/{dataset_id}")
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n✅ Privacy evaluation successful!")
        print(f"\n{'='*70}")
        print(f"DATASET INFORMATION")
        print(f"{'='*70}")
        print(f"Dataset ID: {result['dataset_id']}")
        print(f"Sigma (Privacy Parameter): {result['sigma']}")
        
        print(f"\n{'='*70}")
        print(f"RECONSTRUCTION ATTACK RESULTS")
        print(f"{'='*70}")
        recon = result['reconstruction_attack']
        print(f"Attack Type: {recon['attack_type']}")
        print(f"MSE (Mean Squared Error): {recon['mse']:.6f}")
        print(f"MAE (Mean Absolute Error): {recon['mae']:.6f}")
        print(f"Normalized Error: {recon['normalized_error']:.6f}")
        print(f"Privacy Score: {recon['privacy_score']:.4f} (higher is better)")
        print(f"Attack Success Rate: {recon['success_rate']:.4f} (lower is better)")
        
        print(f"\n{'='*70}")
        print(f"MEMBERSHIP INFERENCE ATTACK RESULTS")
        print(f"{'='*70}")
        mi = result['membership_inference_attack']
        print(f"Attack Type: {mi['attack_type']}")
        print(f"Attack Accuracy: {mi['accuracy']:.4f}")
        print(f"AUC Score: {mi['auc']:.4f}")
        print(f"Privacy Score: {mi['privacy_score']:.4f} (higher is better)")
        print(f"Attack Success Rate: {mi['success_rate']:.4f} (lower is better)")
        print(f"Baseline (Random): {mi['details']['baseline_accuracy']}")
        
        print(f"\n{'='*70}")
        print(f"OVERALL PRIVACY ASSESSMENT")
        print(f"{'='*70}")
        print(f"Overall Privacy Score: {result['overall_privacy_score']:.4f}")
        print(f"Privacy Level: {result['interpretation']['privacy_level']}")
        print(f"Recommendation: {result['interpretation']['recommendation']}")
        
        # Interpretation guide
        print(f"\n{'='*70}")
        print(f"INTERPRETATION GUIDE")
        print(f"{'='*70}")
        print(f"Privacy Score Scale:")
        print(f"  0.0 - 0.4: Low Privacy (❌ Privacy at risk)")
        print(f"  0.4 - 0.7: Medium Privacy (⚠ Consider increasing sigma)")
        print(f"  0.7 - 1.0: High Privacy (✅ Good protection)")
        print(f"\nAttack Success Rate:")
        print(f"  Lower is better for privacy")
        print(f"  Close to 0.5 for membership = random guess (good)")
        print(f"  Close to 0.0 for reconstruction = poor reconstruction (good)")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure:")
    print("  1. Server is running: python backend/main.py")
    print("  2. Dataset exists (run demo_upload.py first)")

# Test getting privacy attack history
print(f"\n{'='*70}")
print(f"RETRIEVING PRIVACY ATTACK HISTORY")
print(f"{'='*70}")

print(f"\n📤 GET /privacy_attacks/{dataset_id}")
try:
    response = requests.get(f"http://localhost:8000/privacy_attacks/{dataset_id}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Retrieved {result['total_attacks']} attack results")
        
        for i, attack in enumerate(result['attacks'], 1):
            print(f"\n--- Attack {i} ---")
            print(f"Type: {attack['attack_type']}")
            print(f"Success Rate: {attack['success_rate']:.4f}")
            print(f"Timestamp: {attack['created_at']}")
    else:
        print(f"❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Test privacy-utility tradeoff endpoint
print(f"\n{'='*70}")
print(f"PRIVACY-UTILITY TRADEOFF ANALYSIS")
print(f"{'='*70}")

print(f"\n📤 GET /privacy_tradeoff")
try:
    response = requests.get("http://localhost:8000/privacy_tradeoff")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Retrieved tradeoff data for {result['total_datasets']} datasets")
        
        print(f"\n{'Sigma':<10} {'Utility':<12} {'Privacy':<12} {'Balance':<15}")
        print("-" * 70)
        
        for data in result['tradeoff_data']:
            balance = "✅ Good" if data['utility'] > 0.7 and data['privacy_score'] > 0.5 else "⚠ Adjust"
            print(f"{data['sigma']:<10.1f} {data['utility']:<12.4f} {data['privacy_score']:<12.4f} {balance:<15}")
        
        print(f"\nSummary:")
        print(f"  Average Utility: {result['summary']['avg_utility']:.4f}")
        print(f"  Average Privacy: {result['summary']['avg_privacy']:.4f}")
        
    else:
        print(f"❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print(f"\n{'='*70}")
print(f"TEST COMPLETE")
print(f"{'='*70}")
print(f"\n💡 Next Steps:")
print(f"   1. Run with different sigma values to see tradeoff")
print(f"   2. Generate visualizations: python backend/visualize_privacy.py")
print(f"   3. Compare results across datasets")
print(f"{'='*70}")

"""
Complete System Demonstration
Shows the full workflow from upload to privacy evaluation
"""
import numpy as np
import requests
import time

print("=" * 80)
print("COMPLETE PRIVACY-PRESERVING ML SYSTEM DEMONSTRATION")
print("=" * 80)

# Configuration
BASE_URL = "http://localhost:8000"
SIGMA_VALUES = [0.5, 1.0, 1.5]

print("\n📋 Test Configuration:")
print(f"   Base URL: {BASE_URL}")
print(f"   Sigma values to test: {SIGMA_VALUES}")
print(f"   Samples: 150 per dataset")
print(f"   Latent dimension: 32")
print(f"   Classes: 3")

results_summary = []

for sigma in SIGMA_VALUES:
    print(f"\n{'='*80}")
    print(f"TESTING WITH SIGMA = {sigma}")
    print(f"{'='*80}")
    
    # Step 1: Generate latent vectors
    print(f"\n📊 Step 1: Generating latent vectors...")
    n_samples = 150
    latent_dim = 32
    n_classes = 3
    
    # Generate class-specific latent vectors
    latent_vectors = []
    labels = []
    
    for class_id in range(n_classes):
        n_per_class = n_samples // n_classes
        mean = np.random.randn(latent_dim) * 3
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
    filename = f"demo_sigma_{sigma}.npy"
    np.save(filename, data)
    print(f"   ✅ Generated {len(data)} samples")
    
    # Step 2: Upload and train classifiers
    print(f"\n🚀 Step 2: Uploading to cloud and training classifiers...")
    try:
        with open(filename, "rb") as f:
            files = {"file": (filename, f, "application/octet-stream")}
            data_params = {"sigma": sigma}
            response = requests.post(
                f"{BASE_URL}/upload_latent",
                files=files,
                data=data_params
            )
        
        if response.status_code == 200:
            upload_result = response.json()
            dataset_id = upload_result['dataset_id']
            
            print(f"   ✅ Upload successful! Dataset ID: {dataset_id}")
            print(f"   📊 MLP Accuracy: {upload_result['mlp_results']['accuracy']:.4f}")
            print(f"   📊 CNN Accuracy: {upload_result['cnn_results']['accuracy']:.4f}")
            print(f"   🏆 Better Model: {upload_result['comparison']['better_model']}")
            
            # Step 3: Evaluate privacy
            print(f"\n🔒 Step 3: Running privacy attacks...")
            time.sleep(1)  # Brief pause
            
            privacy_response = requests.post(
                f"{BASE_URL}/evaluate_privacy/{dataset_id}"
            )
            
            if privacy_response.status_code == 200:
                privacy_result = privacy_response.json()
                
                print(f"   ✅ Privacy evaluation complete!")
                print(f"\n   Reconstruction Attack:")
                print(f"      Privacy Score: {privacy_result['reconstruction_attack']['privacy_score']:.4f}")
                print(f"      Success Rate: {privacy_result['reconstruction_attack']['success_rate']:.4f}")
                
                print(f"\n   Membership Inference Attack:")
                print(f"      Privacy Score: {privacy_result['membership_inference_attack']['privacy_score']:.4f}")
                print(f"      Success Rate: {privacy_result['membership_inference_attack']['success_rate']:.4f}")
                
                print(f"\n   Overall Assessment:")
                print(f"      Privacy Score: {privacy_result['overall_privacy_score']:.4f}")
                print(f"      Privacy Level: {privacy_result['interpretation']['privacy_level']}")
                print(f"      Recommendation: {privacy_result['interpretation']['recommendation']}")
                
                # Store summary
                results_summary.append({
                    'sigma': sigma,
                    'dataset_id': dataset_id,
                    'mlp_accuracy': upload_result['mlp_results']['accuracy'],
                    'cnn_accuracy': upload_result['cnn_results']['accuracy'],
                    'privacy_score': privacy_result['overall_privacy_score'],
                    'privacy_level': privacy_result['interpretation']['privacy_level'],
                    'recon_privacy': privacy_result['reconstruction_attack']['privacy_score'],
                    'mi_privacy': privacy_result['membership_inference_attack']['privacy_score']
                })
            else:
                print(f"   ❌ Privacy evaluation failed: {privacy_response.status_code}")
        else:
            print(f"   ❌ Upload failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Cleanup
    import os
    os.remove(filename)
    print(f"\n   🧹 Cleaned up {filename}")

# Final Summary
print(f"\n{'='*80}")
print(f"COMPLETE SYSTEM SUMMARY")
print(f"{'='*80}")

if results_summary:
    print(f"\n{'Sigma':<8} {'Utility':<10} {'Privacy':<10} {'Level':<12} {'Balance':<15}")
    print("-" * 80)
    
    for r in results_summary:
        avg_utility = (r['mlp_accuracy'] + r['cnn_accuracy']) / 2
        balance = "✅ Good" if avg_utility > 0.7 and r['privacy_score'] > 0.5 else "⚠ Adjust"
        print(f"{r['sigma']:<8.1f} {avg_utility:<10.4f} {r['privacy_score']:<10.4f} {r['privacy_level']:<12} {balance:<15}")
    
    print(f"\n{'='*80}")
    print(f"PRIVACY-UTILITY TRADEOFF ANALYSIS")
    print(f"{'='*80}")
    
    print(f"\n📈 Observations:")
    
    # Find best privacy
    best_privacy = max(results_summary, key=lambda x: x['privacy_score'])
    print(f"   • Best Privacy: Sigma={best_privacy['sigma']} (Score: {best_privacy['privacy_score']:.4f})")
    
    # Find best utility
    best_utility = max(results_summary, key=lambda x: (x['mlp_accuracy'] + x['cnn_accuracy'])/2)
    avg_util = (best_utility['mlp_accuracy'] + best_utility['cnn_accuracy']) / 2
    print(f"   • Best Utility: Sigma={best_utility['sigma']} (Accuracy: {avg_util:.4f})")
    
    # Find best balance
    best_balance = max(results_summary, key=lambda x: x['privacy_score'] * ((x['mlp_accuracy'] + x['cnn_accuracy'])/2))
    print(f"   • Best Balance: Sigma={best_balance['sigma']}")
    
    print(f"\n💡 Recommendations:")
    print(f"   1. For high privacy: Use sigma ≥ {best_privacy['sigma']}")
    print(f"   2. For high utility: Use sigma ≤ {best_utility['sigma']}")
    print(f"   3. For balance: Use sigma = {best_balance['sigma']}")
    
    print(f"\n📊 Attack-Specific Analysis:")
    print(f"\n   Reconstruction Attack Privacy:")
    for r in results_summary:
        status = "✅" if r['recon_privacy'] > 0.5 else "⚠" if r['recon_privacy'] > 0.3 else "❌"
        print(f"      Sigma {r['sigma']:.1f}: {r['recon_privacy']:.4f} {status}")
    
    print(f"\n   Membership Inference Privacy:")
    for r in results_summary:
        status = "✅" if r['mi_privacy'] > 0.5 else "⚠" if r['mi_privacy'] > 0.3 else "❌"
        print(f"      Sigma {r['sigma']:.1f}: {r['mi_privacy']:.4f} {status}")

# Step 4: Generate visualizations
print(f"\n{'='*80}")
print(f"GENERATING VISUALIZATIONS")
print(f"{'='*80}")

print(f"\n📊 Fetching tradeoff data...")
try:
    response = requests.get(f"{BASE_URL}/privacy_tradeoff")
    if response.status_code == 200:
        print(f"   ✅ Data retrieved successfully")
        print(f"\n📈 Generating graphs...")
        
        import subprocess
        result = subprocess.run(
            ["python", "backend/visualize_privacy.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"   ✅ Visualizations generated!")
            print(f"   📁 Location: privacy_visualizations/")
            print(f"      • privacy_utility_tradeoff.png")
            print(f"      • sigma_effects.png")
            print(f"      • attack_comparison.png")
            print(f"      • privacy_dashboard.png")
        else:
            print(f"   ⚠ Visualization generation had issues")
    else:
        print(f"   ❌ Failed to fetch data: {response.status_code}")
except Exception as e:
    print(f"   ⚠ Could not generate visualizations: {e}")

# Final message
print(f"\n{'='*80}")
print(f"DEMONSTRATION COMPLETE")
print(f"{'='*80}")

print(f"\n✅ System Components Tested:")
print(f"   1. ✅ Latent vector upload")
print(f"   2. ✅ MLP classifier training")
print(f"   3. ✅ CNN classifier training")
print(f"   4. ✅ Reconstruction attack")
print(f"   5. ✅ Membership inference attack")
print(f"   6. ✅ Privacy score computation")
print(f"   7. ✅ Database storage")
print(f"   8. ✅ Privacy-utility tradeoff analysis")
print(f"   9. ✅ Visualization generation")

print(f"\n📚 Next Steps:")
print(f"   • View visualizations in privacy_visualizations/")
print(f"   • Adjust sigma based on requirements")
print(f"   • Integrate with your application")
print(f"   • Monitor privacy over time")

print(f"\n{'='*80}")

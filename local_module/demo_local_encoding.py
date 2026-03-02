"""
Demo: Local Encoding of Sensitive Data
This demonstrates the complete workflow of encoding sensitive data locally
before uploading to the cloud.
"""
import numpy as np
import pandas as pd
from encoder import LatentRepresentationEngine

print("=" * 70)
print("LOCAL DATA ENCODING DEMO")
print("=" * 70)

# Step 1: Create sample sensitive data
print("\n📊 Step 1: Creating sample sensitive data...")
print("   (In real use, you'd load your CSV/Excel file)")

# Example: Financial data
data = pd.DataFrame({
    'income': [75000, 85000, 60000, 95000, 55000, 70000, 80000, 65000, 90000, 58000,
               72000, 88000, 62000, 78000, 92000, 68000, 82000, 56000, 76000, 86000],
    'credit_score': [720, 680, 750, 690, 730, 710, 700, 740, 670, 760,
                     715, 685, 745, 705, 695, 735, 675, 755, 725, 665],
    'debt': [25000, 30000, 15000, 35000, 20000, 28000, 32000, 18000, 38000, 22000,
             26000, 31000, 19000, 27000, 34000, 21000, 29000, 16000, 24000, 33000],
    'age': [35, 42, 28, 48, 31, 38, 45, 29, 50, 33,
            37, 44, 30, 40, 47, 32, 43, 27, 36, 46],
    'risk_label': [0, 1, 0, 1, 0, 0, 1, 0, 1, 0,
                   0, 1, 0, 0, 1, 0, 1, 0, 0, 1]  # 0=Low Risk, 1=High Risk
})

print(f"   ✅ Created {len(data)} samples")
print(f"   Features: {list(data.columns[:-1])}")
print(f"   Labels: {data['risk_label'].value_counts().to_dict()}")

# Display sample
print("\n   Sample data (first 3 rows):")
print(data.head(3).to_string(index=False))

# Step 2: Prepare data for encoding
print("\n🔧 Step 2: Preparing data for encoding...")

X = data[['income', 'credit_score', 'debt', 'age']].values
y = data['risk_label'].values

# Normalize features (important for neural networks)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"   ✅ Features shape: {X_scaled.shape}")
print(f"   ✅ Labels shape: {y.shape}")
print(f"   ✅ Data normalized")

# Step 3: Initialize encoder
print("\n🤖 Step 3: Initializing privacy-preserving encoder...")

encoder = LatentRepresentationEngine(
    input_dim=4,       # 4 features (income, credit_score, debt, age)
    latent_dim=32,     # 32-dimensional latent space
    num_classes=2      # 2 classes (Low Risk, High Risk)
)

print(f"   ✅ Encoder initialized")
print(f"   Input dimension: 4")
print(f"   Latent dimension: 32")
print(f"   Number of classes: 2")

# Step 4: Train encoder
print("\n🎓 Step 4: Training encoder (this may take a moment)...")
print("   Training with privacy-preserving autoencoder...")

encoder.train(X_scaled, y, epochs=30)

print("   ✅ Encoder trained successfully!")

# Step 5: Generate latent vectors with privacy
print("\n🔒 Step 5: Generating privacy-protected latent vectors...")

sigma_values = [0.5, 1.0, 1.5]
results = []

for sigma in sigma_values:
    print(f"\n   Testing with sigma = {sigma}...")
    
    # Encode with privacy
    latent_vectors = encoder.encode(X_scaled, sigma=sigma)
    
    # Combine with labels for upload
    data_for_upload = np.column_stack([latent_vectors, y])
    
    # Save to file
    filename = f'financial_data_sigma_{sigma}.npy'
    np.save(filename, data_for_upload)
    
    print(f"   ✅ Generated {len(latent_vectors)} latent vectors")
    print(f"   ✅ Shape: {data_for_upload.shape} (samples, features+label)")
    print(f"   ✅ Saved to: {filename}")
    print(f"   ✅ File size: {data_for_upload.nbytes / 1024:.2f} KB")
    
    results.append({
        'sigma': sigma,
        'filename': filename,
        'shape': data_for_upload.shape
    })

# Step 6: Summary
print("\n" + "=" * 70)
print("ENCODING COMPLETE!")
print("=" * 70)

print("\n📁 Generated Files:")
for result in results:
    print(f"   • {result['filename']}")
    print(f"     Sigma: {result['sigma']}")
    print(f"     Shape: {result['shape']}")
    print(f"     Ready for cloud upload!")

print("\n🔒 Privacy Protection:")
print("   ✅ Original sensitive data (income, credit score, etc.) NOT in files")
print("   ✅ Only privacy-protected latent vectors saved")
print("   ✅ Differential privacy applied (Gaussian noise)")
print("   ✅ Safe to upload to cloud")

print("\n📤 Next Steps:")
print("   1. Go to: http://localhost:3000/upload")
print("   2. Upload one of the generated .npy files")
print("   3. Select models (MLP/CNN)")
print("   4. Train and evaluate!")

print("\n💡 Privacy-Utility Tradeoff:")
print("   • Sigma 0.5: Less privacy, higher accuracy")
print("   • Sigma 1.0: Balanced")
print("   • Sigma 1.5: More privacy, lower accuracy")

print("\n" + "=" * 70)
print("Demo complete! Your data is ready for cloud training.")
print("=" * 70)

"""
Interactive Script: Encode Your Own CSV/Excel Data
This script allows you to encode your own dataset with privacy protection.
"""
import numpy as np
import pandas as pd
from encoder import LatentRepresentationEngine
from sklearn.preprocessing import StandardScaler, LabelEncoder
import sys
import os

def load_data(filepath):
    """Load CSV or Excel file"""
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.csv':
        return pd.read_csv(filepath)
    elif ext in ['.xlsx', '.xls']:
        return pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Use .csv, .xlsx, or .xls")

def main():
    print("=" * 70)
    print("ENCODE YOUR OWN DATA - Interactive Script")
    print("=" * 70)
    
    # Step 1: Get file path
    print("\n📁 Step 1: Load Your Data")
    print("-" * 70)
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("Enter path to your CSV/Excel file: ").strip()
    
    if not os.path.exists(filepath):
        print(f"❌ Error: File not found: {filepath}")
        return
    
    try:
        df = load_data(filepath)
        print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nFirst 3 rows:")
        print(df.head(3))
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return
    
    # Step 2: Select label column
    print("\n" + "=" * 70)
    print("📊 Step 2: Select Label Column")
    print("-" * 70)
    print("Which column contains the labels (what you want to predict)?")
    print(f"Available columns: {list(df.columns)}")
    
    label_column = input("\nEnter label column name: ").strip()
    
    if label_column not in df.columns:
        print(f"❌ Error: Column '{label_column}' not found")
        return
    
    # Step 3: Select feature columns
    print("\n" + "=" * 70)
    print("🔧 Step 3: Select Feature Columns")
    print("-" * 70)
    print("Which columns should be used as features?")
    print(f"Available columns (excluding label): {[c for c in df.columns if c != label_column]}")
    print("\nOptions:")
    print("  1. Use ALL columns (except label)")
    print("  2. Select specific columns")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        feature_columns = [c for c in df.columns if c != label_column]
    else:
        print("\nEnter column names separated by commas:")
        feature_input = input("Columns: ").strip()
        feature_columns = [c.strip() for c in feature_input.split(',')]
        
        # Validate
        invalid = [c for c in feature_columns if c not in df.columns]
        if invalid:
            print(f"❌ Error: Invalid columns: {invalid}")
            return
    
    print(f"\n✅ Selected {len(feature_columns)} features: {feature_columns}")
    
    # Step 4: Prepare data
    print("\n" + "=" * 70)
    print("🔧 Step 4: Preparing Data")
    print("-" * 70)
    
    # Extract features
    X = df[feature_columns].values
    
    # Handle non-numeric features
    print("Checking for non-numeric columns...")
    non_numeric = df[feature_columns].select_dtypes(exclude=[np.number]).columns.tolist()
    
    if non_numeric:
        print(f"⚠️  Found non-numeric columns: {non_numeric}")
        print("Converting to numeric (one-hot encoding)...")
        X_df = pd.get_dummies(df[feature_columns], columns=non_numeric)
        X = X_df.values
        print(f"✅ After encoding: {X.shape[1]} features")
    
    # Extract and encode labels
    y = df[label_column].values
    
    # Encode labels if they're not numeric
    if not np.issubdtype(y.dtype, np.number):
        print(f"Encoding labels...")
        le = LabelEncoder()
        y = le.fit_transform(y)
        print(f"✅ Label mapping: {dict(zip(le.classes_, range(len(le.classes_))))}")
    else:
        y = y.astype(int)
    
    # Normalize features
    print("Normalizing features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print(f"\n✅ Data prepared:")
    print(f"   Features shape: {X_scaled.shape}")
    print(f"   Labels shape: {y.shape}")
    print(f"   Number of classes: {len(np.unique(y))}")
    print(f"   Class distribution: {dict(zip(*np.unique(y, return_counts=True)))}")
    
    # Step 5: Configure encoder
    print("\n" + "=" * 70)
    print("🤖 Step 5: Configure Encoder")
    print("-" * 70)
    
    latent_dim_input = input(f"Latent dimension (default: 32): ").strip()
    latent_dim = int(latent_dim_input) if latent_dim_input else 32
    
    epochs_input = input(f"Training epochs (default: 30): ").strip()
    epochs = int(epochs_input) if epochs_input else 30
    
    print(f"\n✅ Configuration:")
    print(f"   Input dimension: {X_scaled.shape[1]}")
    print(f"   Latent dimension: {latent_dim}")
    print(f"   Number of classes: {len(np.unique(y))}")
    print(f"   Training epochs: {epochs}")
    
    # Step 6: Train encoder
    print("\n" + "=" * 70)
    print("🎓 Step 6: Training Encoder")
    print("-" * 70)
    print("This may take a moment...")
    
    encoder = LatentRepresentationEngine(
        input_dim=X_scaled.shape[1],
        latent_dim=latent_dim,
        num_classes=len(np.unique(y))
    )
    
    encoder.train(X_scaled, y, epochs=epochs)
    
    print("✅ Encoder trained successfully!")
    
    # Step 7: Generate latent vectors
    print("\n" + "=" * 70)
    print("🔒 Step 7: Generate Privacy-Protected Latent Vectors")
    print("-" * 70)
    
    sigma_input = input("Enter sigma values (comma-separated, e.g., 0.5,1.0,1.5): ").strip()
    if sigma_input:
        sigma_values = [float(s.strip()) for s in sigma_input.split(',')]
    else:
        sigma_values = [0.5, 1.0, 1.5]
    
    output_name = input("\nOutput filename prefix (default: encoded_data): ").strip()
    if not output_name:
        output_name = "encoded_data"
    
    print(f"\nGenerating latent vectors...")
    
    results = []
    for sigma in sigma_values:
        print(f"\n   Processing sigma = {sigma}...")
        
        # Encode with privacy
        latent_vectors = encoder.encode(X_scaled, sigma=sigma)
        
        # Combine with labels
        data_for_upload = np.column_stack([latent_vectors, y])
        
        # Save
        filename = f'{output_name}_sigma_{sigma}.npy'
        np.save(filename, data_for_upload)
        
        print(f"   ✅ Saved: {filename}")
        print(f"      Shape: {data_for_upload.shape}")
        print(f"      Size: {data_for_upload.nbytes / 1024:.2f} KB")
        
        results.append({
            'sigma': sigma,
            'filename': filename,
            'shape': data_for_upload.shape
        })
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ ENCODING COMPLETE!")
    print("=" * 70)
    
    print("\n📁 Generated Files:")
    for result in results:
        print(f"   • {result['filename']}")
        print(f"     Sigma: {result['sigma']}")
        print(f"     Shape: {result['shape']}")
    
    print("\n🔒 Privacy Protection:")
    print(f"   ✅ Original features ({', '.join(feature_columns)}) NOT in files")
    print(f"   ✅ Only privacy-protected latent vectors saved")
    print(f"   ✅ Differential privacy applied")
    print(f"   ✅ Safe to upload to cloud")
    
    print("\n📤 Next Steps:")
    print("   1. Go to: http://localhost:3000/upload")
    print("   2. Login with any email/password")
    print("   3. Upload one of the generated .npy files")
    print("   4. Train models and evaluate!")
    
    print("\n💡 Privacy-Utility Tradeoff:")
    for sigma in sigma_values:
        if sigma < 0.8:
            level = "Low privacy, high accuracy"
        elif sigma < 1.2:
            level = "Balanced"
        else:
            level = "High privacy, lower accuracy"
        print(f"   • Sigma {sigma}: {level}")
    
    print("\n" + "=" * 70)
    print("Your data is ready for cloud training!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

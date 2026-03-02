"""
Example usage of the Privacy-Preserving Encoder
"""
import pandas as pd
import numpy as np
from privacy_engine import PrivacyEngine
from dataset_loader import DatasetLoader

def example_workflow():
    # Load dataset
    loader = DatasetLoader()
    df = loader.load_csv('sample_data.csv')  # Replace with actual file
    
    # Initialize privacy engine
    engine = PrivacyEngine()
    
    # Configure parameters
    target_column = 'label'  # User selects
    protected_features = ['age', 'gender']  # User selects
    sigma = 0.1  # Adjustable privacy parameter
    latent_dim = 32
    epochs = 50
    
    # Process dataset
    latent_vectors, metadata = engine.process_dataset(
        df=df,
        target_column=target_column,
        protected_features=protected_features,
        sigma=sigma,
        latent_dim=latent_dim,
        epochs=epochs
    )
    
    # Export latent vectors
    engine.encoder.export_latent_vectors(latent_vectors, 'latent_vectors.npy')
    
    print(f"Generated {latent_vectors.shape[0]} latent vectors")
    print(f"Latent dimension: {latent_vectors.shape[1]}")
    print(f"Metadata: {metadata}")
    
    return latent_vectors, metadata

if __name__ == "__main__":
    print("Example workflow for Privacy-Preserving Encoder")
    print("Modify the parameters in example_workflow() to match your dataset")

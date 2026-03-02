import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from encoder import LatentRepresentationEngine

class PrivacyEngine:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.encoder = None
    
    def preprocess_data(self, df: pd.DataFrame, target_column: str, 
                       protected_features: list) -> tuple:
        """Preprocess dataset for encoding"""
        # Separate features and target
        X = df.drop(columns=[target_column])
        y = df[target_column]
        
        # Encode categorical variables
        for col in X.select_dtypes(include=['object']).columns:
            X[col] = LabelEncoder().fit_transform(X[col].astype(str))
        
        # Encode target
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y_encoded
    
    def train_encoder(self, X: np.ndarray, y: np.ndarray, 
                     latent_dim: int = 32, epochs: int = 50):
        """Train the privacy-preserving encoder"""
        input_dim = X.shape[1]
        num_classes = len(np.unique(y))
        
        self.encoder = LatentRepresentationEngine(input_dim, latent_dim, num_classes)
        self.encoder.train(X, y, epochs=epochs)
        
        return self.encoder
    
    def generate_latent_vectors(self, X: np.ndarray, sigma: float = 0.1) -> np.ndarray:
        """Generate privacy-preserving latent vectors"""
        if self.encoder is None:
            raise ValueError("Encoder not trained. Call train_encoder first.")
        
        latent_vectors = self.encoder.encode(X, sigma=sigma)
        return latent_vectors
    
    def process_dataset(self, df: pd.DataFrame, target_column: str,
                       protected_features: list, sigma: float = 0.1,
                       latent_dim: int = 32, epochs: int = 50):
        """Complete pipeline: preprocess, train, encode"""
        # Configure encoder
        X, y = self.preprocess_data(df, target_column, protected_features)
        
        # Train encoder
        self.train_encoder(X, y, latent_dim, epochs)
        self.encoder.configure(target_column, protected_features)
        
        # Generate latent vectors
        latent_vectors = self.generate_latent_vectors(X, sigma)
        
        return latent_vectors, self.encoder.get_metadata()

if __name__ == "__main__":
    print("Privacy Engine initialized successfully")

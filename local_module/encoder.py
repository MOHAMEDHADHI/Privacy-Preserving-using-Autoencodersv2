import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import Tuple, Optional

class Encoder(nn.Module):
    def __init__(self, input_dim: int, latent_dim: int):
        super(Encoder, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, latent_dim)
        )
    
    def forward(self, x):
        return self.network(x)

class Decoder(nn.Module):
    def __init__(self, latent_dim: int, output_dim: int):
        super(Decoder, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, output_dim)
        )
    
    def forward(self, z):
        return self.network(z)

class AuxiliaryClassifier(nn.Module):
    def __init__(self, latent_dim: int, num_classes: int):
        super(AuxiliaryClassifier, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(latent_dim, 32),
            nn.ReLU(),
            nn.Linear(32, num_classes)
        )
    
    def forward(self, z):
        return self.network(z)

class PrivacyPreservingAutoencoder(nn.Module):
    def __init__(self, input_dim: int, latent_dim: int, num_classes: int):
        super(PrivacyPreservingAutoencoder, self).__init__()
        self.encoder = Encoder(input_dim, latent_dim)
        self.decoder = Decoder(latent_dim, input_dim)
        self.classifier = AuxiliaryClassifier(latent_dim, num_classes)
        self.latent_dim = latent_dim
    
    def forward(self, x):
        z = self.encoder(x)
        x_recon = self.decoder(z)
        y_pred = self.classifier(z)
        return z, x_recon, y_pred
    
    def add_differential_privacy(self, z: torch.Tensor, sigma: float) -> torch.Tensor:
        """Add Gaussian noise for differential privacy"""
        noise = torch.randn_like(z) * sigma
        return z + noise

class LatentRepresentationEngine:
    def __init__(self, input_dim: int, latent_dim: int = 32, num_classes: int = 2):
        self.model = PrivacyPreservingAutoencoder(input_dim, latent_dim, num_classes)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.mse_loss = nn.MSELoss()
        self.ce_loss = nn.CrossEntropyLoss()
        self.metadata = {}
    
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 50, 
              recon_weight: float = 1.0, class_weight: float = 0.5):
        """Train the autoencoder with multi-objective loss"""
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.LongTensor(y)
        
        self.model.train()
        for epoch in range(epochs):
            self.optimizer.zero_grad()
            
            z, x_recon, y_pred = self.model(X_tensor)
            
            # Multi-objective loss
            recon_loss = self.mse_loss(x_recon, X_tensor)
            class_loss = self.ce_loss(y_pred, y_tensor)
            total_loss = recon_weight * recon_loss + class_weight * class_loss
            
            total_loss.backward()
            self.optimizer.step()
            
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}/{epochs} - Loss: {total_loss.item():.4f}")
    
    def encode(self, X: np.ndarray, sigma: float = 0.0) -> np.ndarray:
        """Generate latent vectors with optional differential privacy"""
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X)
            z = self.model.encoder(X_tensor)
            
            if sigma > 0:
                z = self.model.add_differential_privacy(z, sigma)
            
            return z.numpy()
    
    def configure(self, target_column: str, protected_features: list):
        """Store configuration metadata"""
        self.metadata = {
            'target_column': target_column,
            'protected_features': protected_features,
            'latent_dim': self.model.latent_dim
        }
    
    def export_latent_vectors(self, latent_vectors: np.ndarray, filepath: str):
        """Export latent vectors for cloud transmission"""
        np.save(filepath, latent_vectors)
        print(f"Latent vectors saved to {filepath}")
    
    def get_metadata(self):
        """Return configuration metadata"""
        return self.metadata

if __name__ == "__main__":
    print("Privacy-Preserving Encoder initialized successfully")

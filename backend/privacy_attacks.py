"""
Privacy Attack Framework
Implements reconstruction and membership inference attacks
"""
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from typing import Dict, Tuple
import json


class ReconstructionAttacker(nn.Module):
    """Neural network to attempt reconstruction from latent vectors"""
    def __init__(self, latent_dim: int, output_dim: int):
        super(ReconstructionAttacker, self).__init__()
        self.fc1 = nn.Linear(latent_dim, 128)
        self.fc2 = nn.Linear(128, 256)
        self.fc3 = nn.Linear(256, output_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x


class MembershipInferenceAttacker(nn.Module):
    """Binary classifier to predict training membership"""
    def __init__(self, latent_dim: int):
        super(MembershipInferenceAttacker, self).__init__()
        self.fc1 = nn.Linear(latent_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)  # Binary: member or non-member
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x


def reconstruction_attack(
    latent_vectors: np.ndarray,
    original_data: np.ndarray,
    sigma: float,
    epochs: int = 30
) -> Dict:
    """
    Attempt to reconstruct original data from latent vectors
    
    Args:
        latent_vectors: Encoded latent representations
        original_data: Original data before encoding
        sigma: Privacy parameter used
        epochs: Training epochs for attacker
    
    Returns:
        Dictionary with attack metrics
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        latent_vectors, original_data, test_size=0.3, random_state=42
    )
    
    # Convert to tensors
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(y_train)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.FloatTensor(y_test)
    
    # Create data loaders
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    # Initialize attacker model
    latent_dim = latent_vectors.shape[1]
    output_dim = original_data.shape[1]
    model = ReconstructionAttacker(latent_dim, output_dim).to(device)
    
    # Train attacker
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    model.train()
    for epoch in range(epochs):
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
    
    # Evaluate reconstruction
    model.eval()
    all_reconstructed = []
    all_original = []
    
    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            all_reconstructed.append(outputs.cpu().numpy())
            all_original.append(targets.numpy())
    
    reconstructed = np.vstack(all_reconstructed)
    original = np.vstack(all_original)
    
    # Compute reconstruction error
    mse = np.mean((reconstructed - original) ** 2)
    mae = np.mean(np.abs(reconstructed - original))
    
    # Normalized error (0-1 scale)
    data_range = np.max(original) - np.min(original)
    normalized_error = mse / (data_range ** 2) if data_range > 0 else mse
    
    # Privacy score (higher is better, 0-1 scale)
    # If reconstruction error is high, privacy is good
    privacy_score = min(1.0, normalized_error)
    
    return {
        "attack_type": "reconstruction",
        "mse": float(mse),
        "mae": float(mae),
        "normalized_error": float(normalized_error),
        "privacy_score": float(privacy_score),
        "sigma": sigma,
        "success_rate": float(1.0 - privacy_score),  # Lower is better for privacy
        "details": {
            "epochs": epochs,
            "test_samples": len(original),
            "latent_dim": latent_dim,
            "output_dim": output_dim
        }
    }


def membership_inference_attack(
    train_latent: np.ndarray,
    test_latent: np.ndarray,
    sigma: float,
    epochs: int = 20
) -> Dict:
    """
    Attempt to infer if a sample was in the training set
    
    Args:
        train_latent: Latent vectors from training set
        test_latent: Latent vectors from test/holdout set
        sigma: Privacy parameter used
        epochs: Training epochs for attacker
    
    Returns:
        Dictionary with attack metrics
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Create labels: 1 for training members, 0 for non-members
    train_labels = np.ones(len(train_latent))
    test_labels = np.zeros(len(test_latent))
    
    # Combine data
    all_latent = np.vstack([train_latent, test_latent])
    all_labels = np.concatenate([train_labels, test_labels])
    
    # Split for attack training
    X_train, X_test, y_train, y_test = train_test_split(
        all_latent, all_labels, test_size=0.3, random_state=42, stratify=all_labels
    )
    
    # Convert to tensors
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.LongTensor(y_train.astype(int))
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.LongTensor(y_test.astype(int))
    
    # Create data loaders
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    # Initialize attacker model
    latent_dim = all_latent.shape[1]
    model = MembershipInferenceAttacker(latent_dim).to(device)
    
    # Train attacker
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    model.train()
    for epoch in range(epochs):
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    
    # Evaluate attack
    model.eval()
    all_preds = []
    all_probs = []
    all_labels_test = []
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            probs = torch.softmax(outputs, dim=1)
            _, predicted = torch.max(outputs, 1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_probs.extend(probs[:, 1].cpu().numpy())  # Probability of being member
            all_labels_test.extend(labels.numpy())
    
    # Compute metrics
    accuracy = accuracy_score(all_labels_test, all_preds)
    
    # AUC score
    try:
        auc = roc_auc_score(all_labels_test, all_probs)
    except:
        auc = 0.5  # Random guess baseline
    
    # Privacy score (higher is better)
    # If attack accuracy is close to 0.5 (random), privacy is good
    privacy_score = 1.0 - abs(accuracy - 0.5) * 2  # Scale to 0-1
    
    return {
        "attack_type": "membership_inference",
        "accuracy": float(accuracy),
        "auc": float(auc),
        "privacy_score": float(privacy_score),
        "sigma": sigma,
        "success_rate": float(accuracy),
        "details": {
            "epochs": epochs,
            "test_samples": len(all_labels_test),
            "latent_dim": latent_dim,
            "baseline_accuracy": 0.5  # Random guess
        }
    }


def simulate_membership_attack_simple(
    latent_vectors: np.ndarray,
    sigma: float
) -> Dict:
    """
    Simplified membership inference attack using statistical properties
    When we don't have separate train/test sets
    """
    # Split the data to simulate train/test
    split_idx = int(len(latent_vectors) * 0.7)
    train_latent = latent_vectors[:split_idx]
    test_latent = latent_vectors[split_idx:]
    
    return membership_inference_attack(train_latent, test_latent, sigma)


def evaluate_privacy(
    latent_vectors: np.ndarray,
    original_data: np.ndarray,
    sigma: float
) -> Dict:
    """
    Comprehensive privacy evaluation
    
    Args:
        latent_vectors: Encoded latent representations
        original_data: Original data before encoding
        sigma: Privacy parameter used
    
    Returns:
        Dictionary with all attack results
    """
    results = {}
    
    # Reconstruction attack
    print(f"Running reconstruction attack (sigma={sigma})...")
    recon_results = reconstruction_attack(latent_vectors, original_data, sigma)
    results["reconstruction"] = recon_results
    
    # Membership inference attack
    print(f"Running membership inference attack (sigma={sigma})...")
    mi_results = simulate_membership_attack_simple(latent_vectors, sigma)
    results["membership_inference"] = mi_results
    
    # Overall privacy score (average of both attacks)
    overall_privacy = (
        recon_results["privacy_score"] + mi_results["privacy_score"]
    ) / 2
    
    results["overall_privacy_score"] = float(overall_privacy)
    results["sigma"] = sigma
    
    return results


def generate_privacy_utility_data(results_list: list) -> Dict:
    """
    Generate data for privacy-utility tradeoff visualization
    
    Args:
        results_list: List of results with different sigma values
    
    Returns:
        Dictionary with data for plotting
    """
    sigma_values = []
    privacy_scores = []
    utility_scores = []
    recon_errors = []
    mi_accuracies = []
    
    for result in results_list:
        sigma_values.append(result.get("sigma", 0))
        privacy_scores.append(result.get("overall_privacy_score", 0))
        
        # Utility is typically measured by model accuracy
        # Here we use 1 - reconstruction_error as a proxy
        recon = result.get("reconstruction", {})
        privacy_scores.append(recon.get("privacy_score", 0))
        recon_errors.append(recon.get("normalized_error", 0))
        
        mi = result.get("membership_inference", {})
        mi_accuracies.append(mi.get("accuracy", 0.5))
    
    return {
        "sigma_values": sigma_values,
        "privacy_scores": privacy_scores,
        "reconstruction_errors": recon_errors,
        "membership_accuracies": mi_accuracies,
        "tradeoff_data": [
            {
                "sigma": s,
                "privacy": p,
                "reconstruction_error": r,
                "membership_accuracy": m
            }
            for s, p, r, m in zip(
                sigma_values, privacy_scores, recon_errors, mi_accuracies
            )
        ]
    }

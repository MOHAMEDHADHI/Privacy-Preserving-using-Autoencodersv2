import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from typing import Dict, Tuple
import json


class MLPClassifier(nn.Module):
    """Multi-Layer Perceptron for latent vector classification"""
    def __init__(self, input_dim: int, num_classes: int):
        super(MLPClassifier, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, num_classes)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x


class CNNClassifier(nn.Module):
    """CNN for 2D reshaped latent vector classification"""
    def __init__(self, input_channels: int, grid_size: int, num_classes: int):
        super(CNNClassifier, self).__init__()
        self.conv1 = nn.Conv2d(input_channels, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.relu = nn.ReLU()
        
        # Calculate flattened size after convolutions
        self.flat_size = 64 * (grid_size // 4) * (grid_size // 4)
        self.fc1 = nn.Linear(self.flat_size, 128)
        self.fc2 = nn.Linear(128, num_classes)
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, self.flat_size)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x


def reshape_to_2d(latent_vectors: np.ndarray) -> Tuple[np.ndarray, int]:
    """Reshape 1D latent vectors to 2D grid for CNN"""
    n_samples, latent_dim = latent_vectors.shape
    grid_size = int(np.ceil(np.sqrt(latent_dim)))
    padded_dim = grid_size * grid_size
    
    # Pad if necessary
    if latent_dim < padded_dim:
        padding = np.zeros((n_samples, padded_dim - latent_dim))
        latent_vectors = np.concatenate([latent_vectors, padding], axis=1)
    
    # Reshape to (n_samples, 1, grid_size, grid_size)
    reshaped = latent_vectors.reshape(n_samples, 1, grid_size, grid_size)
    return reshaped, grid_size


def train_model(model, train_loader, criterion, optimizer, device, epochs=20):
    """Train a PyTorch model"""
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
    return model


def evaluate_model(model, test_loader, device) -> Dict[str, float]:
    """Evaluate model and return metrics"""
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())
    
    accuracy = accuracy_score(all_labels, all_preds)
    precision = precision_score(all_labels, all_preds, average='weighted', zero_division=0)
    recall = recall_score(all_labels, all_preds, average='weighted', zero_division=0)
    f1 = f1_score(all_labels, all_preds, average='weighted', zero_division=0)
    
    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1)
    }


def train_mlp_classifier(latent_vectors: np.ndarray, labels: np.ndarray, sigma: float, dataset_id: int = None) -> Dict:
    """Train MLP classifier on latent vectors"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        latent_vectors, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    # Convert to tensors
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.LongTensor(y_train)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.LongTensor(y_test)
    
    # Create data loaders
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    # Initialize model
    input_dim = latent_vectors.shape[1]
    num_classes = len(np.unique(labels))
    model = MLPClassifier(input_dim, num_classes).to(device)
    
    # Train
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    model = train_model(model, train_loader, criterion, optimizer, device)
    
    # Evaluate
    metrics = evaluate_model(model, test_loader, device)
    metrics["sigma"] = sigma
    metrics["model_type"] = "MLP"
    
    # Save model if dataset_id provided
    if dataset_id is not None:
        from inference import save_model
        metadata = {
            "input_dim": input_dim,
            "num_classes": num_classes,
            "sigma": sigma,
            "model_type": "MLP",
            "dataset_id": dataset_id,
            "metrics": metrics
        }
        model_path = save_model(model, "MLP", dataset_id, metadata)
        metrics["model_path"] = model_path
    
    return metrics


def train_cnn_classifier(latent_vectors: np.ndarray, labels: np.ndarray, sigma: float, dataset_id: int = None) -> Dict:
    """Train CNN classifier on reshaped latent vectors"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Reshape to 2D
    latent_2d, grid_size = reshape_to_2d(latent_vectors)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        latent_2d, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    # Convert to tensors
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.LongTensor(y_train)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.LongTensor(y_test)
    
    # Create data loaders
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    
    # Initialize model
    num_classes = len(np.unique(labels))
    model = CNNClassifier(1, grid_size, num_classes).to(device)
    
    # Train
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    model = train_model(model, train_loader, criterion, optimizer, device)
    
    # Evaluate
    metrics = evaluate_model(model, test_loader, device)
    metrics["sigma"] = sigma
    metrics["model_type"] = "CNN"
    
    # Save model if dataset_id provided
    if dataset_id is not None:
        from inference import save_model
        metadata = {
            "input_dim": latent_vectors.shape[1],
            "num_classes": num_classes,
            "grid_size": grid_size,
            "sigma": sigma,
            "model_type": "CNN",
            "dataset_id": dataset_id,
            "metrics": metrics
        }
        model_path = save_model(model, "CNN", dataset_id, metadata)
        metrics["model_path"] = model_path
    
    return metrics

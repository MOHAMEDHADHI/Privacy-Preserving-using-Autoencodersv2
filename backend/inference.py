"""
Inference Module - Make predictions on new data
"""
import torch
import numpy as np
from pathlib import Path
from typing import Dict, List
import json
from classifiers import MLPClassifier, CNNClassifier, reshape_to_2d

# Directory to store trained models
MODELS_DIR = Path("trained_models")
MODELS_DIR.mkdir(exist_ok=True)


def save_model(model, model_type: str, dataset_id: int, metadata: Dict):
    """Save trained model to disk"""
    model_path = MODELS_DIR / f"{model_type}_{dataset_id}.pth"
    metadata_path = MODELS_DIR / f"{model_type}_{dataset_id}_metadata.json"
    
    # Save model weights
    torch.save(model.state_dict(), model_path)
    
    # Save metadata
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return str(model_path)


def load_model(model_type: str, dataset_id: int):
    """Load trained model from disk"""
    model_path = MODELS_DIR / f"{model_type}_{dataset_id}.pth"
    metadata_path = MODELS_DIR / f"{model_type}_{dataset_id}_metadata.json"
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    
    # Load metadata
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Initialize model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    if model_type == "MLP":
        model = MLPClassifier(
            metadata['input_dim'],
            metadata['num_classes']
        ).to(device)
    elif model_type == "CNN":
        model = CNNClassifier(
            1,  # input_channels
            metadata['grid_size'],
            metadata['num_classes']
        ).to(device)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Load weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    
    return model, metadata, device


def predict_single(
    latent_vector: np.ndarray,
    model_type: str,
    dataset_id: int,
    class_names: Dict[int, str] = None
) -> Dict:
    """
    Make prediction on a single latent vector
    
    Args:
        latent_vector: 1D numpy array of latent features
        model_type: "MLP" or "CNN"
        dataset_id: ID of the trained model
        class_names: Optional mapping of class indices to names
    
    Returns:
        Dictionary with prediction results
    """
    # Load model
    model, metadata, device = load_model(model_type, dataset_id)
    
    # Prepare input
    if model_type == "MLP":
        # MLP expects 1D vector
        input_tensor = torch.FloatTensor(latent_vector).unsqueeze(0).to(device)
    elif model_type == "CNN":
        # CNN expects 2D grid
        reshaped, _ = reshape_to_2d(latent_vector.reshape(1, -1))
        input_tensor = torch.FloatTensor(reshaped).to(device)
    
    # Make prediction
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidence, predicted_class = torch.max(probabilities, 1)
    
    # Convert to numpy
    predicted_class = int(predicted_class.cpu().numpy()[0])
    confidence = float(confidence.cpu().numpy()[0])
    all_probabilities = probabilities.cpu().numpy()[0].tolist()
    
    # Get class name
    if class_names and predicted_class in class_names:
        class_name = class_names[predicted_class]
    else:
        class_name = f"Class {predicted_class}"
    
    return {
        "predicted_class": predicted_class,
        "class_name": class_name,
        "confidence": confidence,
        "probabilities": {
            class_names.get(i, f"Class {i}") if class_names else f"Class {i}": prob
            for i, prob in enumerate(all_probabilities)
        },
        "model_type": model_type,
        "dataset_id": dataset_id
    }


def predict_batch(
    latent_vectors: np.ndarray,
    model_type: str,
    dataset_id: int,
    class_names: Dict[int, str] = None
) -> List[Dict]:
    """
    Make predictions on multiple latent vectors
    
    Args:
        latent_vectors: 2D numpy array (n_samples, latent_dim)
        model_type: "MLP" or "CNN"
        dataset_id: ID of the trained model
        class_names: Optional mapping of class indices to names
    
    Returns:
        List of prediction dictionaries
    """
    # Load model
    model, metadata, device = load_model(model_type, dataset_id)
    
    # Prepare input
    if model_type == "MLP":
        input_tensor = torch.FloatTensor(latent_vectors).to(device)
    elif model_type == "CNN":
        reshaped, _ = reshape_to_2d(latent_vectors)
        input_tensor = torch.FloatTensor(reshaped).to(device)
    
    # Make predictions
    with torch.no_grad():
        outputs = model(input_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        confidences, predicted_classes = torch.max(probabilities, 1)
    
    # Convert to numpy
    predicted_classes = predicted_classes.cpu().numpy()
    confidences = confidences.cpu().numpy()
    all_probabilities = probabilities.cpu().numpy()
    
    # Format results
    results = []
    for i in range(len(latent_vectors)):
        predicted_class = int(predicted_classes[i])
        confidence = float(confidences[i])
        probs = all_probabilities[i].tolist()
        
        # Get class name
        if class_names and predicted_class in class_names:
            class_name = class_names[predicted_class]
        else:
            class_name = f"Class {predicted_class}"
        
        results.append({
            "predicted_class": predicted_class,
            "class_name": class_name,
            "confidence": confidence,
            "probabilities": {
                class_names.get(j, f"Class {j}") if class_names else f"Class {j}": prob
                for j, prob in enumerate(probs)
            }
        })
    
    return results


def list_available_models() -> List[Dict]:
    """List all available trained models"""
    models = []
    
    for metadata_file in MODELS_DIR.glob("*_metadata.json"):
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        # Extract model info from filename
        filename = metadata_file.stem
        parts = filename.replace("_metadata", "").split("_")
        model_type = parts[0]
        dataset_id = int(parts[1])
        
        models.append({
            "model_type": model_type,
            "dataset_id": dataset_id,
            "metadata": metadata
        })
    
    return models


def get_model_info(model_type: str, dataset_id: int) -> Dict:
    """Get information about a specific model"""
    metadata_path = MODELS_DIR / f"{model_type}_{dataset_id}_metadata.json"
    
    if not metadata_path.exists():
        raise FileNotFoundError(f"Model not found: {model_type}_{dataset_id}")
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    return {
        "model_type": model_type,
        "dataset_id": dataset_id,
        "metadata": metadata,
        "model_path": str(MODELS_DIR / f"{model_type}_{dataset_id}.pth")
    }

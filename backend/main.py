from fastapi import FastAPI, Request, UploadFile, File, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import classifiers
import privacy_attacks
import inference
import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel

app = FastAPI(title="Privacy-Preserving ML Platform")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    datasets = db.query(models.Dataset).order_by(models.Dataset.created_at.desc()).limit(10).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "datasets": datasets})

@app.get("/upload", response_class=HTMLResponse)
async def upload(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Determine dataset type
    ext = Path(file.filename).suffix.lower()
    dataset_type = "csv" if ext == ".csv" else "excel" if ext in [".xlsx", ".xls"] else "unknown"
    
    # Save to database
    dataset = models.Dataset(
        user_id=None,  # No user authentication yet
        name=file.filename,
        file_path=str(file_path),
        dataset_type=dataset_type
    )
    db.add(dataset)
    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=303)


@app.get("/encoder-config", response_class=HTMLResponse)
async def encoder_config(request: Request):
    return templates.TemplateResponse("encoder_config.html", {"request": request})


@app.post("/upload_latent")
async def upload_latent(
    file: UploadFile = File(...),
    sigma: float = Form(1.0),
    db: Session = Depends(get_db)
):
    """
    Upload latent vectors (.npy file) and train both MLP and CNN classifiers
    Expected format: .npy file with shape (n_samples, latent_dim + 1) where last column is labels
    """
    try:
        # Read the uploaded .npy file
        content = await file.read()
        temp_path = UPLOAD_DIR / file.filename
        with open(temp_path, "wb") as f:
            f.write(content)
        
        # Load numpy array
        data = np.load(temp_path)
        
        # Validate shape
        if len(data.shape) != 2:
            raise HTTPException(status_code=400, detail="Invalid data shape. Expected 2D array.")
        
        # Split into vectors and labels (assuming last column is labels)
        latent_vectors = data[:, :-1]
        labels = data[:, -1].astype(int)
        
        # Create dataset entry
        dataset = models.Dataset(
            user_id=None,
            name=file.filename,
            file_path=str(temp_path),
            dataset_type="latent_vectors"
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)
        
        # Store latent vectors in database
        latent_entry = models.LatentVector(
            dataset_id=dataset.id,
            vector_data=json.dumps(latent_vectors.tolist()),
            labels=json.dumps(labels.tolist()),
            sigma=sigma
        )
        db.add(latent_entry)
        db.commit()
        
        # Train MLP Classifier
        mlp_metrics = classifiers.train_mlp_classifier(latent_vectors, labels, sigma, dataset.id)
        mlp_result = models.ModelResult(
            dataset_id=dataset.id,
            model_type="MLP",
            accuracy=mlp_metrics["accuracy"],
            precision=mlp_metrics["precision"],
            recall=mlp_metrics["recall"],
            f1_score=mlp_metrics["f1_score"],
            sigma=sigma,
            result_data=json.dumps(mlp_metrics)
        )
        db.add(mlp_result)
        
        # Train CNN Classifier
        cnn_metrics = classifiers.train_cnn_classifier(latent_vectors, labels, sigma, dataset.id)
        cnn_result = models.ModelResult(
            dataset_id=dataset.id,
            model_type="CNN",
            accuracy=cnn_metrics["accuracy"],
            precision=cnn_metrics["precision"],
            recall=cnn_metrics["recall"],
            f1_score=cnn_metrics["f1_score"],
            sigma=sigma,
            result_data=json.dumps(cnn_metrics)
        )
        db.add(cnn_result)
        
        db.commit()
        
        return JSONResponse({
            "status": "success",
            "dataset_id": dataset.id,
            "mlp_results": mlp_metrics,
            "cnn_results": cnn_metrics,
            "comparison": {
                "mlp_accuracy": mlp_metrics["accuracy"],
                "cnn_accuracy": cnn_metrics["accuracy"],
                "better_model": "MLP" if mlp_metrics["accuracy"] > cnn_metrics["accuracy"] else "CNN"
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing latent vectors: {str(e)}")


@app.get("/results/{dataset_id}")
async def get_results(dataset_id: int, db: Session = Depends(get_db)):
    """Get training results for a specific dataset"""
    results = db.query(models.ModelResult).filter(
        models.ModelResult.dataset_id == dataset_id
    ).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="No results found for this dataset")
    
    return JSONResponse({
        "dataset_id": dataset_id,
        "results": [
            {
                "id": r.id,
                "model_type": r.model_type,
                "accuracy": r.accuracy,
                "precision": r.precision,
                "recall": r.recall,
                "f1_score": r.f1_score,
                "sigma": r.sigma,
                "created_at": r.created_at.isoformat()
            }
            for r in results
        ]
    })


@app.get("/results")
async def get_all_results(db: Session = Depends(get_db)):
    """Get all training results with comparison"""
    results = db.query(models.ModelResult).order_by(
        models.ModelResult.created_at.desc()
    ).all()
    
    return JSONResponse({
        "total_results": len(results),
        "results": [
            {
                "id": r.id,
                "dataset_id": r.dataset_id,
                "model_type": r.model_type,
                "accuracy": r.accuracy,
                "precision": r.precision,
                "recall": r.recall,
                "f1_score": r.f1_score,
                "sigma": r.sigma,
                "created_at": r.created_at.isoformat()
            }
            for r in results
        ]
    })


@app.post("/evaluate_privacy/{dataset_id}")
async def evaluate_privacy(dataset_id: int, db: Session = Depends(get_db)):
    """
    Run privacy attacks on a dataset
    Performs reconstruction and membership inference attacks
    """
    try:
        # Get latent vectors from database
        latent_entry = db.query(models.LatentVector).filter(
            models.LatentVector.dataset_id == dataset_id
        ).first()
        
        if not latent_entry:
            raise HTTPException(status_code=404, detail="Latent vectors not found for this dataset")
        
        # Load latent vectors and labels
        latent_vectors = np.array(json.loads(latent_entry.vector_data))
        labels = np.array(json.loads(latent_entry.labels))
        sigma = latent_entry.sigma
        
        # Generate synthetic "original data" for reconstruction attack
        # In practice, this would be the actual original data
        # Here we simulate it with random data of appropriate dimensions
        original_data = np.random.randn(len(latent_vectors), latent_vectors.shape[1] * 2)
        
        # Run reconstruction attack
        print(f"Running reconstruction attack on dataset {dataset_id}...")
        recon_results = privacy_attacks.reconstruction_attack(
            latent_vectors, original_data, sigma
        )
        
        # Store reconstruction attack results
        recon_attack = models.PrivacyAttackResult(
            model_result_id=None,  # Not tied to specific model
            attack_type="reconstruction",
            success_rate=recon_results["success_rate"],
            details=json.dumps(recon_results)
        )
        db.add(recon_attack)
        
        # Run membership inference attack
        print(f"Running membership inference attack on dataset {dataset_id}...")
        mi_results = privacy_attacks.simulate_membership_attack_simple(
            latent_vectors, sigma
        )
        
        # Store membership inference attack results
        mi_attack = models.PrivacyAttackResult(
            model_result_id=None,
            attack_type="membership_inference",
            success_rate=mi_results["success_rate"],
            details=json.dumps(mi_results)
        )
        db.add(mi_attack)
        
        db.commit()
        
        # Calculate overall privacy score
        overall_privacy = (
            recon_results["privacy_score"] + mi_results["privacy_score"]
        ) / 2
        
        return JSONResponse({
            "status": "success",
            "dataset_id": dataset_id,
            "sigma": sigma,
            "reconstruction_attack": recon_results,
            "membership_inference_attack": mi_results,
            "overall_privacy_score": overall_privacy,
            "interpretation": {
                "privacy_level": "High" if overall_privacy > 0.7 else "Medium" if overall_privacy > 0.4 else "Low",
                "recommendation": "Good privacy protection" if overall_privacy > 0.7 else "Consider increasing sigma" if overall_privacy > 0.4 else "Privacy at risk - increase sigma significantly"
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating privacy: {str(e)}")


@app.get("/privacy_attacks/{dataset_id}")
async def get_privacy_attacks(dataset_id: int, db: Session = Depends(get_db)):
    """Get all privacy attack results for a dataset"""
    attacks = db.query(models.PrivacyAttackResult).filter(
        models.PrivacyAttackResult.model_result_id.in_(
            db.query(models.ModelResult.id).filter(
                models.ModelResult.dataset_id == dataset_id
            )
        )
    ).all()
    
    # Also get attacks not tied to specific models
    general_attacks = db.query(models.PrivacyAttackResult).filter(
        models.PrivacyAttackResult.model_result_id == None
    ).all()
    
    all_attacks = attacks + general_attacks
    
    return JSONResponse({
        "dataset_id": dataset_id,
        "total_attacks": len(all_attacks),
        "attacks": [
            {
                "id": a.id,
                "attack_type": a.attack_type,
                "success_rate": a.success_rate,
                "details": json.loads(a.details) if a.details else {},
                "created_at": a.created_at.isoformat()
            }
            for a in all_attacks
        ]
    })


@app.get("/privacy_tradeoff")
async def get_privacy_tradeoff(db: Session = Depends(get_db)):
    """
    Generate privacy-utility tradeoff data across all datasets
    """
    # Get all datasets with their results
    datasets = db.query(models.Dataset).filter(
        models.Dataset.dataset_type == "latent_vectors"
    ).all()
    
    tradeoff_data = []
    
    for dataset in datasets:
        # Get model results
        model_results = db.query(models.ModelResult).filter(
            models.ModelResult.dataset_id == dataset.id
        ).all()
        
        # Get privacy attacks
        attacks = db.query(models.PrivacyAttackResult).all()
        
        if model_results:
            # Calculate average utility (accuracy)
            avg_accuracy = np.mean([r.accuracy for r in model_results])
            sigma = model_results[0].sigma if model_results else 0
            
            # Get privacy scores from attacks
            recon_privacy = 0
            mi_privacy = 0
            
            for attack in attacks:
                details = json.loads(attack.details) if attack.details else {}
                if attack.attack_type == "reconstruction":
                    recon_privacy = details.get("privacy_score", 0)
                elif attack.attack_type == "membership_inference":
                    mi_privacy = details.get("privacy_score", 0)
            
            overall_privacy = (recon_privacy + mi_privacy) / 2 if (recon_privacy or mi_privacy) else 0
            
            tradeoff_data.append({
                "dataset_id": dataset.id,
                "dataset_name": dataset.name,
                "sigma": sigma,
                "utility": avg_accuracy,
                "privacy_score": overall_privacy,
                "reconstruction_privacy": recon_privacy,
                "membership_privacy": mi_privacy
            })
    
    return JSONResponse({
        "total_datasets": len(tradeoff_data),
        "tradeoff_data": sorted(tradeoff_data, key=lambda x: x["sigma"]),
        "summary": {
            "avg_utility": np.mean([d["utility"] for d in tradeoff_data]) if tradeoff_data else 0,
            "avg_privacy": np.mean([d["privacy_score"] for d in tradeoff_data]) if tradeoff_data else 0
        }
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# ============================================
# INFERENCE ENDPOINTS
# ============================================

class PredictionRequest(BaseModel):
    latent_vector: List[float]
    class_names: Optional[Dict[int, str]] = None


class BatchPredictionRequest(BaseModel):
    latent_vectors: List[List[float]]
    class_names: Optional[Dict[int, str]] = None


@app.post("/predict/{model_type}/{dataset_id}")
async def predict(
    model_type: str,
    dataset_id: int,
    request: PredictionRequest
):
    """
    Make prediction on a single latent vector
    
    Args:
        model_type: "MLP" or "CNN"
        dataset_id: ID of the trained model
        request: JSON body with latent_vector and optional class_names
    
    Returns:
        Prediction with confidence scores
    
    Example:
        POST /predict/MLP/21
        {
            "latent_vector": [0.23, -1.45, 0.87, ...],
            "class_names": {
                "0": "Low Risk",
                "1": "High Risk"
            }
        }
    """
    try:
        latent_vector = np.array(request.latent_vector)
        
        # Convert string keys to int if provided
        class_names = None
        if request.class_names:
            class_names = {int(k): v for k, v in request.class_names.items()}
        
        result = inference.predict_single(
            latent_vector,
            model_type,
            dataset_id,
            class_names
        )
        
        return JSONResponse(result)
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict_batch/{model_type}/{dataset_id}")
async def predict_batch(
    model_type: str,
    dataset_id: int,
    request: BatchPredictionRequest
):
    """
    Make predictions on multiple latent vectors
    
    Args:
        model_type: "MLP" or "CNN"
        dataset_id: ID of the trained model
        request: JSON body with latent_vectors and optional class_names
    
    Returns:
        List of predictions with confidence scores
    """
    try:
        latent_vectors = np.array(request.latent_vectors)
        
        # Convert string keys to int if provided
        class_names = None
        if request.class_names:
            class_names = {int(k): v for k, v in request.class_names.items()}
        
        results = inference.predict_batch(
            latent_vectors,
            model_type,
            dataset_id,
            class_names
        )
        
        return JSONResponse({"predictions": results})
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/models")
async def list_models():
    """List all available trained models"""
    try:
        models_list = inference.list_available_models()
        return JSONResponse({
            "total_models": len(models_list),
            "models": models_list
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing models: {str(e)}")


@app.get("/models/{model_type}/{dataset_id}")
async def get_model_info_endpoint(model_type: str, dataset_id: int):
    """Get information about a specific model"""
    try:
        info = inference.get_model_info(model_type, dataset_id)
        return JSONResponse(info)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting model info: {str(e)}")

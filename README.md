# Privacy-Preserving ML SaaS Platform

## Setup Instructions

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend runs on http://localhost:8000
Swagger docs: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm start
```
Frontend runs on http://localhost:3000

### Local Module
```bash
cd local_module
pip install -r requirements.txt
python dataset_loader.py
```

### Database
Ensure PostgreSQL is running:
- Database: privacy_ml
- User: postgres
- Password: postgres
- Port: 5432

## Features
- FastAPI backend with /health endpoint
- PostgreSQL with 5 tables (users, datasets, latent_vectors, model_results, privacy_attack_results)
- React frontend with Login, Register, Dashboard, Dataset Upload pages
- Local Python module for CSV/Excel/Image loading with basic preprocessing

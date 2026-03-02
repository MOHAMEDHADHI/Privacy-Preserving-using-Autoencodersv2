import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/Dashboard.css';

const API_BASE = 'http://localhost:8000';

function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [sigma, setSigma] = useState(1.0);
  const [selectedModels, setSelectedModels] = useState(['MLP', 'CNN']);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.name.endsWith('.npy')) {
        setFile(selectedFile);
        setError(null);
      } else {
        setError('Please select a .npy file');
        setFile(null);
      }
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith('.npy')) {
      setFile(droppedFile);
      setError(null);
    } else {
      setError('Please drop a .npy file');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const toggleModel = (model) => {
    if (selectedModels.includes(model)) {
      setSelectedModels(selectedModels.filter(m => m !== model));
    } else {
      setSelectedModels([...selectedModels, model]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    if (selectedModels.length === 0) {
      setError('Please select at least one model');
      return;
    }

    try {
      setUploading(true);
      setError(null);

      const formData = new FormData();
      formData.append('file', file);
      formData.append('sigma', sigma.toString());
      
      console.log('Uploading to:', `${API_BASE}/upload_latent`);
      console.log('File:', file.name, file.size);
      console.log('Sigma:', sigma);
      
      const response = await axios.post(
        `${API_BASE}/upload_latent`, 
        formData,
        {
          headers: {
            'Accept': 'application/json',
          },
          timeout: 60000, // 60 second timeout
        }
      );

      console.log('Upload response:', response.data);
      setResult(response.data);
      
      // Navigate to results after 2 seconds
      setTimeout(() => {
        navigate(`/results?dataset=${response.data.dataset_id}`);
      }, 2000);

    } catch (err) {
      console.error('Upload error:', err);
      console.error('Error details:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status
      });
      
      let errorMessage = 'Upload failed';
      if (err.code === 'ERR_NETWORK') {
        errorMessage = 'Network Error: Cannot connect to server. Please ensure backend is running on http://localhost:8000';
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <Sidebar />
      
      <div className="main-content">
        <div className="page-header">
          <h2>Upload Dataset</h2>
          <p>Upload latent vectors for privacy-preserving training</p>
        </div>

        {error && (
          <div className="alert alert-danger">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="alert alert-success">
            <span>✅</span>
            <div>
              <strong>Upload Successful!</strong>
              <p>Dataset ID: {result.dataset_id}</p>
              <p>Redirecting to results...</p>
            </div>
          </div>
        )}

        {/* File Upload */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">1. Select Latent Vectors File</h3>
          </div>
          <div className="card-body">
            <div
              className="file-upload"
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onClick={() => document.getElementById('file-input').click()}
            >
              <div className="file-upload-icon">📁</div>
              <div className="file-upload-text">
                {file ? file.name : 'Drop your .npy file here or click to browse'}
              </div>
              <div className="file-upload-hint">
                Expected format: (n_samples, latent_dim + 1) with labels in last column
              </div>
              <input
                id="file-input"
                type="file"
                accept=".npy"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
            </div>

            {file && (
              <div style={{ marginTop: '16px', padding: '12px', background: '#f9fafb', borderRadius: '8px' }}>
                <strong>Selected File:</strong> {file.name} ({(file.size / 1024).toFixed(2)} KB)
              </div>
            )}
          </div>
        </div>

        {/* Privacy Settings */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">2. Privacy Settings</h3>
          </div>
          <div className="card-body">
            <div className="form-group">
              <label className="form-label">
                Sigma (Privacy Parameter)
                <span style={{ marginLeft: '8px', color: '#6b7280', fontWeight: 'normal' }}>
                  Higher = More Privacy, Lower Utility
                </span>
              </label>
              
              <div className="slider-container">
                <input
                  type="range"
                  min="0"
                  max="3"
                  step="0.1"
                  value={sigma}
                  onChange={(e) => setSigma(parseFloat(e.target.value))}
                  className="slider"
                />
                <div className="slider-value">
                  <span>0.0 (Low Privacy)</span>
                  <span className="slider-current">σ = {sigma.toFixed(1)}</span>
                  <span>3.0 (High Privacy)</span>
                </div>
              </div>

              <div style={{ marginTop: '16px', padding: '12px', background: '#f9fafb', borderRadius: '8px' }}>
                <strong>Recommendation:</strong>
                {sigma < 0.5 && ' Very low privacy - High utility'}
                {sigma >= 0.5 && sigma < 1.0 && ' Low-Medium privacy - Good utility'}
                {sigma >= 1.0 && sigma < 1.5 && ' Medium privacy - Balanced'}
                {sigma >= 1.5 && sigma < 2.0 && ' Good privacy - Moderate utility'}
                {sigma >= 2.0 && ' High privacy - Lower utility'}
              </div>
            </div>
          </div>
        </div>

        {/* Model Selection */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">3. Select Models to Train</h3>
          </div>
          <div className="card-body">
            <div className="model-selection">
              <div
                className={`model-option ${selectedModels.includes('MLP') ? 'selected' : ''}`}
                onClick={() => toggleModel('MLP')}
              >
                <div className="model-option-icon">🧠</div>
                <div className="model-option-name">MLP Classifier</div>
                <div className="model-option-desc">
                  Multi-Layer Perceptron
                  <br />
                  Fast training, good for 1D data
                </div>
                {selectedModels.includes('MLP') && (
                  <div style={{ marginTop: '12px', color: '#10b981', fontWeight: 'bold' }}>
                    ✓ Selected
                  </div>
                )}
              </div>

              <div
                className={`model-option ${selectedModels.includes('CNN') ? 'selected' : ''}`}
                onClick={() => toggleModel('CNN')}
              >
                <div className="model-option-icon">🔲</div>
                <div className="model-option-name">CNN Classifier</div>
                <div className="model-option-desc">
                  Convolutional Neural Network
                  <br />
                  Captures spatial patterns
                </div>
                {selectedModels.includes('CNN') && (
                  <div style={{ marginTop: '12px', color: '#10b981', fontWeight: 'bold' }}>
                    ✓ Selected
                  </div>
                )}
              </div>

              <div
                className={`model-option ${selectedModels.length === 2 ? 'selected' : ''}`}
                onClick={() => setSelectedModels(['MLP', 'CNN'])}
              >
                <div className="model-option-icon">⚖️</div>
                <div className="model-option-name">Both Models</div>
                <div className="model-option-desc">
                  Train both and compare
                  <br />
                  Recommended for analysis
                </div>
                {selectedModels.length === 2 && (
                  <div style={{ marginTop: '12px', color: '#10b981', fontWeight: 'bold' }}>
                    ✓ Selected
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Upload Button */}
        <div className="card">
          <div className="card-body">
            <button
              className="btn btn-primary"
              onClick={handleUpload}
              disabled={!file || uploading || selectedModels.length === 0}
              style={{ width: '100%', padding: '16px', fontSize: '16px' }}
            >
              {uploading ? (
                <>
                  <div className="spinner" style={{ width: '20px', height: '20px', borderWidth: '2px' }}></div>
                  Uploading and Training...
                </>
              ) : (
                <>
                  🚀 Upload and Train Models
                </>
              )}
            </button>

            <div style={{ marginTop: '16px', textAlign: 'center', color: '#6b7280', fontSize: '14px' }}>
              Training typically takes 5-10 seconds per model
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Sidebar() {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <h1>🔒 PrivacyML</h1>
        <p>Privacy-Preserving Platform</p>
      </div>
      <ul className="sidebar-nav">
        <li>
          <a href="/" className="sidebar-nav-item">
            📊 Dashboard
          </a>
        </li>
        <li>
          <a href="/upload" className="sidebar-nav-item active">
            📤 Upload Dataset
          </a>
        </li>
        <li>
          <a href="/train" className="sidebar-nav-item">
            🚀 Train Models
          </a>
        </li>
        <li>
          <a href="/results" className="sidebar-nav-item">
            📈 Results
          </a>
        </li>
        <li>
          <a href="/privacy-evaluation" className="sidebar-nav-item">
            🔍 Privacy Evaluation
          </a>
        </li>
      </ul>
    </div>
  );
}

export default UploadPage;

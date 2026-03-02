import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, LineChart, Line, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import '../styles/Dashboard.css';

const API_BASE = 'http://localhost:8000';

function PrivacyEvaluationPage() {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [evaluating, setEvaluating] = useState(false);
  const [privacyResult, setPrivacyResult] = useState(null);
  const [attackHistory, setAttackHistory] = useState([]);
  const [tradeoffData, setTradeoffData] = useState([]);

  useEffect(() => {
    fetchDatasets();
    fetchTradeoffData();
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await axios.get(`${API_BASE}/results`);
      const results = response.data.results || [];
      const uniqueDatasets = [...new Set(results.map(r => r.dataset_id))];
      setDatasets(uniqueDatasets);
      if (uniqueDatasets.length > 0) {
        setSelectedDataset(uniqueDatasets[0]);
        fetchAttackHistory(uniqueDatasets[0]);
      }
    } catch (error) {
      console.error('Error fetching datasets:', error);
    }
  };

  const fetchAttackHistory = async (datasetId) => {
    try {
      const response = await axios.get(`${API_BASE}/privacy_attacks/${datasetId}`);
      setAttackHistory(response.data.attacks || []);
    } catch (error) {
      console.error('Error fetching attack history:', error);
    }
  };

  const fetchTradeoffData = async () => {
    try {
      const response = await axios.get(`${API_BASE}/privacy_tradeoff`);
      setTradeoffData(response.data.tradeoff_data || []);
    } catch (error) {
      console.error('Error fetching tradeoff data:', error);
    }
  };

  const runPrivacyEvaluation = async () => {
    if (!selectedDataset) return;

    try {
      setEvaluating(true);
      const response = await axios.post(`${API_BASE}/evaluate_privacy/${selectedDataset}`);
      setPrivacyResult(response.data);
      fetchAttackHistory(selectedDataset);
      fetchTradeoffData();
    } catch (error) {
      console.error('Error running privacy evaluation:', error);
      alert('Failed to run privacy evaluation');
    } finally {
      setEvaluating(false);
    }
  };

  const getPrivacyLevelColor = (level) => {
    switch (level) {
      case 'High': return 'success';
      case 'Medium': return 'warning';
      case 'Low': return 'danger';
      default: return 'info';
    }
  };

  return (
    <div className="dashboard-container">
      <Sidebar />
      
      <div className="main-content">
        <div className="page-header">
          <h2>Privacy Evaluation</h2>
          <p>Run privacy attacks and analyze privacy-utility tradeoffs</p>
        </div>

        {/* Dataset Selection */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Select Dataset for Evaluation</h3>
          </div>
          <div className="card-body">
            <div className="form-group">
              <label className="form-label">Dataset ID</label>
              <select
                className="form-select"
                value={selectedDataset || ''}
                onChange={(e) => {
                  const id = parseInt(e.target.value);
                  setSelectedDataset(id);
                  fetchAttackHistory(id);
                }}
              >
                {datasets.map(id => (
                  <option key={id} value={id}>
                    Dataset #{id}
                  </option>
                ))}
              </select>
            </div>

            <button
              className="btn btn-primary"
              onClick={runPrivacyEvaluation}
              disabled={!selectedDataset || evaluating}
            >
              {evaluating ? (
                <>
                  <div className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></div>
                  Running Privacy Attacks...
                </>
              ) : (
                <>
                  🔍 Run Privacy Evaluation
                </>
              )}
            </button>
          </div>
        </div>

        {/* Privacy Evaluation Results */}
        {privacyResult && (
          <>
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Overall Privacy Assessment</h3>
              </div>
              <div className="card-body">
                <div className="stats-grid">
                  <div className="stat-card">
                    <div className="stat-card-label">Overall Privacy Score</div>
                    <div className="stat-card-value">
                      {(privacyResult.overall_privacy_score * 100).toFixed(1)}%
                    </div>
                    <span className={`badge badge-${getPrivacyLevelColor(privacyResult.interpretation.privacy_level)}`}>
                      {privacyResult.interpretation.privacy_level} Privacy
                    </span>
                  </div>

                  <div className="stat-card">
                    <div className="stat-card-label">Sigma Value</div>
                    <div className="stat-card-value">{privacyResult.sigma.toFixed(1)}</div>
                    <div className="stat-card-change">Privacy parameter</div>
                  </div>

                  <div className="stat-card">
                    <div className="stat-card-label">Reconstruction Privacy</div>
                    <div className="stat-card-value">
                      {(privacyResult.reconstruction_attack.privacy_score * 100).toFixed(1)}%
                    </div>
                    <div className="stat-card-change">
                      Attack success: {(privacyResult.reconstruction_attack.success_rate * 100).toFixed(1)}%
                    </div>
                  </div>

                  <div className="stat-card">
                    <div className="stat-card-label">Membership Privacy</div>
                    <div className="stat-card-value">
                      {(privacyResult.membership_inference_attack.privacy_score * 100).toFixed(1)}%
                    </div>
                    <div className="stat-card-change">
                      Attack accuracy: {(privacyResult.membership_inference_attack.accuracy * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>

                <div className="alert alert-info" style={{ marginTop: '20px' }}>
                  <span>💡</span>
                  <div>
                    <strong>Recommendation:</strong>
                    <p>{privacyResult.interpretation.recommendation}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Attack Details */}
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Attack Details</h3>
              </div>
              <div className="card-body">
                <div className="comparison-card">
                  <div className="comparison-item">
                    <h4>🔓 Reconstruction Attack</h4>
                    <div className="comparison-value">
                      {(privacyResult.reconstruction_attack.privacy_score * 100).toFixed(1)}%
                    </div>
                    <div style={{ marginTop: '12px', fontSize: '14px', color: '#6b7280' }}>
                      <div>MSE: {privacyResult.reconstruction_attack.mse.toFixed(4)}</div>
                      <div>MAE: {privacyResult.reconstruction_attack.mae.toFixed(4)}</div>
                      <div>Normalized Error: {privacyResult.reconstruction_attack.normalized_error.toFixed(4)}</div>
                    </div>
                  </div>

                  <div className="comparison-item">
                    <h4>👥 Membership Inference Attack</h4>
                    <div className="comparison-value">
                      {(privacyResult.membership_inference_attack.privacy_score * 100).toFixed(1)}%
                    </div>
                    <div style={{ marginTop: '12px', fontSize: '14px', color: '#6b7280' }}>
                      <div>Accuracy: {(privacyResult.membership_inference_attack.accuracy * 100).toFixed(2)}%</div>
                      <div>AUC: {privacyResult.membership_inference_attack.auc.toFixed(4)}</div>
                      <div>Baseline: 50% (random guess)</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Privacy-Utility Tradeoff */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Privacy-Utility Tradeoff Analysis</h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={350}>
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="utility"
                  name="Utility"
                  label={{ value: 'Utility (Model Accuracy)', position: 'insideBottom', offset: -5 }}
                  domain={[0, 1]}
                />
                <YAxis
                  dataKey="privacy_score"
                  name="Privacy"
                  label={{ value: 'Privacy Score', angle: -90, position: 'insideLeft' }}
                  domain={[0, 1]}
                />
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div style={{
                          background: 'white',
                          padding: '12px',
                          border: '1px solid #e5e7eb',
                          borderRadius: '8px',
                          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                        }}>
                          <p><strong>Dataset #{data.dataset_id}</strong></p>
                          <p>Utility: {(data.utility * 100).toFixed(1)}%</p>
                          <p>Privacy: {(data.privacy_score * 100).toFixed(1)}%</p>
                          <p>Sigma: {data.sigma.toFixed(1)}</p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Legend />
                <Scatter
                  name="Datasets"
                  data={tradeoffData}
                  fill="#6366f1"
                  shape="circle"
                />
              </ScatterChart>
            </ResponsiveContainer>

            <div style={{ marginTop: '20px', padding: '16px', background: '#f9fafb', borderRadius: '8px' }}>
              <strong>Interpretation:</strong>
              <ul style={{ marginTop: '8px', marginLeft: '20px', color: '#6b7280' }}>
                <li>Top-right corner: High privacy AND high utility (ideal)</li>
                <li>Top-left corner: High privacy, low utility</li>
                <li>Bottom-right corner: Low privacy, high utility</li>
                <li>Bottom-left corner: Low privacy AND low utility (avoid)</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Attack History */}
        {attackHistory.length > 0 && (
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Attack History</h3>
            </div>
            <div className="card-body">
              <div className="table-container">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Attack Type</th>
                      <th>Success Rate</th>
                      <th>Privacy Score</th>
                      <th>Date</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {attackHistory.map((attack) => {
                      const details = attack.details;
                      const privacyScore = details.privacy_score || 0;
                      return (
                        <tr key={attack.id}>
                          <td>
                            <span className={`badge ${attack.attack_type === 'reconstruction' ? 'badge-warning' : 'badge-info'}`}>
                              {attack.attack_type === 'reconstruction' ? '🔓 Reconstruction' : '👥 Membership Inference'}
                            </span>
                          </td>
                          <td>{(attack.success_rate * 100).toFixed(2)}%</td>
                          <td>
                            <div className="progress-bar">
                              <div
                                className={`progress-bar-fill ${privacyScore > 0.7 ? 'success' : privacyScore > 0.4 ? 'warning' : 'danger'}`}
                                style={{ width: `${privacyScore * 100}%` }}
                              ></div>
                            </div>
                            {(privacyScore * 100).toFixed(1)}%
                          </td>
                          <td>{new Date(attack.created_at).toLocaleString()}</td>
                          <td>
                            <span className={`badge badge-${privacyScore > 0.7 ? 'success' : privacyScore > 0.4 ? 'warning' : 'danger'}`}>
                              {privacyScore > 0.7 ? 'High Privacy' : privacyScore > 0.4 ? 'Medium Privacy' : 'Low Privacy'}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
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
          <a href="/upload" className="sidebar-nav-item">
            📤 Upload Dataset
          </a>
        </li>
        <li>
          <a href="/results" className="sidebar-nav-item">
            📈 Results
          </a>
        </li>
        <li>
          <a href="/privacy-evaluation" className="sidebar-nav-item active">
            🔍 Privacy Evaluation
          </a>
        </li>
      </ul>
    </div>
  );
}

export default PrivacyEvaluationPage;

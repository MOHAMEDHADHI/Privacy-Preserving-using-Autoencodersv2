import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, LineChart, Line, RadarChart, Radar, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import '../styles/Dashboard.css';

const API_BASE = 'http://localhost:8000';

function ResultsPage() {
  const [results, setResults] = useState([]);
  const [filteredResults, setFilteredResults] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState('all');
  const [selectedModel, setSelectedModel] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchResults();
  }, []);

  useEffect(() => {
    filterResults();
  }, [selectedDataset, selectedModel, results]);

  const fetchResults = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/results`);
      setResults(response.data.results || []);
    } catch (error) {
      console.error('Error fetching results:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterResults = () => {
    let filtered = results;

    if (selectedDataset !== 'all') {
      filtered = filtered.filter(r => r.dataset_id === parseInt(selectedDataset));
    }

    if (selectedModel !== 'all') {
      filtered = filtered.filter(r => r.model_type === selectedModel);
    }

    setFilteredResults(filtered);
  };

  const getDatasets = () => {
    return [...new Set(results.map(r => r.dataset_id))];
  };

  const getMLPvsCNNComparison = () => {
    const datasets = getDatasets();
    return datasets.map(datasetId => {
      const datasetResults = results.filter(r => r.dataset_id === datasetId);
      const mlp = datasetResults.find(r => r.model_type === 'MLP');
      const cnn = datasetResults.find(r => r.model_type === 'CNN');

      return {
        dataset: `Dataset ${datasetId}`,
        MLP: mlp ? mlp.accuracy * 100 : 0,
        CNN: cnn ? cnn.accuracy * 100 : 0,
        sigma: mlp?.sigma || cnn?.sigma || 0
      };
    });
  };

  const getMetricsComparison = () => {
    if (filteredResults.length === 0) return [];

    const avgMetrics = filteredResults.reduce((acc, r) => {
      acc.accuracy += r.accuracy;
      acc.precision += r.precision;
      acc.recall += r.recall;
      acc.f1_score += r.f1_score;
      return acc;
    }, { accuracy: 0, precision: 0, recall: 0, f1_score: 0 });

    const count = filteredResults.length;
    return [
      { metric: 'Accuracy', value: (avgMetrics.accuracy / count) * 100 },
      { metric: 'Precision', value: (avgMetrics.precision / count) * 100 },
      { metric: 'Recall', value: (avgMetrics.recall / count) * 100 },
      { metric: 'F1 Score', value: (avgMetrics.f1_score / count) * 100 }
    ];
  };

  const getRadarData = () => {
    if (filteredResults.length === 0) return [];

    const mlpResults = filteredResults.filter(r => r.model_type === 'MLP');
    const cnnResults = filteredResults.filter(r => r.model_type === 'CNN');

    const avgMLP = mlpResults.length > 0 ? {
      accuracy: mlpResults.reduce((sum, r) => sum + r.accuracy, 0) / mlpResults.length * 100,
      precision: mlpResults.reduce((sum, r) => sum + r.precision, 0) / mlpResults.length * 100,
      recall: mlpResults.reduce((sum, r) => sum + r.recall, 0) / mlpResults.length * 100,
      f1: mlpResults.reduce((sum, r) => sum + r.f1_score, 0) / mlpResults.length * 100
    } : null;

    const avgCNN = cnnResults.length > 0 ? {
      accuracy: cnnResults.reduce((sum, r) => sum + r.accuracy, 0) / cnnResults.length * 100,
      precision: cnnResults.reduce((sum, r) => sum + r.precision, 0) / cnnResults.length * 100,
      recall: cnnResults.reduce((sum, r) => sum + r.recall, 0) / cnnResults.length * 100,
      f1: cnnResults.reduce((sum, r) => sum + r.f1_score, 0) / cnnResults.length * 100
    } : null;

    return [
      { metric: 'Accuracy', MLP: avgMLP?.accuracy || 0, CNN: avgCNN?.accuracy || 0 },
      { metric: 'Precision', MLP: avgMLP?.precision || 0, CNN: avgCNN?.precision || 0 },
      { metric: 'Recall', MLP: avgMLP?.recall || 0, CNN: avgCNN?.recall || 0 },
      { metric: 'F1 Score', MLP: avgMLP?.f1 || 0, CNN: avgCNN?.f1 || 0 }
    ];
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <Sidebar />
      
      <div className="main-content">
        <div className="page-header">
          <h2>Results Analytics</h2>
          <p>Analyze training results and model performance</p>
        </div>

        {/* Filters */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Filters</h3>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div className="form-group">
                <label className="form-label">Dataset</label>
                <select
                  className="form-select"
                  value={selectedDataset}
                  onChange={(e) => setSelectedDataset(e.target.value)}
                >
                  <option value="all">All Datasets</option>
                  {getDatasets().map(id => (
                    <option key={id} value={id}>Dataset #{id}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Model Type</label>
                <select
                  className="form-select"
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                >
                  <option value="all">All Models</option>
                  <option value="MLP">MLP Only</option>
                  <option value="CNN">CNN Only</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-card-label">Total Results</div>
            <div className="stat-card-value">{filteredResults.length}</div>
            <div className="stat-card-change">Filtered from {results.length} total</div>
          </div>

          <div className="stat-card">
            <div className="stat-card-label">Avg Accuracy</div>
            <div className="stat-card-value">
              {filteredResults.length > 0
                ? ((filteredResults.reduce((sum, r) => sum + r.accuracy, 0) / filteredResults.length) * 100).toFixed(1)
                : 0}%
            </div>
            <div className="stat-card-change">Across all models</div>
          </div>

          <div className="stat-card">
            <div className="stat-card-label">Best Model</div>
            <div className="stat-card-value">
              {filteredResults.length > 0
                ? filteredResults.reduce((best, r) => r.accuracy > best.accuracy ? r : best).model_type
                : 'N/A'}
            </div>
            <div className="stat-card-change">Highest accuracy</div>
          </div>

          <div className="stat-card">
            <div className="stat-card-label">Avg Sigma</div>
            <div className="stat-card-value">
              {filteredResults.length > 0
                ? (filteredResults.reduce((sum, r) => sum + r.sigma, 0) / filteredResults.length).toFixed(1)
                : 0}
            </div>
            <div className="stat-card-change">Privacy parameter</div>
          </div>
        </div>

        {/* MLP vs CNN Comparison */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">MLP vs CNN Accuracy Comparison</h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={getMLPvsCNNComparison()}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="dataset" />
                <YAxis label={{ value: 'Accuracy (%)', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="MLP" fill="#6366f1" />
                <Bar dataKey="CNN" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Metrics Radar Chart */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Performance Metrics Comparison</h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={350}>
              <RadarChart data={getRadarData()}>
                <PolarGrid />
                <PolarAngleAxis dataKey="metric" />
                <PolarRadiusAxis angle={90} domain={[0, 100]} />
                <Radar name="MLP" dataKey="MLP" stroke="#6366f1" fill="#6366f1" fillOpacity={0.6} />
                <Radar name="CNN" dataKey="CNN" stroke="#10b981" fill="#10b981" fillOpacity={0.6} />
                <Legend />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Detailed Results Table */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Detailed Results</h3>
          </div>
          <div className="card-body">
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Dataset</th>
                    <th>Model</th>
                    <th>Accuracy</th>
                    <th>Precision</th>
                    <th>Recall</th>
                    <th>F1 Score</th>
                    <th>Sigma</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredResults.map((result) => (
                    <tr key={result.id}>
                      <td>#{result.id}</td>
                      <td>#{result.dataset_id}</td>
                      <td>
                        <span className={`badge ${result.model_type === 'MLP' ? 'badge-info' : 'badge-success'}`}>
                          {result.model_type}
                        </span>
                      </td>
                      <td>
                        <div className="progress-bar">
                          <div
                            className="progress-bar-fill success"
                            style={{ width: `${result.accuracy * 100}%` }}
                          ></div>
                        </div>
                        {(result.accuracy * 100).toFixed(2)}%
                      </td>
                      <td>{(result.precision * 100).toFixed(2)}%</td>
                      <td>{(result.recall * 100).toFixed(2)}%</td>
                      <td>{(result.f1_score * 100).toFixed(2)}%</td>
                      <td>
                        <span className="badge badge-warning">{result.sigma.toFixed(1)}</span>
                      </td>
                      <td>{new Date(result.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
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
          <a href="/upload" className="sidebar-nav-item">
            📤 Upload Dataset
          </a>
        </li>
        <li>
          <a href="/results" className="sidebar-nav-item active">
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

export default ResultsPage;

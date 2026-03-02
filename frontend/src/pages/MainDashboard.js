import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import {
  LineChart, Line, BarChart, Bar, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import '../styles/Dashboard.css';

const API_BASE = 'http://localhost:8000';

function MainDashboard() {
  const [stats, setStats] = useState({
    totalDatasets: 0,
    totalModels: 0,
    avgAccuracy: 0,
    avgPrivacy: 0
  });
  const [recentResults, setRecentResults] = useState([]);
  const [tradeoffData, setTradeoffData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch results
      const resultsRes = await axios.get(`${API_BASE}/results`);
      const results = resultsRes.data.results || [];
      
      // Fetch tradeoff data
      const tradeoffRes = await axios.get(`${API_BASE}/privacy_tradeoff`);
      const tradeoff = tradeoffRes.data;
      
      // Calculate stats
      const uniqueDatasets = new Set(results.map(r => r.dataset_id)).size;
      const avgAcc = results.length > 0
        ? results.reduce((sum, r) => sum + r.accuracy, 0) / results.length
        : 0;
      
      setStats({
        totalDatasets: uniqueDatasets,
        totalModels: results.length,
        avgAccuracy: avgAcc,
        avgPrivacy: tradeoff.summary?.avg_privacy || 0
      });
      
      setRecentResults(results.slice(0, 10));
      setTradeoffData(tradeoff.tradeoff_data || []);
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
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
          <h2>Dashboard</h2>
          <p>Privacy-Preserving Machine Learning Platform</p>
        </div>

        {/* Stats Grid */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-card-header">
              <div>
                <div className="stat-card-label">Total Datasets</div>
                <div className="stat-card-value">{stats.totalDatasets}</div>
              </div>
              <div className="stat-card-icon primary">📊</div>
            </div>
            <div className="stat-card-change positive">
              ↑ Active experiments
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-card-header">
              <div>
                <div className="stat-card-label">Models Trained</div>
                <div className="stat-card-value">{stats.totalModels}</div>
              </div>
              <div className="stat-card-icon success">🤖</div>
            </div>
            <div className="stat-card-change positive">
              ↑ MLP & CNN classifiers
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-card-header">
              <div>
                <div className="stat-card-label">Avg Accuracy</div>
                <div className="stat-card-value">{(stats.avgAccuracy * 100).toFixed(1)}%</div>
              </div>
              <div className="stat-card-icon warning">🎯</div>
            </div>
            <div className="stat-card-change positive">
              ↑ Model performance
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-card-header">
              <div>
                <div className="stat-card-label">Privacy Score</div>
                <div className="stat-card-value">{(stats.avgPrivacy * 100).toFixed(1)}%</div>
              </div>
              <div className="stat-card-icon danger">🔒</div>
            </div>
            <div className="stat-card-change">
              Privacy protection level
            </div>
          </div>
        </div>

        {/* Privacy-Utility Tradeoff Chart */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Privacy-Utility Tradeoff</h3>
            <Link to="/privacy-evaluation" className="btn btn-outline">
              View Details →
            </Link>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={300}>
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="utility"
                  name="Utility (Accuracy)"
                  label={{ value: 'Utility', position: 'insideBottom', offset: -5 }}
                />
                <YAxis
                  dataKey="privacy_score"
                  name="Privacy Score"
                  label={{ value: 'Privacy', angle: -90, position: 'insideLeft' }}
                />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Legend />
                <Scatter
                  name="Datasets"
                  data={tradeoffData}
                  fill="#6366f1"
                />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Results */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Recent Training Results</h3>
            <Link to="/results" className="btn btn-outline">
              View All →
            </Link>
          </div>
          <div className="card-body">
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Dataset ID</th>
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
                  {recentResults.map((result) => (
                    <tr key={result.id}>
                      <td>#{result.dataset_id}</td>
                      <td>
                        <span className={`badge ${result.model_type === 'MLP' ? 'badge-info' : 'badge-success'}`}>
                          {result.model_type}
                        </span>
                      </td>
                      <td>{(result.accuracy * 100).toFixed(2)}%</td>
                      <td>{(result.precision * 100).toFixed(2)}%</td>
                      <td>{(result.recall * 100).toFixed(2)}%</td>
                      <td>{(result.f1_score * 100).toFixed(2)}%</td>
                      <td>{result.sigma.toFixed(1)}</td>
                      <td>{new Date(result.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Quick Actions</h3>
          </div>
          <div className="card-body">
            <div className="stats-grid">
              <Link to="/upload" className="stat-card" style={{ textDecoration: 'none' }}>
                <div className="stat-card-icon primary">📤</div>
                <div className="stat-card-label">Upload Dataset</div>
                <p style={{ fontSize: '14px', color: '#6b7280', marginTop: '8px' }}>
                  Upload latent vectors for training
                </p>
              </Link>

              <Link to="/train" className="stat-card" style={{ textDecoration: 'none' }}>
                <div className="stat-card-icon success">🚀</div>
                <div className="stat-card-label">Train Models</div>
                <p style={{ fontSize: '14px', color: '#6b7280', marginTop: '8px' }}>
                  Train MLP and CNN classifiers
                </p>
              </Link>

              <Link to="/privacy-evaluation" className="stat-card" style={{ textDecoration: 'none' }}>
                <div className="stat-card-icon warning">🔍</div>
                <div className="stat-card-label">Privacy Evaluation</div>
                <p style={{ fontSize: '14px', color: '#6b7280', marginTop: '8px' }}>
                  Run privacy attacks and analysis
                </p>
              </Link>

              <Link to="/results" className="stat-card" style={{ textDecoration: 'none' }}>
                <div className="stat-card-icon danger">📈</div>
                <div className="stat-card-label">View Results</div>
                <p style={{ fontSize: '14px', color: '#6b7280', marginTop: '8px' }}>
                  Analyze training and privacy results
                </p>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <h1>🔒 PrivacyML</h1>
        <p>Privacy-Preserving Platform</p>
        {user && (
          <div style={{ marginTop: '12px', padding: '8px', background: '#f9fafb', borderRadius: '6px', fontSize: '12px' }}>
            👤 {user.email}
          </div>
        )}
      </div>
      <ul className="sidebar-nav">
        <li>
          <Link to="/dashboard" className="sidebar-nav-item active">
            📊 Dashboard
          </Link>
        </li>
        <li>
          <Link to="/upload" className="sidebar-nav-item">
            📤 Upload Dataset
          </Link>
        </li>
        <li>
          <Link to="/results" className="sidebar-nav-item">
            📈 Results
          </Link>
        </li>
        <li>
          <Link to="/privacy-evaluation" className="sidebar-nav-item">
            🔍 Privacy Evaluation
          </Link>
        </li>
        <li style={{ marginTop: 'auto', paddingTop: '20px', borderTop: '1px solid #e5e7eb' }}>
          <button
            onClick={handleLogout}
            className="sidebar-nav-item"
            style={{
              width: '100%',
              textAlign: 'left',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: '#ef4444'
            }}
          >
            🚪 Logout
          </button>
        </li>
      </ul>
    </div>
  );
}

export default MainDashboard;

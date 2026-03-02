import React from 'react';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dashboard</h1>
      <button onClick={() => navigate('/upload')} style={{ padding: '10px 20px' }}>
        Upload Dataset
      </button>
      <div style={{ marginTop: '20px' }}>
        <h3>Recent Datasets</h3>
        <p>No datasets uploaded yet.</p>
      </div>
    </div>
  );
}

export default Dashboard;

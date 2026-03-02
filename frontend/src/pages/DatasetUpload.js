import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function DatasetUpload() {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Dataset uploaded successfully!');
    navigate('/dashboard');
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Upload Dataset</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ marginBottom: '10px' }}
        />
        <br />
        <button type="submit" style={{ padding: '10px 20px' }}>Upload</button>
        <button type="button" onClick={() => navigate('/dashboard')} style={{ padding: '10px 20px', marginLeft: '10px' }}>
          Cancel
        </button>
      </form>
    </div>
  );
}

export default DatasetUpload;

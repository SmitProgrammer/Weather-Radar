import React, { useState, useEffect, useCallback } from 'react';
import RadarMap from './components/RadarMap';
import Header from './components/Header';
import Legend from './components/Legend';
import './App.css';

function App() {
  const [radarData, setRadarData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL || '/api';

  const fetchRadarData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const url = `${API_URL}/radar/latest`;
      console.log('Fetching radar data from:', url);
      
      const response = await fetch(url);
      
      console.log('Response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response:', errorText);
        throw new Error(`Failed to fetch radar data (${response.status})`);
      }
      
      const data = await response.json();
      console.log('Radar data received:', data.metadata);
      setRadarData(data);
      setLastUpdate(new Date());
      
    } catch (err) {
      console.error('Error fetching radar data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [API_URL]);

  useEffect(() => {
    fetchRadarData();
    
    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchRadarData, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, [fetchRadarData]);

  return (
    <div className="App">
      <Header 
        lastUpdate={lastUpdate} 
        onRefresh={fetchRadarData}
        loading={loading}
      />
      
      <div className="main-content">
        {error && (
          <div className="error-banner">
            Error: {error}
          </div>
        )}
        
        <RadarMap 
          radarData={radarData} 
          loading={loading}
        />
        
        <Legend />
      </div>
    </div>
  );
}

export default App;

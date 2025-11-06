import React from 'react';
import './Header.css';

function Header({ lastUpdate, onRefresh, loading }) {
  const formatTime = (date) => {
    if (!date) return 'Never';
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <h1>🌦️ MRMS Weather Radar</h1>
          <p className="subtitle">Reflectivity at Lowest Altitude (RALA)</p>
        </div>
        
        <div className="header-right">
          <div className="update-info">
            <span className="label">Last Updated:</span>
            <span className="time">{formatTime(lastUpdate)}</span>
          </div>
          
          <button 
            className={`refresh-btn ${loading ? 'loading' : ''}`}
            onClick={onRefresh}
            disabled={loading}
          >
            {loading ? '⟳ Updating...' : '🔄 Refresh'}
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;

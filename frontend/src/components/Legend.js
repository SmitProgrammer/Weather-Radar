import React from 'react';
import './Legend.css';

function Legend() {
  const legendItems = [
    { color: '#04e9e7', range: '65+', label: 'Extreme' },
    { color: '#019ff4', range: '55-64', label: 'Very Heavy' },
    { color: '#0300f4', range: '45-54', label: 'Heavy' },
    { color: '#02fd02', range: '35-44', label: 'Moderate' },
    { color: '#01c501', range: '25-34', label: 'Light' },
    { color: '#008e00', range: '15-24', label: 'Very Light' },
    { color: '#ffff00', range: '5-14', label: 'Minimal' }
  ];

  return (
    <div className="legend">
      <div className="legend-title">Reflectivity (dBZ)</div>
      <div className="legend-items">
        {legendItems.map((item, index) => (
          <div key={index} className="legend-item">
            <div 
              className="legend-color" 
              style={{ backgroundColor: item.color }}
            ></div>
            <div className="legend-info">
              <span className="legend-range">{item.range}</span>
              <span className="legend-label">{item.label}</span>
            </div>
          </div>
        ))}
      </div>
      <div className="legend-note">
        Data updates every 2 minutes from MRMS
      </div>
    </div>
  );
}

export default Legend;

import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, CircleMarker, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './RadarMap.css';

// Component to update map when data changes
function RadarDataLayer({ radarData }) {
  const map = useMap();

  useEffect(() => {
    if (radarData && radarData.features && radarData.features.length > 0) {
      // Get bounds of radar data
      const lats = radarData.features.map(f => f.geometry.coordinates[1]);
      const lons = radarData.features.map(f => f.geometry.coordinates[0]);
      
      const minLat = Math.min(...lats);
      const maxLat = Math.max(...lats);
      const minLon = Math.min(...lons);
      const maxLon = Math.max(...lons);
      
      // Fit map to data bounds
      map.fitBounds([
        [minLat, minLon],
        [maxLat, maxLon]
      ], { padding: [50, 50] });
    }
  }, [radarData, map]);

  return null;
}

// Function to get color based on reflectivity value
function getReflectivityColor(dbz) {
  if (dbz >= 65) return '#04e9e7';      // Extreme
  if (dbz >= 55) return '#019ff4';      // Very Heavy
  if (dbz >= 45) return '#0300f4';      // Heavy
  if (dbz >= 35) return '#02fd02';      // Moderate
  if (dbz >= 25) return '#01c501';      // Light
  if (dbz >= 15) return '#008e00';      // Very Light
  if (dbz >= 5) return '#ffff00';       // Minimal
  return '#cccccc';                      // Below threshold
}

function RadarMap({ radarData, loading }) {
  const mapRef = useRef(null);

  // Default center (US)
  const defaultCenter = [39.8283, -98.5795];
  const defaultZoom = 5;

  return (
    <div className="radar-map-container">
      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <p>Loading radar data...</p>
        </div>
      )}
      
      <MapContainer
        center={defaultCenter}
        zoom={defaultZoom}
        style={{ width: '100%', height: '100%' }}
        ref={mapRef}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {radarData && <RadarDataLayer radarData={radarData} />}
        
        {radarData && radarData.features && radarData.features.map((feature, index) => {
          const [lon, lat] = feature.geometry.coordinates;
          const reflectivity = feature.properties.reflectivity;
          const color = getReflectivityColor(reflectivity);
          
          return (
            <CircleMarker
              key={`radar-${index}`}
              center={[lat, lon]}
              radius={6}
              fillColor={color}
              fillOpacity={0.8}
              stroke={false}
            />
          );
        })}
      </MapContainer>
      
      {radarData && radarData.metadata && (
        <div className="map-info">
          <span className="data-timestamp">
            Data Time: {new Date(radarData.metadata.timestamp).toLocaleString()}
          </span>
          <span className="data-count">
            {radarData.metadata.count?.toLocaleString()} data points
          </span>
        </div>
      )}
    </div>
  );
}

export default RadarMap;

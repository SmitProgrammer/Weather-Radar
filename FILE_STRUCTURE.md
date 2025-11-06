# File Structure and Purpose

## Root Directory

```
Weather Radar/
│
├── README.md                 Main project documentation
├── QUICKSTART.md            Fast setup guide for local development
├── DEPLOYMENT.md            Render.com deployment instructions
├── PROJECT_SUMMARY.md       Complete project overview and summary
├── .gitignore               Git ignore patterns
│
├── backend/                 Python Flask API
│   ├── app.py              Main Flask application with API endpoints
│   ├── mrms_service.py     MRMS data fetching and processing logic
│   ├── test_mrms.py        Test script to verify MRMS functionality
│   ├── requirements.txt    Python package dependencies
│   ├── Dockerfile          Docker configuration for deployment
│   ├── Procfile            Render.com/Heroku deployment config
│   ├── runtime.txt         Python version specification
│   ├── start.bat           Windows batch script to start server
│   ├── .env                Environment variables (local dev)
│   ├── .env.example        Example environment variables
│   ├── .gitignore          Backend-specific ignore patterns
│   └── cache/              Directory for cached radar data (auto-created)
│
└── frontend/               React web application
    ├── package.json        Node.js dependencies and scripts
    ├── start.bat           Windows batch script to start frontend
    ├── .env                Environment variables (local dev)
    ├── .env.example        Example environment variables
    ├── .gitignore          Frontend-specific ignore patterns
    │
    ├── public/             Static assets
    │   └── index.html      HTML template with Leaflet CSS
    │
    └── src/                React source code
        ├── index.js        React entry point
        ├── index.css       Global styles
        ├── App.js          Main application component
        ├── App.css         App component styles
        │
        └── components/     React components
            ├── Header.js       Top navigation bar with refresh
            ├── Header.css      Header styles
            ├── RadarMap.js     Leaflet map with radar overlay
            ├── RadarMap.css    Map styles
            ├── Legend.js       Color scale legend
            └── Legend.css      Legend styles
```

## File Purposes

### Documentation Files

- **README.md**: Main project overview, features, architecture, setup instructions
- **QUICKSTART.md**: Fast-track setup guide for local development on Windows
- **DEPLOYMENT.md**: Step-by-step deployment guide for Render.com
- **PROJECT_SUMMARY.md**: Comprehensive project summary with all decisions and features

### Backend Files

- **app.py**: Flask web server with REST API endpoints (/api/health, /api/radar/latest, /api/radar/info)
- **mrms_service.py**: Core logic for downloading MRMS GRIB2 files, processing with cfgrib/xarray, converting to GeoJSON
- **test_mrms.py**: Standalone test script to verify MRMS data fetching works
- **requirements.txt**: Python dependencies (Flask, xarray, cfgrib, numpy, etc.)
- **Dockerfile**: Docker container configuration with eccodes library
- **Procfile**: Deployment configuration for Render.com/Heroku
- **runtime.txt**: Specifies Python 3.11.0 for deployment
- **start.bat**: Windows helper script to start backend server
- **.env**: Local development environment variables (PORT, FLASK_ENV)

### Frontend Files

- **package.json**: Node.js project config with React, Leaflet, axios dependencies
- **public/index.html**: Main HTML template with Leaflet CSS CDN link
- **src/index.js**: React app initialization and rendering
- **src/App.js**: Main component managing state, data fetching, and layout
- **src/components/Header.js**: Top bar with title, timestamp, and refresh button
- **src/components/RadarMap.js**: Leaflet map component with radar data visualization
- **src/components/Legend.js**: Color scale legend for reflectivity values
- **start.bat**: Windows helper script to start frontend dev server
- **.env**: Local development environment variable (REACT_APP_API_URL)

## Key Features by File

### Backend (mrms_service.py)
- Downloads latest MRMS RALA GRIB2 files
- Parses GRIB2 with xarray/cfgrib
- Extracts lat/lon/reflectivity arrays
- Samples data for performance (every 3rd point)
- Converts to GeoJSON FeatureCollection
- Implements 5-minute caching
- Handles MRMS server errors gracefully

### Frontend (RadarMap.js)
- Renders Leaflet map with OpenStreetMap tiles
- Displays radar data as colored CircleMarkers
- Auto-fits map bounds to data extent
- Color codes reflectivity (yellow → green → blue → cyan)
- Shows popup on marker click with dBZ value
- Displays data timestamp and point count

### Styling
- Professional gradient header (blue tones)
- Responsive design (desktop + mobile)
- Loading states with spinner animation
- Clean legend with color swatches
- Error banners for failed requests
- Smooth transitions and hover effects

## Data Flow

1. User opens frontend → App.js loads
2. useEffect triggers fetchRadarData()
3. Fetches from /api/radar/latest
4. Backend (app.py) calls mrms_service.get_latest_radar_data()
5. MRMS service checks cache → if stale, downloads new GRIB2
6. Processes GRIB2 → converts to GeoJSON
7. Returns to frontend → RadarMap.js renders on Leaflet map
8. Auto-refreshes every 5 minutes

## Environment Variables

### Backend (.env)
- PORT: Server port (default 5000)
- FLASK_ENV: development/production

### Frontend (.env)
- REACT_APP_API_URL: Backend API URL
  - Local: http://localhost:5000/api
  - Production: https://your-backend.onrender.com/api

## Scripts

### Start Backend (Windows)
```cmd
cd backend
start.bat
```

### Start Frontend (Windows)
```cmd
cd frontend
start.bat
```

### Test Backend
```cmd
cd backend
python test_mrms.py
```

## Deployment Files

### For Render.com Backend
- Dockerfile (recommended for eccodes support)
- Procfile (alternative to Docker)
- runtime.txt (Python version)

### For Render.com Frontend
- package.json (build: npm run build)
- .env with production REACT_APP_API_URL

## Auto-Generated/Runtime Files

- backend/cache/ - Cached GeoJSON radar data
- backend/sample_radar_data.json - Test output
- frontend/node_modules/ - Node dependencies
- frontend/build/ - Production build output
- backend/__pycache__/ - Python bytecode

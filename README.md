# Weather Radar Display

A full-stack application that displays live MRMS (Multi-Radar/Multi-Sensor System) weather radar data on an interactive map.

## Features

- **Real-time MRMS Data**: Processes Reflectivity at Lowest Altitude (RALA) data directly from NOAA
- **Interactive Map**: Built with React and Leaflet for smooth navigation
- **Auto-refresh**: Updates every 5 minutes to show latest radar data
- **Color-coded Visualization**: Reflectivity values displayed with standard weather radar colors
- **Responsive Design**: Works on desktop and mobile devices

## Architecture

### Backend (Python/Flask)
- Fetches MRMS GRIB2 files from NOAA servers
- Processes radar data using xarray and cfgrib
- Converts to GeoJSON format for frontend consumption
- Implements caching to reduce server load

### Frontend (React)
- Interactive map using Leaflet
- Displays radar data with color-coded markers
- Shows timestamp and data freshness
- Clean, functional UI

## Libraries Used

### Backend
- **Flask**: Web framework
- **cfgrib/xarray**: GRIB2 file parsing (MRMS native format - implementing a parser from scratch would take weeks)
- **numpy**: Efficient array processing for radar data
- **requests**: HTTP client for downloading data

### Frontend
- **React**: UI framework
- **Leaflet/react-leaflet**: Interactive maps (allowed as per requirements)
- **axios**: HTTP client (could be replaced with fetch, but axios provides better error handling)

## Local Development

### Prerequisites
- Python 3.9+
- Node.js 16+
- Docker (recommended for Windows to handle eccodes)

#### Installing eccodes (for GRIB2 support)

**Note**: eccodes installation on Windows with pip can be challenging. We recommend using Docker for local development and deployment.

**Windows (Recommended - Use Docker):**
```cmd
REM Use the provided Dockerfile for both local dev and deployment
cd backend
docker build -t weather-radar-backend .
docker run -p 5000:5000 weather-radar-backend
```

**Linux:**
```bash
sudo apt-get install libeccodes-dev
```

**macOS:**
```bash
brew install eccodes
```

### Backend Setup

**Option 1: Using Docker (Recommended for Windows)**

```cmd
cd backend

REM Build Docker image
docker build -t weather-radar-backend .

REM Run container
docker run -p 5000:5000 weather-radar-backend
```

**Option 2: Using Python venv (Linux/Mac or if eccodes already installed)**

```cmd
cd backend

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
REM Windows:
venv\Scripts\activate
REM Linux/Mac:
source venv/bin/activate

REM Install dependencies
pip install -r requirements.txt

REM Create cache directory
mkdir cache

REM Run the server
python app.py
```

The backend will run on http://localhost:5000

### Frontend Setup

```cmd
cd frontend

REM Install dependencies
npm install

REM Start development server
npm start
```

The frontend will run on http://localhost:3000

## Deployment on Render.com

### Backend Deployment

1. Create a new **Web Service** on Render.com
2. Connect your GitHub repository
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment Variables**: 
     - `PYTHON_VERSION`: `3.11.0`

### Frontend Deployment

1. Create a new **Static Site** on Render.com
2. Connect your GitHub repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
   - **Environment Variables**:
     - `REACT_APP_API_URL`: `https://your-backend-url.onrender.com/api`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/radar/latest` - Get latest radar data (GeoJSON)
- `GET /api/radar/info` - Get service information and cache status

## Data Source

MRMS (Multi-Radar/Multi-Sensor System) via AWS Open Data
- Source: https://noaa-mrms-pds.s3.amazonaws.com (AWS S3 Public Bucket)
- Original NOAA MRMS: https://mrms.ncep.noaa.gov/
- Product: Reflectivity at Lowest Altitude (RALA)
- Update Frequency: Every 2 minutes
- Format: GRIB2 (gzip compressed on S3)
- Coverage: CONUS (Continental US)

**Note**: Direct access to NOAA MRMS servers is restricted. We use the publicly accessible AWS S3 mirror provided through the NOAA Open Data Dissemination (NODD) program.

## License

MIT

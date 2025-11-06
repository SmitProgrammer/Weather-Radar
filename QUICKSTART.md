# Quick Start Guide

## Testing Locally (Windows)

### Quick Setup (Automated)

```cmd
REM Run the automated setup script
setup.bat
```

This will:
1. Create Python virtual environment in `backend/venv`
2. Install all Python dependencies
3. Install all Node.js dependencies
4. Create .env files from templates

### Manual Setup (Step-by-Step)

### Step 1: Set Up Backend

```cmd
cd backend

REM Run backend setup script
setup.bat
```

Or manually:

```cmd
cd backend

REM Create Python virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Create cache directory
mkdir cache

REM Run the backend
python app.py
```

**Important Note about eccodes on Windows:**

If `pip install` fails on cfgrib/eccodes, you have two options:

**Option A: Use Docker (Recommended)**
```cmd
cd backend
docker build -t weather-radar-backend .
docker run -p 5000:5000 weather-radar-backend
```

**Option B: Skip backend testing locally**
Deploy directly to Render.com using Docker (which handles eccodes automatically).

### Step 2: Set Up Frontend

Open a NEW command prompt:

```cmd
cd frontend

REM Run frontend setup script
setup.bat
```

Or manually:

```cmd
cd frontend

REM Install dependencies
npm install

REM Start development server
npm start
```

Frontend runs at: http://localhost:3000

Backend must be running at: http://localhost:5000

### Step 3: Test the Application

1. Open http://localhost:3000 in your browser
2. Wait for radar data to load (may take 30-60 seconds on first load)
3. You should see:
   - A map of the US
   - Colored dots representing radar reflectivity
   - A legend in the bottom-right
   - A refresh button in the header

### Troubleshooting

**Backend won't start:**
- Check if eccodes/cfgrib installed properly
- Check Python version: `python --version` (should be 3.9+)
- If eccodes install fails, see note below about Docker deployment

**Frontend shows "Failed to fetch":**
- Make sure backend is running on port 5000
- Check backend console for errors
- Try accessing http://localhost:5000/api/health directly

**No radar data displayed:**
- This is normal if there's no active weather
- The MRMS server might be temporarily unavailable
- Check backend console for download errors
- Data is cached for 5 minutes - try refreshing after cache expires

**Slow loading:**
- First download of GRIB2 file can take 30-60 seconds
- Subsequent loads use cache (5 min cache duration)
- Processing large GRIB files takes time

### Note on eccodes for Windows

Installing eccodes on Windows with regular Python can be challenging. If you encounter issues:

**Recommended approach for local testing:**
1. Use Docker with the provided `Dockerfile` (easiest)
2. Deploy to Render.com using Docker (handles eccodes automatically)

**Docker local testing:**
```cmd
cd backend
docker build -t weather-radar-backend .
docker run -p 5000:5000 weather-radar-backend
```

Then proceed with frontend setup normally.

## Next Steps

Once local testing works:
1. Push code to GitHub
2. Follow DEPLOYMENT.md for Render.com setup
3. Monitor backend logs during first deployment

## Development Tips

**Backend:**
- Edit `mrms_service.py` to change cache duration or data sampling
- Check `cache/latest_radar.json` to see processed data
- Add `print()` statements for debugging

**Frontend:**
- Changes auto-reload in development mode
- Use browser DevTools to inspect network requests
- Check Console for React errors

**Testing API directly:**
```cmd
REM Health check
curl http://localhost:5000/api/health

REM Get radar data
curl http://localhost:5000/api/radar/latest

REM Get service info
curl http://localhost:5000/api/radar/info
```

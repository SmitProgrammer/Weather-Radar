# Troubleshooting Guide

Common issues and solutions for the Weather Radar application.

## Backend Issues

### "ModuleNotFoundError: No module named 'eccodes'"

**Problem**: cfgrib requires the eccodes C library.

**Note**: Installing eccodes on Windows with regular Python is challenging.

**Solution 1 - Use Docker (Recommended)**:
```cmd
cd backend
docker build -t weather-radar-backend .
docker run -p 5000:5000 weather-radar-backend
```

**Solution 2 - Try pip install (may not work)**:
```cmd
pip install eccodes cfgrib
```

**Solution 3 - Deploy to Render.com**:
Use Docker deployment on Render.com (see DEPLOYMENT.md). The Dockerfile includes eccodes installation.

**For Linux/Mac users**:

Linux:
```bash
sudo apt-get install libeccodes-dev
pip install cfgrib
```

macOS:
```bash
brew install eccodes
pip install cfgrib
```

### "ModuleNotFoundError: No module named 'flask'"

**Problem**: Dependencies not installed or virtual environment not activated.

**Solution**:
```cmd
cd backend

REM Make sure virtual environment is activated
venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt
```

### "Error downloading file: 404"

**Problem**: MRMS file URL not found.

**Reasons**:
1. MRMS server temporarily down
2. File naming convention changed
3. Network connectivity issues

**Solution**:
1. Wait a few minutes and try again
2. Check https://mrms.ncep.noaa.gov/ is accessible
3. Check backend logs for exact URL being requested
4. MRMS updates every 2 minutes, old files get deleted

### "KeyError: 'unknown'" or GRIB parsing errors

**Problem**: GRIB file structure different than expected.

**Solution**:
1. Check the GRIB variable names:
   ```python
   import xarray as xr
   ds = xr.open_dataset('file.grib2', engine='cfgrib')
   print(ds.data_vars)  # See what variables exist
   ```
2. Update `mrms_service.py` to handle the correct variable name

### "MemoryError" or "Process killed"

**Problem**: GRIB file too large for available memory.

**Solution**:
1. Increase sampling rate in `mrms_service.py`:
   ```python
   step = 5  # Change from 3 to 5 or higher
   ```
2. Process smaller region only
3. Upgrade server resources

### Backend runs but returns 500 errors

**Problem**: Runtime error in code.

**Solution**:
1. Check backend console for Python stack trace
2. Look at the exact error message
3. Common issues:
   - Cache directory not writable
   - GRIB file corrupted
   - Network timeout

**Debug mode**:
```python
# In app.py, enable debug mode
app.run(debug=True)
```

## Frontend Issues

### "Module not found: Can't resolve 'leaflet'"

**Problem**: Dependencies not installed.

**Solution**:
```cmd
cd frontend
npm install
```

### Map displays but no radar data

**Problem**: Backend not reachable or returning errors.

**Solution**:
1. Check browser console (F12 → Console tab)
2. Check Network tab for failed requests
3. Verify backend is running: http://localhost:5000/api/health
4. Check CORS is enabled in backend
5. Verify `.env` has correct `REACT_APP_API_URL`

### "Failed to fetch radar data"

**Problem**: Network error or backend offline.

**Solution**:
1. Verify backend URL in `.env`:
   ```
   REACT_APP_API_URL=http://localhost:5000/api
   ```
2. Restart frontend after changing `.env`:
   ```cmd
   # Stop with Ctrl+C
   npm start
   ```
3. Check backend is running and accessible
4. Clear browser cache

### Map tiles not loading (gray squares)

**Problem**: OpenStreetMap unreachable or blocked.

**Solution**:
1. Check internet connection
2. Try different tile provider in `RadarMap.js`:
   ```jsx
   <TileLayer
     url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
   />
   ```
3. Check browser console for tile loading errors

### Markers not displaying

**Problem**: Data format incorrect or coordinates invalid.

**Solution**:
1. Check browser console for errors
2. Verify data in backend:
   ```
   http://localhost:5000/api/radar/latest
   ```
3. Check GeoJSON structure has:
   - `type: "FeatureCollection"`
   - `features` array
   - Each feature has `geometry.coordinates`

### "npm: command not found"

**Problem**: Node.js not installed.

**Solution**:
1. Download Node.js from https://nodejs.org/
2. Install LTS version
3. Restart terminal
4. Verify: `node --version`

## Deployment Issues (Render.com)

### Backend deployment fails on "pip install"

**Problem**: eccodes not available.

**Solution**: Use Docker deployment instead:
1. In Render, select "Docker" instead of "Python"
2. Render will use the `Dockerfile` which installs eccodes
3. Set environment: `PORT=10000` (or whatever Render assigns)

### "Application failed to respond"

**Problem**: App not binding to correct port.

**Solution**:
1. Ensure `app.py` uses environment PORT:
   ```python
   port = int(os.environ.get('PORT', 5000))
   ```
2. Check Render logs for errors
3. Verify start command: `gunicorn app:app`

### Frontend shows "Failed to fetch" on deployed site

**Problem**: CORS or incorrect API URL.

**Solution**:
1. Check `REACT_APP_API_URL` in Render environment variables
2. Should be: `https://your-backend.onrender.com/api` (no trailing slash)
3. Verify CORS enabled in backend `app.py`
4. Rebuild frontend after changing env vars

### Backend timeout errors

**Problem**: MRMS download takes too long.

**Solution**:
1. Increase gunicorn timeout in Procfile:
   ```
   web: gunicorn app:app --timeout 120
   ```
2. Increase cache duration to reduce downloads
3. Consider pre-downloading files in background

### Site works but is very slow

**Problem**: Free tier limitations.

**Reasons**:
1. Server spun down (cold start = 30-60 sec)
2. MRMS download slow
3. Large GRIB file processing

**Solutions**:
1. Use a ping service to keep backend alive
2. Increase cache duration
3. Reduce data sampling
4. Upgrade to paid tier

## Data Issues

### No radar data showing

**Problem**: Clear weather or data not available.

**Possible reasons**:
1. No active precipitation in coverage area
2. MRMS server maintenance
3. All reflectivity values below threshold (< 5 dBZ)

**Verify**:
1. Check https://mrms.ncep.noaa.gov/ directly
2. Look at NOAA radar: https://radar.weather.gov/
3. Try during known active weather

### Data seems outdated

**Problem**: Cache not refreshing.

**Solution**:
1. Wait for cache to expire (5 minutes)
2. Click refresh button manually
3. Clear backend cache:
   ```cmd
   # Delete cache file
   rm backend/cache/latest_radar.json
   ```

### Wrong geographic area

**Problem**: Map not centering on data.

**Solution**:
1. Wait for data to load fully
2. Map auto-fits to data bounds
3. Manually zoom/pan to desired area
4. MRMS covers CONUS (Continental US) only

## Performance Issues

### Browser freezes with many markers

**Problem**: Too many DOM elements.

**Solution**: Increase sampling in `mrms_service.py`:
```python
step = 5  # Reduce number of points
```

### Slow initial load

**Problem**: First GRIB download and processing.

**Expected behavior**: 
- First load: 30-60 seconds
- Cached loads: 1-2 seconds

**Not a bug** if first load is slow.

## Development Issues

### Changes not reflecting

**Problem**: Cache or build not updating.

**Solution**:

**Backend**:
```cmd
# Restart Flask server
# Press Ctrl+C then run again
python app.py
```

**Frontend**:
```cmd
# React auto-reloads, but if not:
# Stop (Ctrl+C) and restart
npm start
```

**Browser cache**:
- Hard refresh: Ctrl+Shift+R (Windows/Linux)
- Hard refresh: Cmd+Shift+R (Mac)

### "Port already in use"

**Problem**: Server already running.

**Solution**:
```cmd
# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or use different port
# In backend/.env:
PORT=5001
```

## Testing & Debugging

### How to test backend without frontend

```cmd
# Test health
curl http://localhost:5000/api/health

# Get radar data
curl http://localhost:5000/api/radar/latest > test.json

# View in browser
http://localhost:5000/api/radar/latest
```

### How to see backend logs

**Local development**:
- Check terminal where `python app.py` is running

**Render.com**:
- Dashboard → Your Service → Logs tab

### How to debug frontend

1. Open browser DevTools (F12)
2. Console tab: See JavaScript errors
3. Network tab: See API requests/responses
4. Elements tab: Inspect HTML/CSS

### Test MRMS service directly

```cmd
cd backend
python test_mrms.py
```

This will:
- Download MRMS file
- Process GRIB2
- Save sample to `sample_radar_data.json`
- Show any errors

## Getting Help

### Check logs first

**Backend**: Terminal output or Render logs
**Frontend**: Browser console (F12)

### Provide when asking for help

1. Error message (exact text)
2. Backend logs
3. Browser console errors
4. Steps to reproduce
5. Operating system
6. Python version: `python --version`
7. Node version: `node --version`

### Useful debugging

```python
# In mrms_service.py, add prints
print(f"Downloading: {url}")
print(f"Got {len(data['features'])} features")
print(f"Timestamp: {timestamp}")
```

```javascript
// In App.js, add console logs
console.log('Fetching radar data...');
console.log('Received:', data);
console.log('Error:', error);
```

## Still Having Issues?

1. Check if this is a known limitation (see CHECKLIST.md)
2. Review relevant documentation file
3. Try the test script: `python test_mrms.py`
4. Check MRMS server status: https://mrms.ncep.noaa.gov/
5. Verify all dependencies installed correctly
6. Try in a fresh environment (new conda env)

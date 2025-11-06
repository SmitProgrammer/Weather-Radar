# Deployment Guide for Render.com

This guide walks through deploying the Weather Radar application to Render.com's free tier.

## Prerequisites

1. GitHub account with this repository pushed
2. Render.com account (sign up at https://render.com)

## Step 1: Deploy Backend

1. **Log in to Render.com** and click "New +"
2. Select **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

   **Basic Settings:**
   - Name: `weather-radar-backend`
   - Region: Choose closest to you
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

   **Instance Type:**
   - Select "Free" tier

   **Environment Variables:**
   Click "Add Environment Variable" and add:
   - Key: `PYTHON_VERSION`, Value: `3.11.0`

   **Important Note for GRIB Support:**
   The free tier on Render may have issues with eccodes (required for GRIB2 files). If deployment fails, you may need to:
   - Use the paid tier, OR
   - Modify the backend to use an alternative approach (pre-processed data)

5. Click **"Create Web Service"**

6. Wait for deployment (5-10 minutes). Note the URL (e.g., `https://weather-radar-backend.onrender.com`)

## Step 2: Deploy Frontend

1. In Render dashboard, click "New +"
2. Select **"Static Site"**
3. Connect the same GitHub repository
4. Configure:

   **Basic Settings:**
   - Name: `weather-radar-frontend`
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `build`

   **Environment Variables:**
   Add:
   - Key: `REACT_APP_API_URL`
   - Value: `https://your-backend-url.onrender.com/api` (use URL from Step 1)

5. Click **"Create Static Site"**

6. Wait for deployment (3-5 minutes)

## Step 3: Test the Application

1. Visit your frontend URL (e.g., `https://weather-radar-frontend.onrender.com`)
2. The map should load and display radar data
3. Click refresh to fetch new data
4. Check the browser console for any errors

## Troubleshooting

### Backend Issues

**Problem: "eccodes library not found"**
- Solution: The free tier may not support eccodes. Consider:
  1. Upgrading to paid tier
  2. Using Docker deployment with custom image
  3. Pre-processing data differently

**Problem: "Timeout errors"**
- Solution: MRMS downloads can be slow. The free tier has limited resources.
  - Increase cache duration in `mrms_service.py`
  - Consider using smaller data samples

### Frontend Issues

**Problem: "Failed to fetch radar data"**
- Check CORS is enabled in backend
- Verify `REACT_APP_API_URL` is correct
- Check backend logs on Render

**Problem: "Map not displaying"**
- Check browser console for errors
- Verify Leaflet CSS is loading

## Alternative: Docker Deployment

If the standard deployment has issues with eccodes, create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install eccodes
RUN apt-get update && apt-get install -y \
    libeccodes-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
```

Then deploy using Render's Docker support.

## Cost Optimization

**Free Tier Limitations:**
- Backend: 750 hours/month (enough for 24/7)
- Spins down after 15 minutes of inactivity
- First request after spin-down will be slow (30-60 seconds)

**Tips:**
- Increase cache duration to reduce MRMS fetches
- Consider ping service to keep backend alive
- Monitor usage in Render dashboard

## Monitoring

1. **Backend Logs**: In Render dashboard → Your service → Logs
2. **Frontend Logs**: Browser console
3. **API Health**: Visit `https://your-backend-url.onrender.com/api/health`

## Updates

To update the application:
1. Push changes to GitHub
2. Render automatically rebuilds and deploys
3. Check deployment logs for issues

## Support

- Render Docs: https://render.com/docs
- MRMS Data: https://mrms.ncep.noaa.gov/

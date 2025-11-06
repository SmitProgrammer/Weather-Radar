# --- Build frontend ---
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --- Build backend ---
FROM python:3.11-slim AS backend
WORKDIR /app

# Install system dependencies for cfgrib and GRIB2 processing
RUN apt-get update && apt-get install -y \
    libeccodes-dev \
    libeccodes-tools \
    && rm -rf /var/lib/apt/lists/*

COPY backend/ ./backend/
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy frontend build to backend's static folder
COPY --from=frontend-build /app/frontend/build ./backend/static

# Copy backend entrypoint
COPY backend/ ./backend/

# Set environment variables (optional)
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Start the backend (serves API and static frontend)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "backend.app:app"]
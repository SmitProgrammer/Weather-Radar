FROM python:3.11-slim

# Install eccodes and other system dependencies
RUN apt-get update && apt-get install -y \
    libeccodes-dev \
    libeccodes-tools \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create cache directory
RUN mkdir -p cache

# Expose port (Render sets PORT env variable)
ENV PORT=5000
EXPOSE $PORT

# Run the application
CMD gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120

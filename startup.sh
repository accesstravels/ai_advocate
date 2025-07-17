#!/bin/bash
# Azure Web App startup script for Python FastAPI

echo "Starting Azure AI Avatar application..."

# Set working directory
cd /tmp/*/

# Install dependencies
echo "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Set environment to production
export ENVIRONMENT=production

# Start the application with gunicorn for better performance
echo "Starting application with gunicorn on port $PORT..."
python -m gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT --timeout 600

#!/bin/bash
# Azure Web App startup script for Python FastAPI

# Install dependencies
pip install -r requirements.txt

# Start the application
python -m uvicorn main:app --host=0.0.0.0 --port=$PORT

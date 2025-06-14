#!/bin/bash
# start_backend.sh - Script to start the backend service

# Set Python path to include the application root
export PYTHONPATH=$PYTHONPATH:.

# Determine the port (use PORT environment variable provided by Render.com if available)
PORT=${PORT:-8000}

# Start the application with uvicorn
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port $PORT

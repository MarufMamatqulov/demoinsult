#!/bin/bash
# Script to start both frontend and backend services for the Stroke Rehabilitation platform

# Function to handle errors
handle_error() {
    echo "Error: $1"
    exit 1
}

echo "======================================================"
echo "      Starting Stroke Rehabilitation AI Platform       "
echo "======================================================"

# Check if .env file exists for backend
if [ ! -f "./backend/.env" ]; then
    echo "Warning: No .env file found in backend directory."
    echo "Creating .env from example..."
    if [ -f "./backend/.env.example" ]; then
        cp ./backend/.env.example ./backend/.env
        echo "Created .env file. Please edit it with your API keys before continuing."
    else
        handle_error "No .env.example file found. Please create a .env file manually."
    fi
fi

# Check for OpenAI API Key
if grep -q "OPENAI_API_KEY=\"\"" "./backend/.env" || ! grep -q "OPENAI_API_KEY" "./backend/.env"; then
    echo "Warning: OpenAI API Key not configured in .env file."
    echo "Please set your OpenAI API key before using AI features."
fi

# Start backend server
echo "Starting backend server..."
cd backend || handle_error "Backend directory not found"
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend server started (PID: $BACKEND_PID)"

# Wait a moment to ensure backend has started
sleep 3

# Start frontend server
echo "Starting frontend server..."
cd ../frontend || handle_error "Frontend directory not found"
npm start &
FRONTEND_PID=$!
echo "Frontend server started (PID: $FRONTEND_PID)"

# Function to handle script termination
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Servers shut down."
    exit 0
}

# Register cleanup function to run on script termination
trap cleanup SIGINT SIGTERM

echo "======================================================"
echo "      Stroke Rehabilitation AI Platform Running        "
echo "======================================================"
echo "  Backend: http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo "  Press Ctrl+C to stop all services"
echo "======================================================"

# Wait for termination signal
wait

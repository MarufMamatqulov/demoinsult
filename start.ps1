# PowerShell script to start both frontend and backend services for the Stroke Rehabilitation platform

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "      Starting Stroke Rehabilitation AI Platform       " -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# Check if .env file exists for backend
if (-Not (Test-Path "./backend/.env")) {
    Write-Host "Warning: No .env file found in backend directory." -ForegroundColor Yellow
    Write-Host "Creating .env from example..." -ForegroundColor Yellow
    if (Test-Path "./backend/.env.example") {
        Copy-Item "./backend/.env.example" "./backend/.env"
        Write-Host "Created .env file. Please edit it with your API keys before continuing." -ForegroundColor Green
    } else {
        Write-Host "Error: No .env.example file found. Please create a .env file manually." -ForegroundColor Red
        exit 1
    }
}

# Check for OpenAI API Key
$envContent = Get-Content "./backend/.env" -ErrorAction SilentlyContinue
if (-Not ($envContent -match "OPENAI_API_KEY=")) {
    Write-Host "Warning: OpenAI API Key not configured in .env file." -ForegroundColor Yellow
    Write-Host "Please set your OpenAI API key before using AI features." -ForegroundColor Yellow
}

# Start backend server
Write-Host "Starting backend server..." -ForegroundColor Cyan
$backendJob = Start-Job -ScriptBlock {
    Set-Location $args[0]
    & uvicorn main:app --reload --host 0.0.0.0 --port 8000
} -ArgumentList "$PWD\backend"

# Wait a moment to ensure backend has started
Start-Sleep -Seconds 3

# Start frontend server
Write-Host "Starting frontend server..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $args[0]
    & npm start
} -ArgumentList "$PWD\frontend"

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "      Stroke Rehabilitation AI Platform Running        " -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Backend: http://localhost:8000" -ForegroundColor Green
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor Green
Write-Host "  Press Ctrl+C to stop all services" -ForegroundColor Yellow
Write-Host "======================================================" -ForegroundColor Cyan

try {
    # Display job output in real-time
    while ($true) {
        Receive-Job -Job $backendJob
        Receive-Job -Job $frontendJob
        Start-Sleep -Seconds 1
    }
}
finally {
    # Clean up jobs when script is terminated
    Write-Host "Shutting down servers..." -ForegroundColor Yellow
    Stop-Job -Job $backendJob
    Stop-Job -Job $frontendJob
    Remove-Job -Job $backendJob
    Remove-Job -Job $frontendJob
    Write-Host "Servers shut down." -ForegroundColor Green
}

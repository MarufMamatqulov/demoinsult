# Script to verify the API fixes for the Stroke Rehabilitation AI Platform

Write-Host "=== Stroke Rehabilitation AI Platform API Fixes Verification ===" -ForegroundColor Cyan
Write-Host "This script will verify the fixes for:"
Write-Host "1. Assessment history endpoint (500 error fix)"
Write-Host "2. OpenAI integration compatibility (API version issues)"
Write-Host

# Check if the API server is running
$apiUrl = "http://localhost:8000"

# Try to get the server status
try {
    Write-Host "Checking if API server is running..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$apiUrl/docs" -Method Get -ErrorAction SilentlyContinue
    
    Write-Host "API server is running." -ForegroundColor Green
}
catch {
    Write-Host "API server does not appear to be running." -ForegroundColor Red
    Write-Host "Would you like to start the server now? (y/n)" -ForegroundColor Yellow
    $startServer = Read-Host

    if ($startServer -eq "y") {
        Write-Host "Starting API server..." -ForegroundColor Yellow
        
        # Start the server in a new PowerShell window
        Start-Process powershell -ArgumentList "-Command cd '$PSScriptRoot'; python backend/main.py"
        
        Write-Host "Waiting for server to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    } else {
        Write-Host "Please start the API server manually and run this script again." -ForegroundColor Red
        exit
    }
}

# Set environment variable for the API URL
$env:API_URL = $apiUrl

# Run the verification tests
Write-Host "Running API verification tests..." -ForegroundColor Yellow
python $PSScriptRoot/tests/verify_api_fixes.py

# Check the test result
if ($LASTEXITCODE -eq 0) {
    Write-Host "API fixes verification completed successfully!" -ForegroundColor Green
    
    # Open the documentation
    Write-Host "Opening the API fixes documentation..." -ForegroundColor Yellow
    Invoke-Item $PSScriptRoot/API_FIXES_DOCUMENTATION.md
} else {
    Write-Host "API fixes verification failed with exit code $LASTEXITCODE" -ForegroundColor Red
    Write-Host "Please check the logs for details." -ForegroundColor Red
}

Write-Host "=== Verification process completed ===" -ForegroundColor Cyan

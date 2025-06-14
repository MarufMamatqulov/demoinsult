# Final verification script for API fixes

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "=== Stroke Rehabilitation AI Platform API Fixes Verification ===" -ForegroundColor Cyan
Write-Host "This script will verify the fixes for:" -ForegroundColor White
Write-Host "1. Assessment history endpoint (500 error fix)" -ForegroundColor White
Write-Host "2. OpenAI integration compatibility (API version issues)" -ForegroundColor White
Write-Host "3. Patient chat endpoint functionality" -ForegroundColor White
Write-Host

# Check if the API server is running
$apiUrl = "http://localhost:8000"

try {
    Write-Host "Checking if API server is running..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$apiUrl/health" -Method Get -TimeoutSec 5 -ErrorAction Stop
    
    Write-Host "API server is running and healthy." -ForegroundColor Green
}
catch {
    Write-Host "API server does not appear to be running or is not responding." -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    
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
        exit 1
    }
}

# Run the verification tests
Write-Host "Running comprehensive API verification tests..." -ForegroundColor Yellow
python $PSScriptRoot/tests/final_verification.py

# Check the test result
if ($LASTEXITCODE -eq 0) {
    Write-Host "API fixes verification completed successfully!" -ForegroundColor Green
    
    # Open the documentation
    Write-Host "Opening the API fixes documentation..." -ForegroundColor Yellow
    Invoke-Item $PSScriptRoot/API_FIXES_UPDATE.md
    
    # Show additional resources
    Write-Host "Additional resources:" -ForegroundColor Cyan
    Write-Host "- View detailed log: $PSScriptRoot/final_api_verification.log" -ForegroundColor White
    Write-Host "- View results JSON: $PSScriptRoot/api_verification_results.json" -ForegroundColor White
    
    exit 0
} else {
    Write-Host "API fixes verification failed with exit code $LASTEXITCODE" -ForegroundColor Red
    Write-Host "Please check the logs for details:" -ForegroundColor Yellow
    Write-Host "- $PSScriptRoot/final_api_verification.log" -ForegroundColor White
    
    exit 1
}

Write-Host "=== Verification process completed ===" -ForegroundColor Cyan

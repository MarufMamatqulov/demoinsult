# PowerShell script to verify the fixed authentication system
# This script will:
# 1. Stop any running servers
# 2. Recreate the database with the fixed models
# 3. Start the server
# 4. Run test registration and login

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "======== STARTING AUTHENTICATION SYSTEM VERIFICATION ========" -ForegroundColor Cyan

# Function to check if port is in use
function Test-PortInUse {
    param(
        [int]$Port
    )
    
    $connections = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
    return $connections -ne $null
}

# Stop any running server on port 8000
if (Test-PortInUse -Port 8000) {
    Write-Host "Stopping existing server on port 8000..." -ForegroundColor Yellow
    $processId = (Get-NetTCPConnection -LocalPort 8000 -State Listen).OwningProcess
    Stop-Process -Id $processId -Force
    Write-Host "Server stopped." -ForegroundColor Green
}

# Change to backend directory
Set-Location -Path "c:\Users\Marufjon\InsultMedAI\backend"

# Verify the fixed models
Write-Host "Verifying fixed models..." -ForegroundColor Yellow
python verify_fixed_models.py

# Start the server in the background
Write-Host "Starting server..." -ForegroundColor Yellow
$server = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8000" -PassThru -NoNewWindow

# Wait for server to start
Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Create a test request
$testUser = @{
    email = "test_$(Get-Date -Format 'yyyyMMddHHmmss')@example.com"
    username = "testuser_$(Get-Date -Format 'yyyyMMddHHmmss')"
    password = "TestPassword123!"
    first_name = "Test"
    last_name = "User"
} | ConvertTo-Json

# Test registration
Write-Host "Testing registration..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/auth/register" -Method Post -Body $testUser -ContentType "application/json" -ErrorAction SilentlyContinue
    Write-Host "Registration successful! User ID: $($response.id)" -ForegroundColor Green
} catch {
    Write-Host "Registration failed: $_" -ForegroundColor Red
}

# Ask user if they want to keep the server running
$keepRunning = Read-Host -Prompt "Keep server running? (Y/N)"
if ($keepRunning -ne "Y" -and $keepRunning -ne "y") {
    Write-Host "Stopping server..." -ForegroundColor Yellow
    Stop-Process -Id $server.Id -Force
    Write-Host "Server stopped." -ForegroundColor Green
} else {
    Write-Host "Server is still running on http://localhost:8000" -ForegroundColor Green
    Write-Host "You can stop it manually later by pressing Ctrl+C in the server window or by running:" -ForegroundColor Yellow
    Write-Host "Stop-Process -Id $($server.Id) -Force" -ForegroundColor Yellow
}

Write-Host "======== VERIFICATION COMPLETE ========" -ForegroundColor Cyan

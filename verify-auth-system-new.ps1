# PowerShell script to verify the authentication system is working properly
# verify-auth-system-new.ps1

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "    STROKE REHABILITATION PLATFORM AUTH VERIFICATION" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if the backend server is already running
$backendRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -Method GET -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $backendRunning = $true
        Write-Host "✅ Backend server is already running" -ForegroundColor Green
    }
} catch {
    Write-Host "Backend server is not running. Starting it now..." -ForegroundColor Yellow
    $backendRunning = $false
}

# If backend is not running, start it
if (-not $backendRunning) {
    Write-Host "Starting the backend server..." -ForegroundColor Yellow
    
    # Start the backend server in a new window
    Start-Process powershell -ArgumentList "-Command", "cd $PSScriptRoot\backend; python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    
    # Wait for the server to start
    Write-Host "Waiting for the server to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Check if the server started properly
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -Method GET -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Backend server started successfully" -ForegroundColor Green
        } else {
            Write-Host "❌ Backend server started but returned status code $($response.StatusCode)" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Failed to start backend server: $_" -ForegroundColor Red
        exit 1
    }
}

# Run the comprehensive authentication verification script
Write-Host ""
Write-Host "Running comprehensive authentication verification tests..." -ForegroundColor Cyan
try {
    python $PSScriptRoot\tests\comprehensive_auth_verification.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "==================================================" -ForegroundColor Green
        Write-Host "    AUTH SYSTEM VERIFICATION PASSED!" -ForegroundColor Green
        Write-Host "==================================================" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "==================================================" -ForegroundColor Red
        Write-Host "    AUTH SYSTEM VERIFICATION FAILED!" -ForegroundColor Red
        Write-Host "==================================================" -ForegroundColor Red
        Write-Host "Check the auth_verification.log file for details." -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error running verification script: $_" -ForegroundColor Red
    exit 1
}

# Prompt to stop the server if we started it
if (-not $backendRunning) {
    Write-Host ""
    $stopServer = Read-Host "Do you want to stop the backend server? (y/n)"
    if ($stopServer -eq "y") {
        # Find and stop the uvicorn process
        Get-Process | Where-Object { $_.ProcessName -eq "python" -and $_.CommandLine -like "*uvicorn*" } | Stop-Process -Force
        Write-Host "Backend server stopped." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Authentication verification process completed." -ForegroundColor Cyan
# Verify that all previously failing API endpoints are now fixed

Write-Host "Starting API Endpoint Verification..." -ForegroundColor Cyan

# Make sure Python environment is activated
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating Python virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
} elseif (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating Python virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "No virtual environment found. Proceeding with system Python..." -ForegroundColor Yellow
}

# Check if the server is running
$serverRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $serverRunning = $true
        Write-Host "Server is already running." -ForegroundColor Green
    }
} catch {
    Write-Host "Server is not running. Starting it now..." -ForegroundColor Yellow
    Start-Process -FilePath "python" -ArgumentList "backend\main.py" -NoNewWindow
    
    # Wait for server to start
    Write-Host "Waiting for server to start..." -ForegroundColor Yellow
    $maxAttempts = 10
    $attempts = 0
    $serverStarted = $false
    
    while (-not $serverStarted -and $attempts -lt $maxAttempts) {
        try {
            Start-Sleep -Seconds 2
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $serverStarted = $true
                $serverRunning = $true
                Write-Host "Server started successfully." -ForegroundColor Green
            }
        } catch {
            $attempts++
            Write-Host "Waiting for server to start (attempt $attempts of $maxAttempts)..." -ForegroundColor Yellow
        }
    }
    
    if (-not $serverStarted) {
        Write-Host "Failed to start server after $maxAttempts attempts. Please start it manually and try again." -ForegroundColor Red
        exit 1
    }
}

# Run the verification script
Write-Host "Running endpoint verification script..." -ForegroundColor Cyan
python tests/verify_fixed_endpoints.py

# Check if verification was successful
if ($LASTEXITCODE -eq 0) {
    Write-Host "All fixed endpoints are working correctly!" -ForegroundColor Green
} else {
    Write-Host "Some endpoints still have issues. Check the logs for details." -ForegroundColor Red
}

Write-Host "Verification complete. See 'final_endpoint_verification.log' for detailed results." -ForegroundColor Cyan

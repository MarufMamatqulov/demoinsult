# Run the assessment history verification tests

Write-Host "Starting Assessment History Endpoint Verification..." -ForegroundColor Cyan

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

# Ensure required packages are installed
Write-Host "Checking required packages..." -ForegroundColor Yellow
pip install requests werkzeug -q

# Check if the server is running
$serverRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $serverRunning = $true
        Write-Host "Server is already running." -ForegroundColor Green
    }
} catch {
    Write-Host "Server is not running. Please start it with 'python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000' in another terminal." -ForegroundColor Red
    Write-Host "Would you like to start the server now? (y/n)" -ForegroundColor Yellow
    $answer = Read-Host
    
    if ($answer -eq 'y' -or $answer -eq 'Y') {
        Write-Host "Starting server in a new window..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-Command cd $PWD; python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
        
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
    } else {
        Write-Host "Server must be running to perform verification. Exiting..." -ForegroundColor Red
        exit 1
    }
}

# Create a test user for the verification
Write-Host "Creating test user for verification..." -ForegroundColor Cyan
python tests/create_test_user_direct.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to create test user. Cannot proceed with verification." -ForegroundColor Red
    exit 1
}

# Run the verification script
Write-Host "Running assessment history verification script..." -ForegroundColor Cyan
python tests/verify_assessment_history.py
$verificationExitCode = $LASTEXITCODE

# Check if verification was successful
if ($verificationExitCode -eq 0) {
    Write-Host "All assessment history endpoints are now working correctly!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "Some assessment history endpoints still have issues. Check the logs for details." -ForegroundColor Red
    exit 1
}

Write-Host "Verification complete. See 'assessment_history_verification.log' for detailed results." -ForegroundColor Cyan

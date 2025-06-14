# Restart the backend server with the latest changes
Write-Host "Restarting the Stroke Rehabilitation AI Platform Backend..." -ForegroundColor Cyan

# Check if there's a server already running on port 8000
$existingProcess = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($existingProcess) {
    Write-Host "Stopping existing server process (PID: $existingProcess)..." -ForegroundColor Yellow
    Stop-Process -Id $existingProcess -Force
    Start-Sleep -Seconds 2
}

# Apply OpenAI integration fix
Write-Host "Applying OpenAI integration fix..." -ForegroundColor Yellow
python -c "import sys; sys.path.append(r'$PWD'); from fix_openai_integration import fix_openai_integration; print('OpenAI integration fix ' + ('successfully applied' if fix_openai_integration() else 'failed to apply'))"

# Activate virtual environment if it exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating Python virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
} elseif (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating Python virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "No virtual environment found. Proceeding with system Python..." -ForegroundColor Yellow
}

# Start the server
Write-Host "Starting backend server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-Command cd $PWD; python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal

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
            Write-Host "Server started successfully." -ForegroundColor Green
        }
    } catch {
        $attempts++
        Write-Host "Waiting for server to start (attempt $attempts of $maxAttempts)..." -ForegroundColor Yellow
    }
}

if (-not $serverStarted) {
    Write-Host "Server may still be starting. Please check the new terminal window for details." -ForegroundColor Yellow
}

Write-Host "`nChanges Applied:" -ForegroundColor Cyan
Write-Host "1. Fixed OpenAI API integration to properly use your API key" -ForegroundColor Green
Write-Host "2. Improved rate limiting for profile requests with better error messages" -ForegroundColor Green
Write-Host "3. Added automatic cleanup of old rate limit entries" -ForegroundColor Green
Write-Host "4. Integrated OpenAI fix module into server startup process" -ForegroundColor Green

Write-Host "`nTest your application to verify the fixes are working correctly." -ForegroundColor Cyan
Write-Host "Run 'verify-all-fixes.ps1' to run a comprehensive verification." -ForegroundColor Cyan

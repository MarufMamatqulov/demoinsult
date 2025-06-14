# PowerShell script to deploy the fixed authentication system
# This will:
# 1. Install any missing dependencies
# 2. Start the server with the fixed models
# 3. Run tests to verify the authentication system

# Ensure we're in the correct directory
Set-Location -Path "c:\Users\Marufjon\InsultMedAI"

# Install dependencies if needed
Write-Host "Checking and installing dependencies..." -ForegroundColor Green
pip install -r requirements.txt

# Start the server in the background
$serverProcess = Start-Process -FilePath "python" -ArgumentList "backend/start_fixed_server.py" -PassThru -NoNewWindow

# Wait for the server to start
Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Run the authentication tests
Write-Host "Running authentication tests..." -ForegroundColor Cyan
python tests/test_fixed_auth.py

# Ask the user if they want to stop the server
$response = Read-Host -Prompt "Do you want to stop the server? (Y/N)"
if ($response -eq "Y" -or $response -eq "y") {
    Write-Host "Stopping server..." -ForegroundColor Red
    Stop-Process -Id $serverProcess.Id -Force
    Write-Host "Server stopped." -ForegroundColor Green
} else {
    Write-Host "Server is still running. You can manually stop it by pressing Ctrl+C in the server window." -ForegroundColor Yellow
}

Write-Host "Deployment process completed." -ForegroundColor Green

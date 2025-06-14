# Verify all API fixes for the Stroke Rehabilitation AI Platform
Write-Host "Starting API Fixes Verification..." -ForegroundColor Cyan

# Create log file
$logFile = "final_api_verification.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"$timestamp - Starting verification of all API fixes" | Out-File -FilePath $logFile

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
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install requests python-dotenv openai -q

# Function to log results
function Log-Step {
    param (
        [string]$step,
        [bool]$success,
        [string]$message
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $status = if ($success) { "SUCCESS" } else { "FAILED" }
    $logEntry = "$timestamp - $step - $status - $message"
    $logEntry | Out-File -FilePath $logFile -Append
    
    if ($success) {
        Write-Host "✅ ${step}: ${message}" -ForegroundColor Green
    } else {
        Write-Host "❌ ${step}: ${message}" -ForegroundColor Red
    }
}

# 1. Check if our enhanced files are in place
Write-Host "Checking if fix files are in place..." -ForegroundColor Yellow
$openaiHelperExists = Test-Path "backend\utils\openai_helper.py"
$fixModuleExists = Test-Path "fix_openai_integration.py"

if ($openaiHelperExists -and $fixModuleExists) {
    Log-Step -step "Fix Files Check" -success $true -message "OpenAI helper and fix module found."
} else {
    Log-Step -step "Fix Files Check" -success $false -message "Missing fix files. Cannot proceed with verification."
    exit 1
}

# 2. Verify OpenAI Integration
Write-Host "Verifying OpenAI Integration..." -ForegroundColor Yellow
$openaiTestResult = python -c "import sys; import os; sys.path.append(os.path.abspath('.')); from fix_openai_integration import fix_openai_integration; print('SUCCESS' if fix_openai_integration() else 'FAILURE')"
$openaiSuccess = $openaiTestResult -eq "SUCCESS"

Log-Step -step "OpenAI Integration" -success $openaiSuccess -message "OpenAI API key integration check completed."

# 3. Check if server is running
$serverRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $serverRunning = $true
        Log-Step -step "Server Check" -success $true -message "Server is running."
    }
} catch {
    Log-Step -step "Server Check" -success $false -message "Server is not running. Starting it now..."
    
    # Start the server in a new window
    Start-Process powershell -ArgumentList "-Command cd $PWD; python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
    
    # Wait for server to start
    Write-Host "Waiting for server to start..." -ForegroundColor Yellow
    $maxAttempts = 10
    $attempts = 0
    $serverStarted = $false
    
    while ($attempts -lt $maxAttempts -and -not $serverStarted) {
        Start-Sleep -Seconds 3
        $attempts++
        
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $serverStarted = $true
                $serverRunning = $true
                Log-Step -step "Server Start" -success $true -message "Server started successfully after $attempts attempts."
            }
        } catch {
            Write-Host "Waiting for server to start (attempt $attempts of $maxAttempts)..." -ForegroundColor Yellow
        }
    }
    
    if (-not $serverStarted) {
        Log-Step -step "Server Start" -success $false -message "Failed to start server after $maxAttempts attempts."
    }
}

if (-not $serverRunning) {
    Log-Step -step "Verification" -success $false -message "Cannot proceed with verification - server is not running."
    exit 1
}

# 4. Run the comprehensive verification script
Write-Host "Running comprehensive API verification..." -ForegroundColor Yellow
$verificationResult = python .\tests\verify_api_fixes_final.py
$verificationExitCode = $LASTEXITCODE
$verificationSuccess = $verificationExitCode -eq 0

Log-Step -step "API Verification" -success $verificationSuccess -message "Comprehensive API verification completed."

# 5. Check the api_fixes_verification.json file
if (Test-Path "api_fixes_verification.json") {
    $jsonContent = Get-Content "api_fixes_verification.json" -Raw | ConvertFrom-Json
    $allTestsPassed = $jsonContent.all_passed
    
    if ($allTestsPassed) {
        Log-Step -step "Verification Summary" -success $true -message "All verification tests passed successfully."
    } else {
        Log-Step -step "Verification Summary" -success $false -message "Some verification tests failed. Check api_fixes_verification.json for details."
    }
} else {
    Log-Step -step "Verification Summary" -success $false -message "Could not find verification results file."
}

# Final output
if ($verificationSuccess) {
    Write-Host "`n🎉 All API fixes have been successfully verified!" -ForegroundColor Green
    Write-Host "The Stroke Rehabilitation AI Platform should now be functioning correctly." -ForegroundColor Green
    
    # Update the verification status in a file
    "API_FIXES_VERIFIED=true" | Out-File -FilePath "verification_status.env" -Encoding utf8
} else {
    Write-Host "`n⚠️ Some API fixes verification tests failed. Please review the logs and fix any remaining issues." -ForegroundColor Red
}

# Log completion
"$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Verification completed - Overall result: $(if ($verificationSuccess) { 'SUCCESS' } else { 'FAILURE' })" | Out-File -FilePath $logFile -Append

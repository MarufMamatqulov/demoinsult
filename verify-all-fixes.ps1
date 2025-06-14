# Comprehensive Verification Script for Stroke Rehabilitation AI Platform
Write-Host "Starting Comprehensive Verification..." -ForegroundColor Cyan

# Ensure required packages are installed
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install requests python-dotenv openai -q

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

# Function to log results
function Log-Step {
    param (
        [string]$step,
        [bool]$success,
        [string]$message
    )
    
    $status = if ($success) { "SUCCESS" } else { "FAILED" }
    $logEntry = "$(Get-Date) - $step - $status - $message"
    $logEntry | Out-File -FilePath $logFile -Append
      if ($success) {
        Write-Host "${step}: ${message}" -ForegroundColor Green
    } else {
        Write-Host "${step}: ${message}" -ForegroundColor Red
    }
}

# Check if the server is running
$serverRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $serverRunning = $true
        Log-Step -step "Server Check" -success $true -message "Server is already running."
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
    
    while (-not $serverStarted -and $attempts -lt $maxAttempts) {
        try {
            Start-Sleep -Seconds 2
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $serverStarted = $true
                $serverRunning = $true
                Log-Step -step "Server Start" -success $true -message "Server started successfully."
            }
        } catch {
            $attempts++
            Write-Host "Waiting for server to start (attempt $attempts of $maxAttempts)..." -ForegroundColor Yellow
        }
    }
    
    if (-not $serverStarted) {
        Log-Step -step "Server Start" -success $false -message "Failed to start server after $maxAttempts attempts."
        exit 1
    }
}

# Step 1: Verify Assessment History Endpoints
Write-Host "`nStep 1: Verifying Assessment History Endpoints..." -ForegroundColor Cyan
try {
    & .\verify-assessment-history.ps1
    if ($LASTEXITCODE -eq 0) {
        Log-Step -step "Assessment History" -success $true -message "Assessment history endpoints are working correctly."
    } else {
        Log-Step -step "Assessment History" -success $false -message "Assessment history endpoints have issues."
    }
} catch {
    Log-Step -step "Assessment History" -success $false -message "Error running assessment history verification: $_"
}

# Step 2: Verify Email Configuration
Write-Host "`nStep 2: Verifying Email Configuration..." -ForegroundColor Cyan
try {
    & .\verify-email-configuration.ps1
    if ($LASTEXITCODE -eq 0) {
        Log-Step -step "Email Configuration" -success $true -message "Email configuration is working correctly."
    } else {
        Log-Step -step "Email Configuration" -success $false -message "Email configuration has issues."
    }
} catch {
    Log-Step -step "Email Configuration" -success $false -message "Error running email verification: $_"
}

# Step 3: Verify OpenAI Integration
Write-Host "`nStep 3: Verifying OpenAI Integration..." -ForegroundColor Cyan
try {
    & .\verify-openai-integration.ps1
    if ($LASTEXITCODE -eq 0) {
        Log-Step -step "OpenAI Integration" -success $true -message "OpenAI integration is working correctly."
    } else {
        Log-Step -step "OpenAI Integration" -success $false -message "OpenAI integration has issues."
    }
} catch {
    Log-Step -step "OpenAI Integration" -success $false -message "Error running OpenAI verification: $_"
}

# Step 4: Test User Registration
Write-Host "`nStep 4: Testing User Registration..." -ForegroundColor Cyan
try {
    python tests/test_registration_endpoint.py
    if ($LASTEXITCODE -eq 0) {
        Log-Step -step "User Registration" -success $true -message "User registration is working correctly."
    } else {
        Log-Step -step "User Registration" -success $false -message "User registration has issues."
    }
} catch {
    Log-Step -step "User Registration" -success $false -message "Error testing user registration: $_"
}

# Step 5: Test Rate Limiting
Write-Host "`nStep 5: Testing Rate Limiting..." -ForegroundColor Cyan
$rateLimitScriptPath = "tests\test_rate_limiting.py"

@"
import requests
import time
import sys

def test_rate_limiting():
    """Test the rate limiting implementation for profile requests."""
    print("Testing rate limiting for profile requests...")
    
    # Make multiple requests in quick succession
    url = "http://localhost:8000/profile"
    headers = {"host": "test-client"}
    
    # First request should succeed
    print("Making first request...")
    response1 = requests.get(url, headers=headers)
    print(f"First request status: {response1.status_code}")
    
    if response1.status_code != 200:
        print(f"First request failed: {response1.text}")
        return False
    
    # Second immediate request should be rate limited
    print("Making immediate second request (should be rate limited)...")
    response2 = requests.get(url, headers=headers)
    print(f"Second request status: {response2.status_code}")
    
    if response2.status_code != 429:
        print("Rate limiting not working - second request should have been blocked")
        return False
    
    # Check if the response contains the expected error message
    if "Too many profile requests" not in response2.text:
        print("Rate limiting error message is not as expected")
        return False
    
    # Wait for 6 seconds (more than the 5-second window)
    print("Waiting for 6 seconds...")
    time.sleep(6)
    
    # Third request after waiting should succeed
    print("Making third request after waiting...")
    response3 = requests.get(url, headers=headers)
    print(f"Third request status: {response3.status_code}")
    
    if response3.status_code != 200:
        print(f"Third request failed: {response3.text}")
        return False
    
    print("Rate limiting is working correctly!")
    return True

if __name__ == "__main__":
    success = test_rate_limiting()
    sys.exit(0 if success else 1)
"@ | Out-File -FilePath $rateLimitScriptPath -Encoding utf8

try {
    python $rateLimitScriptPath
    if ($LASTEXITCODE -eq 0) {
        Log-Step -step "Rate Limiting" -success $true -message "Rate limiting is working correctly."
    } else {
        Log-Step -step "Rate Limiting" -success $false -message "Rate limiting has issues."
    }
} catch {
    Log-Step -step "Rate Limiting" -success $false -message "Error testing rate limiting: $_"
}

# Summarize results
Write-Host "`nComprehensive Verification Complete!" -ForegroundColor Cyan
Write-Host "See $logFile for detailed results."

# Read log file and count successes/failures
$logContent = Get-Content -Path $logFile
$totalTests = ($logContent | Select-String -Pattern " - SUCCESS - " -CaseSensitive).Count + 
              ($logContent | Select-String -Pattern " - FAILED - " -CaseSensitive).Count
$successTests = ($logContent | Select-String -Pattern " - SUCCESS - " -CaseSensitive).Count
$failedTests = ($logContent | Select-String -Pattern " - FAILED - " -CaseSensitive).Count

Write-Host "`nSummary:"
Write-Host "Total Tests: $totalTests"
Write-Host "Successful: $successTests" -ForegroundColor Green
Write-Host "Failed: $failedTests" -ForegroundColor Red

# Create a summary file
$summaryContent = @"
# Stroke Rehabilitation AI Platform Verification Summary

Date: $(Get-Date)

## Results Summary
- Total Tests: $totalTests
- Successful: $successTests
- Failed: $failedTests

## Detailed Results
$(Get-Content -Path $logFile)
"@

$summaryContent | Out-File -FilePath "VERIFICATION_SUMMARY.md"
Write-Host "`nDetailed summary written to VERIFICATION_SUMMARY.md"

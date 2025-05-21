# Mobile Interaction Fixes Deployment Script

# Set error handling
$ErrorActionPreference = "Stop"

# Function to log messages with timestamp
function Log-Message {
    param ([string]$message)
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $message"
}

Log-Message "Starting deployment of mobile interaction fixes..."

# Navigate to the frontend directory
try {
    Set-Location -Path ".\frontend"
    Log-Message "Changed directory to frontend"
} catch {
    Log-Message "Error: Failed to change directory to frontend. $($_.Exception.Message)"
    exit 1
}

# Install dependencies if needed
if (-not (Test-Path -Path ".\node_modules")) {
    Log-Message "Installing frontend dependencies..."
    npm install
    if ($LASTEXITCODE -ne 0) {
        Log-Message "Error: npm install failed with exit code $LASTEXITCODE"
        exit 1
    }
}

# Build the frontend with the mobile interaction fixes
Log-Message "Building frontend with mobile interaction fixes..."
npm run build
if ($LASTEXITCODE -ne 0) {
    Log-Message "Error: npm build failed with exit code $LASTEXITCODE"
    exit 1
}

# Test the build
Log-Message "Testing the build..."

# Verify that key files exist in the build
$requiredFiles = @(
    ".\build\static\js\main.*.js",
    ".\build\static\css\main.*.css",
    ".\build\index.html"
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path -Path $file)) {
        Log-Message "Error: Required file pattern $file not found in build"
        exit 1
    }
}

Log-Message "Build verification completed successfully"

# Deploy the build
Log-Message "Deploying the frontend with mobile interaction fixes..."

# Use the existing deployment script if available
if (Test-Path -Path "..\deploy-frontend.ps1") {
    Log-Message "Running deployment script..."
    Set-Location -Path ".."
    .\deploy-frontend.ps1
    if ($LASTEXITCODE -ne 0) {
        Log-Message "Error: Deployment script failed with exit code $LASTEXITCODE"
        exit 1
    }
} else {
    Log-Message "No deployment script found. Please deploy the build manually."
    Log-Message "Build files are located in: $(Resolve-Path .\build)"
}

Log-Message "Mobile interaction fixes deployment completed successfully"

# Return to the original directory
Set-Location -Path ".."

Log-Message "Deployment script finished"

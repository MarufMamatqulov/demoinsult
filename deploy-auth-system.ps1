#!/usr/bin/env pwsh
# Authentication System Deployment Script

# Show intro
Write-Host "========================================="
Write-Host "Stroke Rehabilitation AI Platform"
Write-Host "Authentication System Deployment"
Write-Host "========================================="
Write-Host ""

# Check environment
Write-Host "Checking environment..."
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    Write-Host "Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

$nodeInstalled = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeInstalled) {
    Write-Host "Node.js not found. Please install Node.js 14 or higher." -ForegroundColor Red
    exit 1
}

# Verify .env file configuration
Write-Host "Checking .env file configuration..."
$envPath = Join-Path $PSScriptRoot "backend\.env"
if (-not (Test-Path $envPath)) {
    Write-Host ".env file not found in backend directory. Please create it first." -ForegroundColor Red
    exit 1
}

$envContent = Get-Content $envPath -Raw
$emailConfigured = $envContent -match "EMAIL_USER=\S+" -and $envContent -match "EMAIL_PASSWORD=\S+"
if (-not $emailConfigured) {
    Write-Host "Email configuration is missing in the .env file. Please update it with your email credentials." -ForegroundColor Yellow
    Write-Host "Refer to EMAIL_CONFIGURATION_GUIDE.md for detailed instructions." -ForegroundColor Yellow
    $continue = Read-Host "Do you want to continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit 0
    }
}

$jwtConfigured = $envContent -match "JWT_SECRET_KEY=\S+"
if (-not $jwtConfigured) {
    Write-Host "JWT configuration is missing in the .env file. Please update it with a secure JWT secret key." -ForegroundColor Yellow
    Write-Host "Refer to EMAIL_CONFIGURATION_GUIDE.md for detailed instructions." -ForegroundColor Yellow
    $continue = Read-Host "Do you want to continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit 0
    }
}

# Update database with new schema (run migrations)
Write-Host "Running database migrations..."
Set-Location -Path (Join-Path $PSScriptRoot "backend")
python -m alembic upgrade head
if ($LASTEXITCODE -ne 0) {
    Write-Host "Database migration failed. Please check the migration scripts and database connection." -ForegroundColor Red
    exit 1
}

# Install frontend dependencies
Write-Host "Installing frontend dependencies..."
Set-Location -Path (Join-Path $PSScriptRoot "frontend")
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install frontend dependencies." -ForegroundColor Red
    exit 1
}

# Build frontend
Write-Host "Building frontend..."
npm run build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Frontend build failed." -ForegroundColor Red
    exit 1
}

# Run tests
Write-Host "Running authentication tests..."
Set-Location -Path $PSScriptRoot
python -m tests.test_authentication
if ($LASTEXITCODE -ne 0) {
    Write-Host "Authentication tests failed. Please check the logs." -ForegroundColor Yellow
    $continue = Read-Host "Do you want to continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit 0
    }
}

# Deployment complete
Write-Host ""
Write-Host "========================================="
Write-Host "Authentication System Deployment Complete" -ForegroundColor Green
Write-Host "========================================="
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Start the backend server: ./start_backend.sh"
Write-Host "2. Start the frontend server: cd frontend && npm start"
Write-Host "3. Test the authentication system by registering a new user"
Write-Host "4. Verify that email verification and password reset work correctly"
Write-Host ""
Write-Host "For troubleshooting, refer to AUTHENTICATION_IMPLEMENTATION.md"
Write-Host ""

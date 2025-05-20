
# Navigate to the frontend directory
Set-Location -Path "c:\Users\Marufjon\InsultMedAI\frontend"

# Clear node_modules and package-lock.json
Write-Host "Cleaning node_modules and package-lock.json..." -ForegroundColor Yellow
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force "node_modules"
}
if (Test-Path "package-lock.json") {
    Remove-Item -Force "package-lock.json"
}

# Install ajv explicitly first
Write-Host "Installing ajv with required dependencies..." -ForegroundColor Green
npm install --save ajv@8.12.0

# Install all dependencies with legacy peer deps
Write-Host "Installing all dependencies..." -ForegroundColor Green
npm install --legacy-peer-deps

# Testing the build
Write-Host "Testing build process..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build succeeded! The frontend is ready for deployment." -ForegroundColor Green
} else {
    Write-Host "❌ Build failed. See errors above." -ForegroundColor Red
}

# Return to the project root
Set-Location -Path "c:\Users\Marufjon\InsultMedAI"

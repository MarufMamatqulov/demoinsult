# Verify Frontend Dependencies and TypeScript compatibility

Write-Host "Verifying frontend dependencies and TypeScript compatibility..." -ForegroundColor Green

# Change to frontend directory
Set-Location -Path "c:\Users\Marufjon\InsultMedAI\frontend"

# Create temporary .npmrc file for installation
if (-not (Test-Path ".npmrc")) {
    Write-Host "Creating .npmrc file with legacy-peer-deps=true..." -ForegroundColor Yellow
    "legacy-peer-deps=true" | Out-File -FilePath ".npmrc" -Encoding utf8
}

# Clean installation
Write-Host "Cleaning node_modules..." -ForegroundColor Yellow
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force "node_modules"
}
if (Test-Path "package-lock.json") {
    Remove-Item -Force "package-lock.json"
}

# Install dependencies with --legacy-peer-deps
Write-Host "Installing dependencies with --legacy-peer-deps..." -ForegroundColor Yellow
npm install --legacy-peer-deps

# Check TypeScript compilation
Write-Host "Checking TypeScript compilation..." -ForegroundColor Yellow
npx tsc --noEmit

$tsResult = $LASTEXITCODE
if ($tsResult -eq 0) {
    Write-Host "✅ TypeScript compilation successful!" -ForegroundColor Green
} else {
    Write-Host "❌ TypeScript compilation failed. Please fix the errors before deploying." -ForegroundColor Red
}

# Try build
Write-Host "Attempting build process..." -ForegroundColor Yellow
npm run build

$buildResult = $LASTEXITCODE
if ($buildResult -eq 0) {
    Write-Host "✅ Build successful! Frontend is ready for deployment." -ForegroundColor Green
} else {
    Write-Host "❌ Build failed. Please fix the errors before deploying." -ForegroundColor Red
}

# Return to the project root
Set-Location -Path "c:\Users\Marufjon\InsultMedAI"

if ($tsResult -eq 0 -and $buildResult -eq 0) {
    Write-Host "All checks passed! You can now deploy the frontend to Vercel." -ForegroundColor Green
    Write-Host "Use: .\deploy-frontend.ps1 -EC2_IP 16.170.244.228 [-GithubRepo YOUR_GITHUB_REPO]" -ForegroundColor Green
} else {
    Write-Host "Please fix the errors before deploying to Vercel." -ForegroundColor Red
}

# Script to fix all issues for Vercel deployment

Write-Host "🔧 Starting deployment fix script..." -ForegroundColor Cyan

# Step 1: Navigate to project root
Set-Location -Path "c:\Users\Marufjon\InsultMedAI"
Write-Host "Working in: $(Get-Location)" -ForegroundColor Green

# Step 2: Backup current files before making changes
Write-Host "Creating backups of key files..." -ForegroundColor Yellow
Copy-Item -Path "frontend\package.json" -Destination "frontend\package.json.bak" -Force
Copy-Item -Path "frontend\vercel.json" -Destination "frontend\vercel.json.bak" -Force

# Step 3: Replace vercel.json with the new version
Write-Host "Updating vercel.json..." -ForegroundColor Green
if (Test-Path "frontend\vercel.json.new") {
    Remove-Item -Path "frontend\vercel.json" -Force
    Rename-Item -Path "frontend\vercel.json.new" -NewName "vercel.json"
    Write-Host "✅ vercel.json has been updated." -ForegroundColor Green
} else {
    Write-Host "⚠️ vercel.json.new not found. Skipping this step." -ForegroundColor Yellow
}

# Step 4: Clean up frontend dependencies
Write-Host "Setting up environment for clean installation..." -ForegroundColor Green
Set-Location -Path "frontend"

# Create .npmrc file for legacy peer deps
@"
legacy-peer-deps=true
"@ | Out-File -FilePath ".npmrc" -Encoding utf8 -Force

# Clean installation
Write-Host "Cleaning node_modules..." -ForegroundColor Yellow
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force "node_modules"
}
if (Test-Path "package-lock.json") {
    Remove-Item -Force "package-lock.json"
}

# Install dependencies explicitly in the right order
Write-Host "Installing dependencies..." -ForegroundColor Green
npm install --save ajv@8.12.0 --legacy-peer-deps
npm install --legacy-peer-deps

# Step 5: Create production build for testing
Write-Host "Creating production build for testing..." -ForegroundColor Green
npm run build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Build successful! Your React app should now be compatible with Vercel." -ForegroundColor Green
    
    # Step 6: Create a Vercel-specific deployment command
    Set-Location -Path ".."
    @"
# filepath: c:\Users\Marufjon\InsultMedAI\deploy-to-vercel.ps1
# Script to deploy frontend to Vercel

# Prerequisites: 
# 1. Vercel CLI should be installed: npm install -g vercel
# 2. You should be logged in to Vercel: vercel login

Write-Host "🚀 Deploying to Vercel..." -ForegroundColor Cyan

# Navigate to frontend directory
Set-Location -Path "frontend"

# Set up environment variable for production
vercel env add REACT_APP_API_URL production http://16.170.244.228:8000

# Deploy to production
vercel --prod

if (`$LASTEXITCODE -eq 0) {
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
} else {
    Write-Host "❌ Deployment failed. Check the errors above." -ForegroundColor Red
}

# Return to the project root
Set-Location -Path ".."
"@ | Out-File -FilePath "deploy-to-vercel.ps1" -Encoding utf8 -Force
    
    Write-Host "Created deploy-to-vercel.ps1 script for deployment." -ForegroundColor Green
} else {
    Write-Host "❌ Build failed. Please check the errors above." -ForegroundColor Red
}

# Return to project root
Set-Location -Path ".."

Write-Host @"

==============================================
🚀 Next steps for Vercel deployment:

1. Make sure you have Vercel CLI installed:
   npm install -g vercel

2. Log in to Vercel:
   vercel login

3. Use the deployment script:
   .\deploy-to-vercel.ps1

Alternatively, you can deploy through the Vercel dashboard:
1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Select frontend as the root directory
4. Add REACT_APP_API_URL environment variable with value http://16.170.244.228:8000
5. Deploy!
==============================================
"@ -ForegroundColor Cyan

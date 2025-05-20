# Filepath: c:\Users\Marufjon\InsultMedAI\deploy-frontend.ps1
# Deploy Frontend to Vercel

param(
    [Parameter(Mandatory=$true)]
    [string]$EC2_IP,
    
    [Parameter(Mandatory=$false)]
    [string]$VercelToken,
    
    [Parameter(Mandatory=$false)]
    [string]$GithubRepo
)

# Step 1: Update configuration files with the EC2 IP
Write-Host "Updating configuration files with EC2 IP: $EC2_IP" -ForegroundColor Green
Write-Host "Note: Make sure to use the public IP address of your EC2 instance, not the internal one" -ForegroundColor Yellow

# Update .env.production
$envProdPath = "c:\Users\Marufjon\InsultMedAI\frontend\.env.production"
$envProdContent = Get-Content $envProdPath -Raw
$envProdContent = $envProdContent -replace "REACT_APP_API_URL=http://YOUR_PUBLIC_EC2_IP:8000", "REACT_APP_API_URL=http://$EC2_IP`:8000"
Set-Content -Path $envProdPath -Value $envProdContent

# Update vercel.json
$vercelJsonPath = "c:\Users\Marufjon\InsultMedAI\frontend\vercel.json"
$vercelJsonContent = Get-Content $vercelJsonPath -Raw
$vercelJsonContent = $vercelJsonContent -replace '"REACT_APP_API_URL": "http://YOUR_PUBLIC_EC2_IP:8000"', "`"REACT_APP_API_URL`": `"http://$EC2_IP`:8000`""
Set-Content -Path $vercelJsonPath -Value $vercelJsonContent

# Step 2: Check if Vercel CLI is installed
$vercelInstalled = $null
try {
    $vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
} catch {
    $vercelInstalled = $null
}

if ($null -eq $vercelInstalled) {
    Write-Host "Vercel CLI is not installed. Installing now..." -ForegroundColor Yellow
    npm install -g vercel
}

# Step 3: Deploy to Vercel (if token is provided)
if ($VercelToken) {
    Write-Host "Deploying to Vercel..." -ForegroundColor Green
    
    # Change to frontend directory
    Set-Location -Path "c:\Users\Marufjon\InsultMedAI\frontend"
    
    # Login to Vercel
    Write-Host "Logging in to Vercel..." -ForegroundColor Green
    vercel login --token $VercelToken
    
    # Deploy to Vercel
    Write-Host "Deploying to Vercel..." -ForegroundColor Green
    vercel --prod
    
    Write-Host "Frontend deployment complete! Check the Vercel dashboard for the deployment URL." -ForegroundColor Green
} elseif ($GithubRepo) {
    # Check if git is installed
    $gitInstalled = $null
    try {
        $gitInstalled = Get-Command git -ErrorAction SilentlyContinue
    } catch {
        $gitInstalled = $null
    }
    
    if ($null -eq $gitInstalled) {
        Write-Host "Git is not installed. Please install Git and try again." -ForegroundColor Red
        exit 1
    }
    
    # Initialize git repository and push to GitHub
    Write-Host "Pushing code to GitHub repository: $GithubRepo" -ForegroundColor Green
    
    Set-Location -Path "c:\Users\Marufjon\InsultMedAI"
    
    # Check if .git directory exists
    if (!(Test-Path -Path ".git")) {
        Write-Host "Initializing git repository..." -ForegroundColor Green
        git init
        git add .
        git commit -m "Initial commit for deployment"
        git branch -M main
        git remote add origin $GithubRepo
        git push -u origin main
    } else {
        Write-Host "Git repository already initialized. Committing changes..." -ForegroundColor Green
        git add .
        git commit -m "Update configuration for deployment"
        git push
    }
    
    Write-Host "Code pushed to GitHub. Now go to Vercel and import your GitHub repository to deploy the frontend." -ForegroundColor Green
} else {
    Write-Host "No deployment method selected. Configuration files have been updated with EC2 IP: $EC2_IP" -ForegroundColor Yellow
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Push your code to GitHub" -ForegroundColor Yellow
    Write-Host "2. Go to Vercel and import your GitHub repository" -ForegroundColor Yellow
    Write-Host "3. Select the frontend directory and deploy" -ForegroundColor Yellow
}

# Reset location
Set-Location -Path "c:\Users\Marufjon\InsultMedAI"

Write-Host "Process complete!" -ForegroundColor Green

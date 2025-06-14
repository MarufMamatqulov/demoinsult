# Clean Git Repository - Remove Sensitive Information
# This script helps remove API keys and sensitive information from Git history

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  Git repository cleaning assistant" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "WARNING: This script will alter your Git history." -ForegroundColor Yellow
Write-Host "Make sure you've communicated with your team before running this." -ForegroundColor Yellow
Write-Host ""

$continue = Read-Host "Do you want to continue? (y/n)"
if ($continue -ne "y") {
    Write-Host "Operation cancelled." -ForegroundColor Red
    exit
}

# 1. First, remove sensitive files from git cache
Write-Host "`n1. Removing sensitive files from Git cache..." -ForegroundColor Cyan
git rm --cached backend/.env
git rm --cached set-openai-api-key.ps1
git rm --cached fix-openai-api-key.ps1
git rm --cached test_token.txt
git rm --cached ec2-kp.pem

# 2. Ensure .gitignore is properly configured
Write-Host "`n2. Ensuring .gitignore is properly configured..." -ForegroundColor Cyan
$gitignoreContent = Get-Content .gitignore
$sensitivePatterns = @(
    ".env",
    "*.pem",
    "set-openai-api-key.ps1",
    "fix-openai-api-key.ps1",
    "test_token.txt"
)

foreach ($pattern in $sensitivePatterns) {
    if (-not ($gitignoreContent -match $pattern)) {
        Add-Content -Path .gitignore -Value "`n$pattern"
        Write-Host "  Added $pattern to .gitignore" -ForegroundColor Green
    }
}

# 3. Commit the .gitignore changes
Write-Host "`n3. Committing .gitignore changes..." -ForegroundColor Cyan
git add .gitignore
git commit -m "Update .gitignore to exclude sensitive files"

Write-Host "`nComplete! Now you can try pushing again:" -ForegroundColor Green
Write-Host "  git push" -ForegroundColor Yellow
Write-Host ""
Write-Host "If you still have issues with sensitive data in Git history," -ForegroundColor Yellow
Write-Host "consider using BFG Repo-Cleaner or git-filter-repo to clean history." -ForegroundColor Yellow

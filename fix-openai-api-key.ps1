# Fix OpenAI API Key in Environment Variables
Write-Host "Setting up OpenAI API Key..." -ForegroundColor Cyan

# Get the current directory
$currentDir = Get-Location

# Define the paths
$envFilePath = Join-Path $currentDir "backend\.env"

# Check if the .env file exists
if (Test-Path $envFilePath) {
    Write-Host "Found .env file at $envFilePath" -ForegroundColor Green
    
    # Read the current OpenAI API key from the .env file
    $envContent = Get-Content $envFilePath -Raw
    $apiKeyMatch = [regex]::Match($envContent, 'OPENAI_API_KEY=(.+)')
    
    if ($apiKeyMatch.Success) {
        $apiKey = $apiKeyMatch.Groups[1].Value.Trim()
        Write-Host "Found OpenAI API key in .env file" -ForegroundColor Green
        
        # Set the environment variable for the current session
        $env:OPENAI_API_KEY = $apiKey
        Write-Host "Set OPENAI_API_KEY environment variable for current session" -ForegroundColor Green
        
        # Generate a small PowerShell script to set the environment variable permanently
        $envSetupScript = @"
# Set OpenAI API Key as an environment variable
[Environment]::SetEnvironmentVariable('OPENAI_API_KEY', '$apiKey', 'User')
Write-Host "OpenAI API Key has been set as a user environment variable." -ForegroundColor Green
"@
        
        $envSetupScriptPath = Join-Path $currentDir "set-openai-api-key.ps1"
        $envSetupScript | Out-File -FilePath $envSetupScriptPath -Encoding utf8
        
        Write-Host "Created script to set OpenAI API key as a permanent environment variable:" -ForegroundColor Yellow
        Write-Host "Run the following to set it permanently:" -ForegroundColor Yellow
        Write-Host ".\set-openai-api-key.ps1" -ForegroundColor Yellow
        
        # Export the key to a .env file in the project root for compatibility
        if (-not (Test-Path (Join-Path $currentDir ".env"))) {
            "OPENAI_API_KEY=$apiKey" | Out-File -FilePath (Join-Path $currentDir ".env") -Encoding utf8
            Write-Host "Created .env file in project root with OpenAI API key" -ForegroundColor Green
        }
        
        # Check if the server is running
        $existingProcess = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($existingProcess) {
            Write-Host "Would you like to restart the server to apply the API key change? (y/n)" -ForegroundColor Yellow
            $answer = Read-Host
            
            if ($answer -eq 'y' -or $answer -eq 'Y') {
                Write-Host "Restarting server..." -ForegroundColor Yellow
                Stop-Process -Id $existingProcess -Force
                Start-Sleep -Seconds 2
                Start-Process powershell -ArgumentList "-Command cd $currentDir; python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal
                Write-Host "Server has been restarted with the updated API key." -ForegroundColor Green
            }
        }
    } else {
        Write-Host "Could not find OPENAI_API_KEY in .env file" -ForegroundColor Red
    }
} else {
    Write-Host "Could not find .env file at $envFilePath" -ForegroundColor Red
}

Write-Host "`nVerify that the OpenAI API key is now being used correctly by testing the API endpoints." -ForegroundColor Cyan

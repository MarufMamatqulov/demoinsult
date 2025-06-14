# Set OpenAI API Key as an environment variable
$apiKey = Read-Host -Prompt "Enter your OpenAI API Key" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey)
$apiKeyPlaintext = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
[Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $apiKeyPlaintext, 'User')
Write-Host "OpenAI API Key has been set as a user environment variable." -ForegroundColor Green
Write-Host "Please restart any open terminal windows for the change to take effect." -ForegroundColor Yellow

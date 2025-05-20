# Test deployment of InsultMedAI

# Set the EC2 IP address
$EC2_IP = "16.170.244.228"
$API_BASE_URL = "http://$EC2_IP`:8000"

Write-Host "🔍 Testing InsultMedAI deployment..." -ForegroundColor Cyan
Write-Host "API Base URL: $API_BASE_URL" -ForegroundColor Yellow

# Check if npm is available
$npmAvailable = $null
try {
    $npmAvailable = Get-Command npm -ErrorAction SilentlyContinue
} catch {
    $npmAvailable = $null
}

# Check if curl is available
$curlAvailable = $null
try {
    $curlAvailable = Get-Command curl -ErrorAction SilentlyContinue
} catch {
    $curlAvailable = $null
}

# Function to test API health
function Test-ApiHealth {
    Write-Host "`n📡 Testing API health..." -ForegroundColor Cyan
    
    if ($curlAvailable) {
        try {
            $response = curl -s "$API_BASE_URL/docs" -UseBasicParsing
            $statusCode = $LASTEXITCODE
            
            if ($statusCode -eq 0) {
                Write-Host "✅ API is responding!" -ForegroundColor Green
                return $true
            } else {
                Write-Host "❌ API is not responding. Status code: $statusCode" -ForegroundColor Red
                return $false
            }
        } catch {
            Write-Host "❌ Error connecting to API: $_" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "⚠️ curl command not found. Skipping API health check." -ForegroundColor Yellow
        return $false
    }
}

# Function to test PHQ9 endpoint
function Test-Phq9Endpoint {
    Write-Host "`n📡 Testing PHQ-9 endpoint..." -ForegroundColor Cyan
    
    if ($curlAvailable) {
        try {
            $data = @{
                answers = @(1, 1, 2, 1, 0, 1, 0, 1, 1)
                language = "en"
            } | ConvertTo-Json
            
            $response = curl -s -X POST "$API_BASE_URL/phq/analyze" -H "Content-Type: application/json" -d $data
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ PHQ-9 endpoint is working!" -ForegroundColor Green
                Write-Host "Response: $response" -ForegroundColor Gray
                return $true
            } else {
                Write-Host "❌ PHQ-9 endpoint failed. Status code: $LASTEXITCODE" -ForegroundColor Red
                return $false
            }
        } catch {
            Write-Host "❌ Error testing PHQ-9 endpoint: $_" -ForegroundColor Red
            return $false
        }
    } else {
        # Try using the node.js test script if available
        if ($npmAvailable -and (Test-Path "c:\Users\Marufjon\InsultMedAI\api_test.js")) {
            Write-Host "🔄 Using Node.js script for API testing..." -ForegroundColor Yellow
            node "c:\Users\Marufjon\InsultMedAI\api_test.js" "$API_BASE_URL"
            return $LASTEXITCODE -eq 0
        } else {
            Write-Host "⚠️ curl command not found and no alternative test method available." -ForegroundColor Yellow
            return $false
        }
    }
}

# Function to verify environment configuration
function Test-EnvironmentConfig {
    Write-Host "`n📋 Checking environment configuration..." -ForegroundColor Cyan
    
    # Check frontend .env.production
    if (Test-Path "c:\Users\Marufjon\InsultMedAI\frontend\.env.production") {
        $envContent = Get-Content "c:\Users\Marufjon\InsultMedAI\frontend\.env.production" -Raw
        if ($envContent -like "*$EC2_IP*") {
            Write-Host "✅ Frontend .env.production contains correct EC2 IP" -ForegroundColor Green
        } else {
            Write-Host "❌ Frontend .env.production does not contain correct EC2 IP" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Frontend .env.production file not found" -ForegroundColor Red
    }
    
    # Check vercel.json
    if (Test-Path "c:\Users\Marufjon\InsultMedAI\frontend\vercel.json") {
        $vercelContent = Get-Content "c:\Users\Marufjon\InsultMedAI\frontend\vercel.json" -Raw
        if ($vercelContent -like "*$EC2_IP*") {
            Write-Host "✅ vercel.json contains correct EC2 IP" -ForegroundColor Green
        } else {
            Write-Host "❌ vercel.json does not contain correct EC2 IP" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ vercel.json file not found" -ForegroundColor Red
    }
    
    # Check deploy-backend.ps1
    if (Test-Path "c:\Users\Marufjon\InsultMedAI\deploy-backend.ps1") {
        $deployContent = Get-Content "c:\Users\Marufjon\InsultMedAI\deploy-backend.ps1" -Raw
        if ($deployContent -like "*$EC2_IP*") {
            Write-Host "✅ deploy-backend.ps1 contains correct EC2 IP" -ForegroundColor Green
        } else {
            Write-Host "❌ deploy-backend.ps1 contains YOUR_EC2_IP placeholders" -ForegroundColor Red
        }
    }
}

# Run tests
$apiHealthOk = Test-ApiHealth
$phq9EndpointOk = Test-Phq9Endpoint
Test-EnvironmentConfig

# Final report
Write-Host "`n📋 Deployment Test Summary:" -ForegroundColor Cyan
if ($apiHealthOk) {
    Write-Host "✅ API Health: PASSED" -ForegroundColor Green
} else {
    Write-Host "❌ API Health: FAILED" -ForegroundColor Red
}

if ($phq9EndpointOk) {
    Write-Host "✅ PHQ-9 Endpoint: PASSED" -ForegroundColor Green
} else {
    Write-Host "❌ PHQ-9 Endpoint: FAILED" -ForegroundColor Red
}

# Next steps
Write-Host "`n🚀 Next Steps:" -ForegroundColor Cyan
if ($apiHealthOk -and $phq9EndpointOk) {
    Write-Host "1. Deploy the frontend to Vercel using .\fix-vercel-deploy.ps1" -ForegroundColor Green
    Write-Host "2. Test the complete application by accessing your Vercel URL" -ForegroundColor Green
} else {
    Write-Host "1. Fix any issues with the backend deployment" -ForegroundColor Yellow
    Write-Host "2. Run .\deploy-backend.ps1 to redeploy the backend" -ForegroundColor Yellow
    Write-Host "3. Run this test script again to verify the backend is working" -ForegroundColor Yellow
}

# Clear browser cache instructions for testing the profile page

function Clear-BrowserCache {
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host "  BROWSER CACHE CLEARING INSTRUCTIONS" -ForegroundColor Cyan
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To properly test the profile page fixes, please clear your browser cache:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Chrome:" -ForegroundColor Green
    Write-Host "1. Press Ctrl+Shift+Delete"
    Write-Host "2. Set time range to 'All time'"
    Write-Host "3. Select 'Cookies and other site data' and 'Cached images and files'"
    Write-Host "4. Click 'Clear data'"
    Write-Host ""
    Write-Host "Firefox:" -ForegroundColor Green
    Write-Host "1. Press Ctrl+Shift+Delete"
    Write-Host "2. Set time range to 'Everything'"
    Write-Host "3. Select 'Cookies' and 'Cache'"
    Write-Host "4. Click 'Clear Now'"
    Write-Host ""
    Write-Host "Edge:" -ForegroundColor Green
    Write-Host "1. Press Ctrl+Shift+Delete"
    Write-Host "2. Select 'All time' as the time range"
    Write-Host "3. Check 'Cookies and other site data' and 'Cached images and files'"
    Write-Host "4. Click 'Clear now'"
    Write-Host ""
    Write-Host "Alternatively, try using an Incognito/Private window for testing" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "After clearing cache, restart the frontend application:"
    Write-Host ""
    
    $restart = Read-Host "Would you like to restart the frontend now? (y/n)"
    if ($restart -eq "y") {
        Write-Host "Restarting frontend application..." -ForegroundColor Cyan
        # Change directory to frontend
        Push-Location -Path ".\frontend"
        
        # Stop any running processes (adjust as needed)
        # This is a simplified example
        try {
            npm run build
            npm start
        }
        catch {
            Write-Host "Error restarting frontend. Please restart it manually." -ForegroundColor Red
        }
        
        # Go back to original directory
        Pop-Location
    }
    else {
        Write-Host "Please restart the frontend application manually when ready." -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "After restarting the frontend, try accessing the profile page again." -ForegroundColor Cyan
}

# Run the function
Clear-BrowserCache

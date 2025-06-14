# Verify Email Configuration for Stroke Rehabilitation AI Platform
Write-Host "Starting Email Configuration Verification..." -ForegroundColor Cyan

# Make sure Python environment is activated
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating Python virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
} elseif (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating Python virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "No virtual environment found. Proceeding with system Python..." -ForegroundColor Yellow
}

# Ensure required packages are installed
Write-Host "Checking required packages..." -ForegroundColor Yellow
pip install requests python-dotenv -q

# Create a test email verification script
$testEmailScriptPath = "tests\verify_email_config.py"

Write-Host "Creating test email verification script..." -ForegroundColor Yellow
@"
import os
from dotenv import load_dotenv
import logging
import sys
from backend.utils.email_utils import send_email, EMAIL_USER, EMAIL_PASSWORD, EMAIL_HOST, EMAIL_PORT, EMAIL_FROM

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('email_verification.log')
    ]
)

def verify_email_config():
    """Verify email configuration by checking settings and sending a test email."""
    # Check if email settings are configured
    logging.info("Checking email configuration...")
    logging.info(f"EMAIL_HOST: {EMAIL_HOST}")
    logging.info(f"EMAIL_PORT: {EMAIL_PORT}")
    logging.info(f"EMAIL_USER: {'Configured' if EMAIL_USER else 'Not configured'}")
    logging.info(f"EMAIL_PASSWORD: {'Configured' if EMAIL_PASSWORD else 'Not configured'}")
    logging.info(f"EMAIL_FROM: {EMAIL_FROM}")
    
    if not EMAIL_USER or not EMAIL_PASSWORD:
        logging.error("Email credentials missing. Please set EMAIL_USER and EMAIL_PASSWORD.")
        return False
    
    # Send test email to yourself
    logging.info(f"Sending test email from {EMAIL_FROM} to {EMAIL_USER}...")
    
    subject = "InsultMedAI - Email Configuration Test"
    html_content = """
    <html>
    <body>
        <h2>Email Configuration Test</h2>
        <p>This is a test email sent by the InsultMedAI email verification script.</p>
        <p>If you're receiving this email, your email configuration is working correctly!</p>
    </body>
    </html>
    """
    text_content = "Email Configuration Test\n\nThis is a test email sent by the InsultMedAI email verification script.\n\nIf you're receiving this email, your email configuration is working correctly!"
    
    try:
        result = send_email(EMAIL_USER, subject, html_content, text_content)
        if result:
            logging.info("Test email sent successfully!")
            return True
        else:
            logging.error("Failed to send test email.")
            return False
    except Exception as e:
        logging.error(f"Error sending test email: {str(e)}")
        return False

if __name__ == "__main__":
    # Try to load environment variables from .env file
    load_dotenv()
    
    # Run verification
    success = verify_email_config()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
"@ | Out-File -FilePath $testEmailScriptPath -Encoding utf8

# Run the verification script
Write-Host "Running email configuration verification..." -ForegroundColor Cyan
python $testEmailScriptPath
$emailVerificationExitCode = $LASTEXITCODE

# Check if verification was successful
if ($emailVerificationExitCode -eq 0) {
    Write-Host "Email configuration is working correctly!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "Email configuration has issues. Check the logs for details." -ForegroundColor Red
    exit 1
}

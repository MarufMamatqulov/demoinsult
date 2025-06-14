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

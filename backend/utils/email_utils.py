"""Email utilities for sending verification emails and password reset emails."""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict

# Load email configuration from environment variables
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USER if EMAIL_USER else "noreply@strokerehabai.com")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Try to load variables from .env file if they're not set
if not EMAIL_USER or not EMAIL_PASSWORD:
    try:
        from dotenv import load_dotenv
        # Try to load from project root .env and then from backend/.env
        load_dotenv()
        # Check if variables are now available
        EMAIL_USER = os.getenv("EMAIL_USER", EMAIL_USER)
        EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", EMAIL_PASSWORD)
        EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USER if EMAIL_USER else EMAIL_FROM)
    except ImportError:
        print("python-dotenv not installed, using environment variables only")

def send_email(to_email: str, subject: str, html_content: str, text_content: str = None) -> bool:
    """
    Send an email with HTML and optional text content.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        text_content: Plain text content of the email (optional)
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("Email configuration missing. Please set EMAIL_USER and EMAIL_PASSWORD environment variables.")
        return False
        
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    
    # Add text content if provided, otherwise create a simple version from HTML
    if text_content is None:
        # Very basic HTML to text conversion
        text_content = html_content.replace('<br>', '\n').replace('</p>', '\n').replace('<p>', '')
        # Strip remaining HTML tags
        import re
        text_content = re.sub('<[^<]+?>', '', text_content)
    
    # Attach parts
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')
    msg.attach(part1)
    msg.attach(part2)
    
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_verification_email(to_email: str, token: str) -> bool:
    """
    Send a verification email to the user.
    
    Args:
        to_email: User's email address
        token: Verification token
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    verification_link = f"{FRONTEND_URL}/verify-email?token={token}"
    
    subject = "Verify Your Email - Stroke Rehabilitation AI Platform"
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #004d99; color: white; padding: 15px; text-align: center; }}
            .content {{ padding: 20px; border: 1px solid #ddd; }}
            .button {{ display: inline-block; padding: 10px 20px; background-color: #004d99; color: white; 
                      text-decoration: none; border-radius: 5px; margin-top: 15px; }}
            .footer {{ margin-top: 20px; font-size: 12px; color: #777; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Stroke Rehabilitation AI Platform</h1>
            </div>
            <div class="content">
                <h2>Verify Your Email Address</h2>
                <p>Thank you for registering with the Stroke Rehabilitation AI Platform. Please verify your email address to continue.</p>
                <p>Click the button below to verify your email:</p>
                <p><a href="{verification_link}" class="button">Verify Email</a></p>
                <p>Or copy and paste this link into your browser:</p>
                <p>{verification_link}</p>
                <p>This link will expire in 24 hours.</p>
                <p>If you did not create an account, please ignore this email.</p>
            </div>
            <div class="footer">
                <p>© {2025} Stroke Rehabilitation AI Platform. All rights reserved.</p>
                <p>This is an automated message. Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(to_email, subject, html_content)

def send_password_reset_email(to_email: str, token: str) -> bool:
    """
    Send a password reset email to the user.
    
    Args:
        to_email: User's email address
        token: Password reset token
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    reset_link = f"{FRONTEND_URL}/reset-password?token={token}"
    
    subject = "Reset Your Password - Stroke Rehabilitation AI Platform"
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #004d99; color: white; padding: 15px; text-align: center; }}
            .content {{ padding: 20px; border: 1px solid #ddd; }}
            .button {{ display: inline-block; padding: 10px 20px; background-color: #004d99; color: white; 
                      text-decoration: none; border-radius: 5px; margin-top: 15px; }}
            .footer {{ margin-top: 20px; font-size: 12px; color: #777; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Stroke Rehabilitation AI Platform</h1>
            </div>
            <div class="content">
                <h2>Reset Your Password</h2>
                <p>We received a request to reset your password. Click the button below to create a new password:</p>
                <p><a href="{reset_link}" class="button">Reset Password</a></p>
                <p>Or copy and paste this link into your browser:</p>
                <p>{reset_link}</p>
                <p>This link will expire in 1 hour.</p>
                <p>If you did not request a password reset, please ignore this email or contact support if you have concerns.</p>
            </div>
            <div class="footer">
                <p>© {2025} Stroke Rehabilitation AI Platform. All rights reserved.</p>
                <p>This is an automated message. Please do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(to_email, subject, html_content)

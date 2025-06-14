## Environment Variables for Email Configuration

To enable email verification and password reset functionality in the Stroke Rehabilitation AI Platform, you need to configure the following environment variables:

### Backend Environment Variables (`.env` file in backend directory)

```bash
# JWT Configuration
JWT_SECRET_KEY=your_secure_jwt_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days in minutes

# Email Configuration
EMAIL_HOST=smtp.gmail.com  # Replace with your SMTP server
EMAIL_PORT=587  # Common SMTP port, adjust if needed
EMAIL_USER=your_email@example.com  # Email address to send from
EMAIL_PASSWORD=your_email_password_or_app_password  # Password or app password
EMAIL_FROM=noreply@strokerehabai.com  # Display name for emails
EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS=24
PASSWORD_RESET_TOKEN_EXPIRE_HOURS=1

# Frontend URL (for email links)
FRONTEND_URL=http://localhost:3000  # Update for production
```

### Frontend Environment Variables (`.env` file in frontend directory)

```bash
# API URL
REACT_APP_API_URL=http://localhost:8000  # Update for production

# Google OAuth (if using Google login)
REACT_APP_GOOGLE_CLIENT_ID=your_google_client_id
```

### Notes on Email Configuration:

1. **For Gmail users**:
   - You need to enable "Less secure app access" or use an "App Password" if you have 2FA enabled
   - Generate an app password at: https://myaccount.google.com/apppasswords

2. **For production deployment**:
   - Use environment-specific variables for different environments
   - Consider using a transactional email service like SendGrid, Mailgun, or Amazon SES

3. **Testing email functionality**:
   - You can use services like Mailtrap (https://mailtrap.io) for testing emails in development
   - Update EMAIL_HOST, EMAIL_PORT, EMAIL_USER, and EMAIL_PASSWORD accordingly

4. **Security considerations**:
   - Never commit .env files to version control
   - Use secure, random strings for JWT_SECRET_KEY
   - Rotate email credentials periodically for security

### Troubleshooting

If emails are not being sent:
1. Check that all environment variables are set correctly
2. Verify SMTP server settings
3. Check server logs for email sending errors
4. Test SMTP connection from command line
5. Check spam/junk folders when testing email delivery

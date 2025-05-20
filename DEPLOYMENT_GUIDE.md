# InsultMedAI Deployment Guide

This guide provides step-by-step instructions for deploying the InsultMedAI application with:
- Backend running on AWS EC2
- Frontend hosted on Vercel

## Prerequisites

- AWS EC2 instance (t2.micro or better)
- AWS EC2 key pair (.pem file)
- GitHub account (for Vercel integration)
- Vercel account

## Step 1: Deploy Backend to EC2

1. **✅ Update the EC2 IP address in all necessary files**:
   
   Replace `YOUR_EC2_IP` with your actual EC2 public IP address in these files:
   - `deploy-backend.ps1`
   - `frontend/.env.production`
   - `frontend/vercel.json`

2. **✅ Run the deployment script**:
   
   Open PowerShell and run:
   ```powershell
   cd c:\Users\Marufjon\InsultMedAI
   .\deploy-backend.ps1
   ```

3. **✅ Verify backend deployment**:
   
   After the script completes, open your browser and visit:
   ```
   http://YOUR_EC2_IP:8000/docs
   ```
   You should see the FastAPI Swagger documentation page.

## Step 2: Deploy Frontend to Vercel

1. **Prepare for deployment**:
   
   Make sure git is installed and initialize a git repository if not already done:
   ```bash
   cd c:\Users\Marufjon\InsultMedAI
   git init
   git add .
   git commit -m "Initial commit for deployment"
   ```

2. **Create a GitHub repository**:
   
   - Go to GitHub and create a new repository
   - Follow GitHub instructions to push your existing repository

3. **Deploy using Vercel**:
   
   a. Log in to Vercel (https://vercel.com)
   b. Click "New Project"
   c. Import your GitHub repository
   d. Configure the project:
      - Framework Preset: Create React App
      - Root Directory: frontend
      - Build Command: npm run build
      - Output Directory: build
      - Install Command: npm install
   
   e. Add environment variables:
      - REACT_APP_API_URL: http://YOUR_EC2_IP:8000
   
   f. Click "Deploy"

4. **Verify frontend deployment**:
   
   Once deployment is complete, Vercel will provide a URL for your frontend application.
   
   Open the URL in your browser to verify that the frontend is working correctly.

## Step 3: Test the Complete Deployment

1. **Test the application end-to-end**:
   
   - Navigate to the Vercel-provided URL
   - Try submitting a PHQ-9 form
   - Ensure that the form data is sent to the backend and analyzed correctly
   - Verify that the results are displayed correctly

## Troubleshooting

### Backend Issues

1. **Check service status**:
   ```bash
   sudo systemctl status insultmedai
   ```

2. **View logs**:
   ```bash
   sudo journalctl -u insultmedai -f
   ```

3. **Restart the service**:
   ```bash
   sudo systemctl restart insultmedai
   ```

4. **Check EC2 security group**:
   - Ensure port 8000 is open for incoming connections

### Frontend Issues

1. **Check Vercel deployment logs**:
   - On your Vercel dashboard, navigate to your project
   - Click on the latest deployment
   - View the deployment logs

2. **Verify environment variables**:
   - Check that REACT_APP_API_URL is set correctly

3. **CORS issues**:
   - Verify that the backend CORS settings allow requests from your Vercel domain
   - You may need to update the backend with:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-vercel-app.vercel.app"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

## Security Considerations

1. **API Key Protection**:
   - Consider using a more secure method to store your OpenAI API key
   - AWS Secrets Manager or environment variables are recommended

2. **Restrict Access**:
   - Consider implementing authentication for the API
   - Limit CORS to only allow requests from your Vercel domain

## Future Improvements

1. **Add HTTPS to backend**:
   - Consider using a reverse proxy like Nginx with Let's Encrypt

2. **Implement user authentication**:
   - Add login/registration functionality
   - Protect sensitive endpoints

3. **Set up monitoring**:
   - Implement health checks and monitoring for the backend service

---

For any questions or issues, please contact the development team.

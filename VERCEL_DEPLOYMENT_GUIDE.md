# Vercel Deployment Guide

This guide provides detailed steps for deploying your InsultMedAI application frontend to Vercel.

## Prerequisites

Before you start, make sure you have:

1. Successfully deployed the backend to EC2 (IP: 16.170.244.228)
2. Fixed all dependency issues in the frontend code

## TypeScript Dependency Issue Fix

If you're seeing the error with TypeScript and i18next dependencies, follow these steps:

1. Update `package.json` resolutions to include i18next:
```json
"resolutions": {
  "typescript": "4.9.5",
  "@types/react": "18.2.15",
  "i18next": "22.5.0"
}
```

2. Make sure `.npmrc` file in your frontend directory contains:
```
legacy-peer-deps=true
```
3. A GitHub account (recommended for easier Vercel deployment)
4. A Vercel account (sign up at https://vercel.com if you don't have one)

## Option 1: Deploy via Vercel Dashboard (Recommended)

### Step 1: Push Your Code to GitHub

If your code is not already in a GitHub repository:

```powershell
# Navigate to your project directory
cd c:\Users\Marufjon\InsultMedAI

# Initialize git repository if not already done
git init

# Add files (excluding node_modules and other unnecessary files)
git add .
git commit -m "Ready for Vercel deployment"

# Connect to your GitHub repository
git remote add origin https://github.com/yourusername/InsultMedAI.git
git push -u origin main
```

### Step 2: Import Your Project in Vercel

1. Go to https://vercel.com/new
2. Connect your GitHub account if not already connected
3. Select your InsultMedAI repository
4. Configure the project:
   - **Framework Preset**: Create React App
   - **Root Directory**: frontend
   - **Build Command**: npm run build
   - **Output Directory**: build
   - **Install Command**: npm install --legacy-peer-deps

5. Add the environment variable:
   - Name: `REACT_APP_API_URL`
   - Value: `http://16.170.244.228:8000`

6. Click "Deploy"

### Step 3: Monitor Deployment

Vercel will show a progress indicator during deployment. Once complete, you'll get a URL for your frontend application.

## Option 2: Deploy using Vercel CLI

### Step 1: Install Vercel CLI

```powershell
npm install -g vercel
```

### Step 2: Run the Deployment Script

We've created a script that handles the deployment process:

```powershell
# Navigate to your project directory
cd c:\Users\Marufjon\InsultMedAI

# Run the fix script first to ensure dependencies are compatible
.\fix-vercel-deploy.ps1

# Deploy to Vercel
.\deploy-to-vercel.ps1
```

## Option 3: Manual Deployment with Vercel CLI

If you prefer to manually control the deployment process:

```powershell
# Navigate to the frontend directory
cd c:\Users\Marufjon\InsultMedAI\frontend

# Login to Vercel
vercel login

# Deploy to Vercel
vercel --prod
```

During the interactive setup, you'll be asked several questions:
- Set the build directory to `frontend`
- Set the environment variable `REACT_APP_API_URL` to `http://16.170.244.228:8000`

## Troubleshooting

### Dependency Issues

If you encounter dependency issues during deployment:

1. Run the fix-dependencies script:
   ```powershell
   cd c:\Users\Marufjon\InsultMedAI\frontend
   .\fix-dependencies.ps1
   ```

2. If specific errors persist, you can force the installation:
   ```powershell
   npm install --force
   ```

### Build Errors

If your build fails, check the following:

1. TypeScript errors - These must be fixed in your code
2. Dependencies compatibility - Make sure versions are compatible
3. Environment variables - Verify they are correctly set

### CORS Issues

If your deployed frontend cannot communicate with the backend:

1. Check that the backend CORS settings allow requests from your Vercel domain
2. Verify that the EC2 security group allows incoming traffic on port 8000

## After Successful Deployment

1. Test your application thoroughly by performing some basic operations
2. Monitor the backend logs for any errors:
   ```powershell
   ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo journalctl -u insultmedai -f"
   ```

3. Set up monitoring and alerting for your production environment

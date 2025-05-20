# InsultMedAI Deployment Checklist

## Pre-Deployment Steps

### Backend Preparation
- [x] Fixed duplicate CORS middleware in backend/main.py
- [x] Updated requirements.txt with all necessary dependencies
- [x] Created systemd service file for backend (insultmedai.service)
- [x] Created deployment script for backend (deploy-backend.ps1)
- [x] Verified OpenAI API key is correctly set in the systemd service file

### Frontend Preparation
- [x] Created API configuration utility (frontend/src/config/api.js)
- [x] Updated all components to use the API configuration instead of hardcoded URLs
- [x] Created environment files (.env, .env.development, .env.production)
- [x] Created Vercel configuration (vercel.json)
- [x] Added CORS headers to the Vercel configuration

## Deployment Instructions

### Step 1: Deploy Backend
1. [x] Replace YOUR_EC2_IP with your actual EC2 IP address (16.170.244.228) in:
   - deploy-backend.ps1
   - frontend/.env.production
   - frontend/vercel.json
   
2. [x] Run backend deployment script:
   ```powershell
   cd c:\Users\Marufjon\InsultMedAI
   .\deploy-backend.ps1
   ```
   
3. [x] Verify backend is running:
   ```
   http://16.170.244.228:8000/docs
   ```

### Step 2: Deploy Frontend
1. [ ] Fix dependency conflicts:
   ```powershell
   cd c:\Users\Marufjon\InsultMedAI
   .\fix-vercel-deploy.ps1
   ```

2. [ ] Test API connectivity:
   ```powershell
   cd c:\Users\Marufjon\InsultMedAI
   .\test-deployment.ps1
   ```

3. [ ] Push your code to GitHub:
   ```powershell
   git init
   git remote add origin YOUR_GITHUB_REPO_URL
   git add .
   git commit -m "Ready for deployment"
   git push -u origin main
   ```
   
4. [ ] Deploy on Vercel:
   - Create new project on Vercel
   - Connect to your GitHub repository
   - Configure build settings:
     - Root Directory: frontend
     - Build Command: npm run build
     - Output Directory: build
     - Install Command: npm install --legacy-peer-deps
   - Add environment variables:
     - REACT_APP_API_URL: http://16.170.244.228:8000
   - Deploy

5. [ ] Verify frontend deployment:
   - Open the Vercel URL
   - Test the PHQ-9 form and other features

## Post-Deployment Tasks
1. [ ] Update production CORS settings in backend/main.py:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-vercel-app.vercel.app"],  # Replace with your Vercel domain
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. [ ] Set up monitoring and alerts:
   - [ ] CPU/memory monitoring for EC2
   - [ ] API endpoint monitoring
   - [ ] Error logging

3. [ ] Implement security enhancements:
   - [ ] Move OpenAI API key to AWS Secrets Manager
   - [ ] Add authentication to the API
   - [ ] Set up HTTPS for the backend

4. [ ] Create backup strategy for:
   - [ ] Database/file storage
   - [ ] Application configurations

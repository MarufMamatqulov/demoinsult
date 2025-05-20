#!/bin/bash
# Run this script on your EC2 instance to update CORS settings

cat > ~/InsultMedAI/backend/main.py.new << 'EOL'
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
# ... keep existing imports

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Vercel domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... rest of your main.py file
EOL

# Backup the original file
cp ~/InsultMedAI/backend/main.py ~/InsultMedAI/backend/main.py.backup

# Replace the beginning of the file but keep everything after the app = FastAPI() line
head -n 10 ~/InsultMedAI/backend/main.py.new > ~/InsultMedAI/backend/main.py.tmp
tail -n +3 ~/InsultMedAI/backend/main.py >> ~/InsultMedAI/backend/main.py.tmp
mv ~/InsultMedAI/backend/main.py.tmp ~/InsultMedAI/backend/main.py

# Restart the service
sudo systemctl restart insultmedai

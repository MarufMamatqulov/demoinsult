# Deploy Backend to EC2
# The EC2 public IP address is: 16.170.244.228 (as of May 20, 2025)

# Step 1: Connect to EC2
Write-Host "Connecting to EC2 instance..." -ForegroundColor Green
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "echo 'Connected to EC2 instance'"

# Step 2: Clean up instance and kill any running processes
Write-Host "Cleaning up instance..." -ForegroundColor Green
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo pkill -f python || true"
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo docker-compose down || true"
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo docker system prune -af || true"

# Step 3: Transfer the project files
Write-Host "Transferring project files..." -ForegroundColor Green
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "rm -rf ~/InsultMedAI"
cd c:\Users\Marufjon
tar --exclude=InsultMedAI/frontend/node_modules --exclude=InsultMedAI/.git -czf InsultMedAI.tar.gz InsultMedAI
scp -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" InsultMedAI.tar.gz ubuntu@16.170.244.228:~/
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "tar -xzf InsultMedAI.tar.gz -C ~/ && rm InsultMedAI.tar.gz"

# Step 4: Setup Python environment and install dependencies
Write-Host "Setting up Python environment..." -ForegroundColor Green
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo apt update && sudo apt install -y python3-venv"
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "rm -rf ~/insultmedai_venv"
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "python3 -m venv ~/insultmedai_venv"
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "source ~/insultmedai_venv/bin/activate && pip install -r ~/InsultMedAI/requirements.txt"
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "source ~/insultmedai_venv/bin/activate && pip install python-multipart requests pydantic-settings"

# Step 5: Create startup script and set up the systemd service
Write-Host "Creating startup script..." -ForegroundColor Green
$startupScript = @"
#!/bin/bash
cd ~/InsultMedAI
source ~/insultmedai_venv/bin/activate
export PYTHONPATH=~/InsultMedAI
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
"@
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "echo '$startupScript' > ~/InsultMedAI/start_backend.sh"
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "chmod +x ~/InsultMedAI/start_backend.sh"

Write-Host "Setting up systemd service..." -ForegroundColor Green
$systemdService = @"
[Unit]
Description=InsultMedAI Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/InsultMedAI
ExecStart=/home/ubuntu/InsultMedAI/start_backend.sh
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=insultmedai
Environment=PYTHONPATH=/home/ubuntu/InsultMedAI

[Install]
WantedBy=multi-user.target
"@
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "echo '$systemdService' | sudo tee /etc/systemd/system/insultmedai.service > /dev/null"
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo systemctl daemon-reload"
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo systemctl enable insultmedai"
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo systemctl start insultmedai"

# Step 6: Check if the service is running
Write-Host "Checking service status..." -ForegroundColor Green
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo systemctl status insultmedai"

Write-Host "Backend deployment complete! The API should be available at: http://16.170.244.228:8000" -ForegroundColor Green
Write-Host "⚠️ Make sure to update the EC2 IP address in the frontend .env file and vercel.json before deploying the frontend!" -ForegroundColor Yellow

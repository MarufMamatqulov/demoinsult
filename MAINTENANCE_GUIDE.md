# Maintenance Guide for InsultMedAI Deployment

This guide provides instructions for maintaining your InsultMedAI application after successful deployment.

## Deployment Architecture

Your InsultMedAI application is deployed with:

- **Backend**: Running on AWS EC2 instance (IP: 16.170.244.228)
- **Frontend**: Hosted on Vercel

## Monitoring Your Application

### Backend Monitoring

1. **Check service status**:
   ```powershell
   ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo systemctl status insultmedai"
   ```

2. **View logs**:
   ```powershell
   ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo journalctl -u insultmedai -n 100"
   ```

   For real-time logs:
   ```powershell
   ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo journalctl -u insultmedai -f"
   ```

3. **Check server resources**:
   ```powershell
   ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "top -b -n 1"
   ```

### Frontend Monitoring

1. Visit your Vercel dashboard to:
   - View deployment status
   - Check usage metrics
   - Monitor error reports

## Common Maintenance Tasks

### Restarting the Backend Service

If you need to restart the backend:

```powershell
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo systemctl restart insultmedai"
```

### Updating the Backend Code

1. Make your code changes locally
2. Run the deployment script:
   ```powershell
   .\deploy-backend.ps1
   ```

### Updating the Frontend Code

1. Make your code changes locally
2. Test locally:
   ```powershell
   cd frontend
   npm start
   ```
3. Commit and push to GitHub:
   ```powershell
   git add .
   git commit -m "Updated frontend code"
   git push
   ```
4. Vercel will automatically redeploy if you've set up continuous deployment

## Database Backup

If you've added a database to your application:

```powershell
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "pg_dump -U dbuser -d insultmedai > ~/backups/insultmedai_$(date +%Y%m%d).sql"
```

## Security Maintenance

### Updating Dependencies

Regularly update dependencies to address security vulnerabilities:

**Backend**:
```powershell
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "cd ~/InsultMedAI && source ~/insultmedai_venv/bin/activate && pip list --outdated"
```

**Frontend**:
```powershell
cd frontend
npm outdated
npm update
```

### EC2 Security Updates

Keep your EC2 instance updated:

```powershell
ssh -i "c:\Users\Marufjon\InsultMedAI\ec2-kp.pem" ubuntu@16.170.244.228 "sudo apt update && sudo apt upgrade -y"
```

## Troubleshooting

### Backend Issues

1. **API not responding**:
   - Check if the service is running
   - Review logs for errors
   - Check if the EC2 instance is healthy

2. **High server load**:
   - Check resource usage with `top`
   - Consider scaling up your EC2 instance

### Frontend Issues

1. **CORS errors**:
   - Verify CORS settings in the backend
   - Check if the EC2 IP address is correct in the frontend configuration

2. **Loading failures**:
   - Check browser console for JavaScript errors
   - Verify API connectivity

## Recommended Maintenance Schedule

- **Daily**: Check application status
- **Weekly**: Review logs for issues
- **Monthly**: Update dependencies, apply security patches
- **Quarterly**: Comprehensive review of performance and security

## Future Enhancements

Consider these improvements to your deployment:

1. Set up automatic backups
2. Implement monitoring tools (e.g., CloudWatch)
3. Add HTTPS to your backend with a custom domain
4. Set up alerting for service disruptions

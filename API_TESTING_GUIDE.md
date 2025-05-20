# API Testing Guide after Deployment

After deploying the InsultMedAI backend to EC2, you should verify that the API is working correctly. This guide provides simple cURL commands and a JavaScript test file to test various endpoints.

## Prerequisites
- Your EC2 instance IP address
- cURL (for command-line testing)
- Node.js (for running the JavaScript test file)

## Basic Health Check

### Using cURL
```bash
curl http://YOUR_EC2_IP:8000/
```

Expected response:
```json
{"status": "ok", "message": "InsultMedAI API is running"}
```

## Testing PHQ-9 Endpoint

### Using cURL
```bash
curl -X POST http://YOUR_EC2_IP:8000/phq/analyze \
  -H "Content-Type: application/json" \
  -d '{"answers": [1, 1, 1, 1, 1, 1, 1, 1, 1], "language": "en"}'
```

### Using the provided test script
You can also use the provided JavaScript test file to test the PHQ-9 endpoint:

1. Update the EC2 IP address in the test file:

```javascript
// In test_chat_api.js
const API_URL = 'http://YOUR_EC2_IP:8000';
```

2. Run the test script:

```bash
node test_chat_api.js
```

## Testing Audio Upload Endpoint

### Using cURL
```bash
curl -X POST http://YOUR_EC2_IP:8000/audio/upload \
  -F "file=@./test_audio.mp3" \
  -F "language=english" \
  -F "analysis_type=speech"
```

Note: You need to have a test audio file available.

## Testing NIHSS Endpoint

### Using cURL
```bash
curl -X POST http://YOUR_EC2_IP:8000/nihss/analyze \
  -H "Content-Type: application/json" \
  -d '{"scores": [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0], "language": "en"}'
```

## Troubleshooting

If you encounter issues with the API, here are some common troubleshooting steps:

1. **Check if the service is running**:
   ```bash
   sudo systemctl status insultmedai
   ```

2. **View the logs**:
   ```bash
   sudo journalctl -u insultmedai -n 100
   ```

3. **Restart the service**:
   ```bash
   sudo systemctl restart insultmedai
   ```

4. **Check port availability**:
   ```bash
   sudo netstat -tulnp | grep 8000
   ```

5. **Check the security group**:
   Make sure port 8000 is open in the EC2 security group settings.

6. **Test CORS configuration**:
   ```javascript
   fetch('http://YOUR_EC2_IP:8000/phq/analyze', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
     },
     body: JSON.stringify({
       answers: [1, 1, 1, 1, 1, 1, 1, 1, 1],
       language: 'en'
     })
   })
   .then(response => response.json())
   .then(data => console.log(data))
   .catch(error => console.error('Error:', error));
   ```
   Run this in your browser console from the deployed frontend application.

## Next Steps

After successfully testing the API, you should:

1. Update the frontend configuration with the correct EC2 IP address
2. Deploy the frontend to Vercel
3. Test the complete application with the frontend

Remember to refer to the `DEPLOYMENT_GUIDE.md` and `DEPLOYMENT_CHECKLIST.md` for complete deployment instructions.

// Test script for patient chat API
const http = require('http');

const data = JSON.stringify({
  messages: [
    {
      role: 'user',
      content: 'Salom, mening insultim haqida ma\'lumot bering'
    }
  ],
  patient_context: {},
  language: 'uz'
});

const options = {
  hostname: 'localhost',
  port: 8000,
  path: '/chat/patient-chat',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }
};

console.log('Testing patient chat API...');

const req = http.request(options, res => {
  console.log(`Status Code: ${res.statusCode}`);
  
  let responseData = '';
  
  res.on('data', chunk => {
    responseData += chunk;
  });
  
  res.on('end', () => {
    try {
      const parsedData = JSON.parse(responseData);
      console.log('API Response:', parsedData);
      
      if (parsedData.response) {
        console.log('✅ API is working correctly!');
      } else {
        console.error('❌ API response missing expected fields:', parsedData);
      }
    } catch (err) {
      console.error('❌ Error parsing response:', err);
    }
  });
});

req.on('error', error => {
  console.error('❌ Error connecting to API:', error);
});

req.write(data);
req.end();

console.log('Request sent! Waiting for response...');

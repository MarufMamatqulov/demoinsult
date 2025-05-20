// Test script for InsultMedAI API endpoints
const http = require('http');
const https = require('https');
const url = require('url');

// Get the API URL from command line arguments or use default
const API_URL = process.argv[2] || 'http://localhost:8000';
console.log(`Using API URL: ${API_URL}`);

// Parse the URL to get hostname, port, and protocol
const parsedUrl = url.parse(API_URL);
const isHttps = parsedUrl.protocol === 'https:';
const hostname = parsedUrl.hostname;
const port = parsedUrl.port || (isHttps ? 443 : 80);

// Test data for patient chat
const patientChatData = JSON.stringify({
  messages: [
    {
      role: 'user',
      content: 'Salom, mening insultim haqida ma\'lumot bering'
    }
  ],
  patient_context: {},
  language: 'uz'
});

// Test data for PHQ-9 analysis
const phqData = JSON.stringify({
  answers: [1, 1, 2, 1, 0, 1, 0, 1, 1],
  language: 'en'
});

// Configure options for the request
const patientChatOptions = {
  hostname: hostname,
  port: port,
  path: '/chat/patient-chat',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': patientChatData.length
  }
};

console.log('Testing patient chat API...');

// Test PHQ-9 endpoint
const phqOptions = {
  hostname: hostname,
  port: port,
  path: '/phq/analyze',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': phqData.length
  }
};

// Function to make an HTTP/HTTPS request
function makeRequest(options, data, testName) {
  console.log(`Testing ${testName}...`);
  
  const httpModule = isHttps ? https : http;
  const req = httpModule.request(options, res => {
    console.log(`[${testName}] Status Code: ${res.statusCode}`);
    
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

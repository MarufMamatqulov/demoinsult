/**
 * Test script for InsultMedAI API endpoints
 * Usage: node api_test.js [API_URL]
 * Example: node api_test.js http://54.123.45.678:8000
 */
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

// Test data for different endpoints
const testData = {
  phq: {
    path: '/phq/analyze',
    data: JSON.stringify({
      answers: [1, 1, 2, 1, 0, 1, 0, 1, 1],
      language: 'en'
    })
  },
  patientChat: {
    path: '/chat/patient-chat',
    data: JSON.stringify({
      messages: [
        {
          role: 'user',
          content: 'Salom, mening insultim haqida ma\'lumot bering'
        }
      ],
      patient_context: {},
      language: 'uz'
    })
  },
  nihss: {
    path: '/nihss/analyze',
    data: JSON.stringify({
      scores: [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
      language: 'en'
    })
  }
};

// Function to make an HTTP/HTTPS request
function makeRequest(endpoint, testData) {
  return new Promise((resolve, reject) => {
    console.log(`\n----- Testing ${endpoint} endpoint -----`);
    
    const options = {
      hostname: hostname,
      port: port,
      path: testData.path,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': testData.data.length
      }
    };
    
    const httpModule = isHttps ? https : http;
    const req = httpModule.request(options, res => {
      console.log(`Status Code: ${res.statusCode}`);
      
      let responseData = '';
      
      res.on('data', chunk => {
        responseData += chunk;
      });
      
      res.on('end', () => {
        try {
          const parsedData = JSON.parse(responseData);
          console.log('API Response:', JSON.stringify(parsedData, null, 2));
          resolve({success: true, data: parsedData});
        } catch (error) {
          console.error('Error parsing response:', error);
          console.log('Raw response:', responseData);
          resolve({success: false, error: error, raw: responseData});
        }
      });
    });

    req.on('error', error => {
      console.error('Error making request:', error);
      reject(error);
    });

    req.write(testData.data);
    req.end();
    
    console.log('Request sent, waiting for response...');
  });
}

// Health check
async function healthCheck() {
  return new Promise((resolve, reject) => {
    console.log('\n----- Testing API health check -----');
    
    const options = {
      hostname: hostname,
      port: port,
      path: '/',
      method: 'GET'
    };
    
    const httpModule = isHttps ? https : http;
    const req = httpModule.request(options, res => {
      console.log(`Status Code: ${res.statusCode}`);
      
      let responseData = '';
      
      res.on('data', chunk => {
        responseData += chunk;
      });
      
      res.on('end', () => {
        try {
          if (responseData) {
            const parsedData = JSON.parse(responseData);
            console.log('API Response:', JSON.stringify(parsedData, null, 2));
            resolve({success: true, data: parsedData});
          } else {
            console.log('Empty response, but status code is OK');
            resolve({success: true, data: {status: 'ok'}});
          }
        } catch (error) {
          console.error('Error parsing response:', error);
          console.log('Raw response:', responseData);
          resolve({success: false, error: error, raw: responseData});
        }
      });
    });

    req.on('error', error => {
      console.error('Error making request:', error);
      reject(error);
    });

    req.end();
    
    console.log('Request sent, waiting for response...');
  });
}

// Run the tests
async function runTests() {
  try {
    // First do a health check
    await healthCheck();
    
    // Test each endpoint with a 2-second delay between tests
    await makeRequest('PHQ-9', testData.phq);
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    await makeRequest('Patient Chat', testData.patientChat);
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    await makeRequest('NIHSS', testData.nihss);
    
    console.log('\n✅ All tests completed!');
  } catch (error) {
    console.error('\n❌ Test execution failed:', error);
  }
}

// Start the tests
console.log('======= InsultMedAI API Test =======');
runTests();

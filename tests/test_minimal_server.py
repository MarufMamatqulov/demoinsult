"""
Test script for the minimal auth server.
"""

import requests
import json
from datetime import datetime

# Constants
API_URL = "http://localhost:8001"
TEST_USER = {
    "email": f"test_{int(datetime.now().timestamp())}@example.com",
    "username": f"testuser_{int(datetime.now().timestamp())}",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}

def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_registration():
    """Test user registration endpoint."""
    print("Testing registration...")
    print(f"Request body: {json.dumps(TEST_USER, indent=2)}")
    try:
        response = requests.post(f"{API_URL}/register", json=TEST_USER, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Running tests for minimal auth server...")
    
    if not test_health():
        print("Health check failed. Is the server running?")
        exit(1)
        
    if not test_registration():
        print("Registration test failed.")
        exit(1)
        
    print("All tests passed!")

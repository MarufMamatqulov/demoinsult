"""
Simple script to test the registration endpoint directly.
"""

import requests
import json
from datetime import datetime

# Constants
API_URL = "http://localhost:8000"
TEST_USER = {
    "email": f"test_{int(datetime.now().timestamp())}@example.com",
    "username": f"testuser_{int(datetime.now().timestamp())}",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}

def test_registration():
    """Test user registration endpoint."""
    print(f"Sending request to: {API_URL}/auth/register")
    print(f"Request body: {json.dumps(TEST_USER, indent=2)}")
    try:
        response = requests.post(f"{API_URL}/auth/register", json=TEST_USER, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 201 or response.status_code == 200
    except requests.exceptions.Timeout:
        print("Request timed out. The server may not be responding.")
        return False
    except requests.exceptions.ConnectionError:
        print("Connection error. The server may not be running.")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_registration()

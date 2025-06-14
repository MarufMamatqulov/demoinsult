"""
Test script for the standalone auth server.
"""

import requests
import json
from datetime import datetime
import sys
import time

# Constants
API_URL = "http://localhost:8002"
TEST_USER = {
    "email": f"test_{int(datetime.now().timestamp())}@example.com",
    "username": f"testuser_{int(datetime.now().timestamp())}",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}

def print_separator(title):
    """Print a separator with a title."""
    print(f"\n{'=' * 40}")
    print(f" {title} ")
    print(f"{'=' * 40}")

def test_health():
    """Test health endpoint."""
    print_separator("TESTING HEALTH ENDPOINT")
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
    print_separator("TESTING REGISTRATION")
    print(f"Request body: {json.dumps(TEST_USER, indent=2)}")
    try:
        response = requests.post(f"{API_URL}/register", json=TEST_USER, timeout=30)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_login():
    """Test user login endpoint."""
    print_separator("TESTING LOGIN")
    login_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    print(f"Login data: {json.dumps(login_data, indent=2)}")
    try:
        response = requests.post(
            f"{API_URL}/token", 
            data=login_data,
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return response.json().get("access_token")
        else:
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def test_get_me(token):
    """Test get current user endpoint."""
    print_separator("TESTING GET CURRENT USER")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/users/me", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json() if response.status_code == 200 else response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def run_tests():
    """Run all tests."""
    print_separator("STARTING AUTH TESTS")
    
    # Wait for server to start
    print("Waiting for server to start...")
    retries = 5
    while retries > 0:
        if test_health():
            break
        retries -= 1
        time.sleep(2)
    
    if retries == 0:
        print("Server not responding. Exiting tests.")
        sys.exit(1)
    
    # Test registration
    if not test_registration():
        print("Registration test failed.")
        sys.exit(1)
    
    # Test login
    token = test_login()
    if not token:
        print("Login test failed.")
        sys.exit(1)
    
    # Test get me
    if not test_get_me(token):
        print("Get current user test failed.")
        sys.exit(1)
    
    print_separator("ALL TESTS PASSED")

if __name__ == "__main__":
    run_tests()

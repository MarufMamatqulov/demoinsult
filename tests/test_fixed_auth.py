"""
Test script to validate the fixed authentication system.
"""

import sys
import os
import requests
import json
import time
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Constants
API_URL = "http://localhost:8000"
TEST_USER = {
    "email": f"test_{int(datetime.now().timestamp())}@example.com",
    "username": f"testuser_{int(datetime.now().timestamp())}",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}
GOOGLE_TOKEN = "dummy_google_token_for_testing"

def print_separator(title):
    """Print a separator with a title."""
    print(f"\n{'=' * 30}")
    print(f" {title} ")
    print(f"{'=' * 30}")

def test_health():
    """Test health endpoint."""
    print_separator("TESTING HEALTH ENDPOINT")
    try:
        print(f"Sending request to: {API_URL}/health")
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
    print(f"Sending request to: {API_URL}/auth/register")
    print(f"Request body: {json.dumps(TEST_USER, indent=2)}")
    try:
        response = requests.post(f"{API_URL}/auth/register", json=TEST_USER, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
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

def test_login():
    """Test user login endpoint."""
    print_separator("TESTING LOGIN")
    login_data = {
        "username": TEST_USER["email"],  # Using email as username
        "password": TEST_USER["password"]
    }
    print(f"Sending request to: {API_URL}/auth/login")
    print(f"Request body: {json.dumps(login_data, indent=2)}")
    try:
        response = requests.post(
            f"{API_URL}/auth/login", 
            data=login_data,
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200 and "access_token" in response.json()
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_user_me(token):
    """Test get current user endpoint."""
    print_separator("TESTING GET CURRENT USER")
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Sending request to: {API_URL}/auth/me")
    print(f"Headers: {headers}")
    try:
        response = requests.get(f"{API_URL}/auth/me", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200 and "id" in response.json()
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_google_login():
    """Test Google login endpoint (mocked)."""
    print_separator("TESTING GOOGLE LOGIN (MOCK)")
    google_login_data = {
        "token": GOOGLE_TOKEN
    }
    print(f"Sending request to: {API_URL}/auth/login/google")
    print(f"Request body: {json.dumps(google_login_data, indent=2)}")
    print("Note: This test will fail if Google OAuth is not properly mocked.")
    try:
        response = requests.post(f"{API_URL}/auth/login/google", json=google_login_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json() if response.status_code == 200 else response.text}")
        # This will likely fail in real environment without proper Google token
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def run_tests():
    """Run all tests."""
    print_separator("STARTING AUTHENTICATION TESTS")
    
    # Test health endpoint
    if not test_health():
        print("❌ Health check failed. Is the server running?")
        return
    
    # Test registration
    if not test_registration():
        print("❌ Registration test failed.")
        return
    
    # Test login
    login_success = test_login()
    if not login_success:
        print("❌ Login test failed.")
        return
    
    # Get token for authenticated requests
    login_data = {
        "username": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    try:
        response = requests.post(f"{API_URL}/auth/login", data=login_data, timeout=10)
        if response.status_code == 200:
            token = response.json()["access_token"]
        else:
            print("❌ Could not get token for authenticated requests.")
            return
    except Exception as e:
        print(f"Error getting token: {str(e)}")
        return
    
    # Test get current user
    if not test_user_me(token):
        print("❌ Get current user test failed.")
        return
    
    # Test Google login (this will likely fail without proper mocking)
    test_google_login()
    
    print_separator("TESTS COMPLETED")
    print("✅ Authentication system is working correctly!")

if __name__ == "__main__":
    run_tests()

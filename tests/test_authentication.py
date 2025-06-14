# Test Authentication System
# This script tests the authentication system endpoints

import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_URL = f"http://{os.getenv('API_HOST', 'localhost')}:{os.getenv('API_PORT', '8000')}"
print(f"Testing API at: {API_URL}")

# Test data
test_user = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
}

def test_registration():
    """Test user registration endpoint"""
    print("\n--- Testing Registration ---")
    print(f"Sending request to: {API_URL}/auth/register")
    print(f"Request body: {json.dumps(test_user, indent=2)}")
    try:
        response = requests.post(f"{API_URL}/auth/register", json=test_user, timeout=10)
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
    """Test login endpoint"""
    print("\n--- Testing Login ---")
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = requests.post(f"{API_URL}/auth/login", data=login_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"Token type: {token_data.get('token_type')}")
        print(f"Access token received: {token_data.get('access_token', '')[:10]}...")
        return token_data.get("access_token")
    else:
        print(f"Response: {response.json()}")
        return None

def test_protected_endpoint(token):
    """Test a protected endpoint that requires authentication"""
    print("\n--- Testing Protected Endpoint ---")
    if not token:
        print("No token available. Skipping test.")
        return False
        
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/auth/me", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_request_password_reset():
    """Test password reset request endpoint"""
    print("\n--- Testing Password Reset Request ---")
    reset_data = {"email": test_user["email"]}
    response = requests.post(f"{API_URL}/auth/request-password-reset", json=reset_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def main():
    """Main test function"""
    print("=== Authentication System Test ===")
    
    # Test registration
    registration_success = test_registration()
    
    # Test login
    token = test_login()
    
    # Test protected endpoint
    if token:
        protected_endpoint_success = test_protected_endpoint(token)
    else:
        protected_endpoint_success = False
    
    # Test password reset request
    password_reset_success = test_request_password_reset()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Registration: {'✅ Success' if registration_success else '❌ Failed'}")
    print(f"Login: {'✅ Success' if token else '❌ Failed'}")
    print(f"Protected Endpoint: {'✅ Success' if protected_endpoint_success else '❌ Failed'}")
    print(f"Password Reset Request: {'✅ Success' if password_reset_success else '❌ Failed'}")
    
    print("\nNOTE: For complete testing, you need to check your email for verification and password reset links.")

if __name__ == "__main__":
    main()

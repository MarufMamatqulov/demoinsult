"""
Test script for the main application authentication endpoints.
"""

import sys
import os
import requests
import json
import random
import string

def generate_random_string(length=8):
    """Generate a random string."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Create test user data
random_suffix = generate_random_string()
test_user = {
    "email": f"test_main_{random_suffix}@example.com",
    "username": f"testuser_main_{random_suffix}",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}

# Define base URL for the main application
BASE_URL = "http://localhost:8000"

def test_registration():
    """Test user registration endpoint."""
    url = f"{BASE_URL}/auth/register"
    
    print("\n=== Testing User Registration ===")
    print(f"POST {url}")
    print(f"Data: {json.dumps(test_user, indent=2)}")
    
    try:
        response = requests.post(url, json=test_user, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("✅ Registration successful!")
            return True
        else:
            print(f"Response: {response.text}")
            print("❌ Registration failed.")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        print("❌ Registration failed.")
        return False

def test_login():
    """Test user login endpoint."""
    url = f"{BASE_URL}/auth/login"
    
    print("\n=== Testing User Login ===")
    print(f"POST {url}")
    
    login_data = {
        "username": test_user["email"],  # Try logging in with email
        "password": test_user["password"]
    }
    
    print(f"Form data: {json.dumps(login_data, indent=2)}")
    
    try:
        response = requests.post(url, data=login_data, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
            print("✅ Login successful!")
            return response_data.get("access_token")
        else:
            print(f"Response: {response.text}")
            print("❌ Login failed.")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        print("❌ Login failed.")
        return None

def test_current_user(token):
    """Test getting current user information with the token."""
    if not token:
        print("\n⚠️ Skipping current user test due to missing token.")
        return
    
    url = f"{BASE_URL}/auth/me"
    
    print("\n=== Testing Get Current User ===")
    print(f"GET {url}")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            print("✅ Get current user successful!")
        else:
            print(f"Response: {response.text}")
            print("❌ Get current user failed.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("❌ Get current user failed.")

if __name__ == "__main__":
    print("🚀 Starting main application authentication test...")
    
    # Run registration test
    registration_success = test_registration()
    
    # Run login test
    token = test_login()
    
    # Test getting current user info
    if token:
        test_current_user(token)
    
    if registration_success and token:
        print("\n✅ All authentication tests passed successfully!")
    else:
        print("\n❌ Some authentication tests failed.")

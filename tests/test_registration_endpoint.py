"""
Simple test script for the registration endpoint.
"""

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
    "email": f"test_{random_suffix}@example.com",
    "username": f"testuser_{random_suffix}",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}

# API endpoint
url = "http://localhost:8002/register"  # Changed to use the standalone server port

print(f"Testing registration with user: {json.dumps(test_user, indent=2)}")

# Send registration request
try:
    response = requests.post(url, json=test_user, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201 or response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("Registration successful!")
    else:
        print(f"Response: {response.text}")
        print("Registration failed.")
except Exception as e:
    print(f"Error: {str(e)}")
    print("Registration failed.")

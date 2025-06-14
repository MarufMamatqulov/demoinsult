"""
Simple test script for the login endpoint.
"""

import requests
import json

# Use the same test user that was created in test_registration_endpoint.py
test_user = {
    "username": "testuser_dp283uuv",  # Use the same username as registered previously
    "password": "TestPassword123!"
}

# API endpoint
url = "http://localhost:8002/token"  # Login endpoint of the standalone server

print(f"Testing login with user: {json.dumps(test_user, indent=2)}")

# Send login request as form data (OAuth2 password flow)
try:
    response = requests.post(
        url, 
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        },
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
        print("Login successful!")
        
        # Test token validity by making a request to a protected endpoint
        token = response_data["access_token"]
        me_url = "http://localhost:8002/users/me"
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        me_response = requests.get(me_url, headers=headers, timeout=30)
        print(f"\nTesting token with /users/me endpoint:")
        print(f"Status Code: {me_response.status_code}")
        
        if me_response.status_code == 200:
            print(f"User data: {json.dumps(me_response.json(), indent=2)}")
            print("Token verification successful!")
        else:
            print(f"Response: {me_response.text}")
            print("Token verification failed.")
    else:
        print(f"Response: {response.text}")
        print("Login failed.")
except Exception as e:
    print(f"Error: {str(e)}")
    print("Login failed.")

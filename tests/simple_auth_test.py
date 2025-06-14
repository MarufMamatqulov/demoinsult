import requests
import json
import time
import os

API_URL = "http://localhost:8001"  # Updated port
print(f"Testing API at: {API_URL}")

# Test user data
test_user = {
    "email": "test2@example.com",  # Using a different email to avoid conflicts
    "username": "testuser2",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
}

# Login data
login_data = {
    "username": test_user["email"],
    "password": test_user["password"]
}

def test_server_health():
    """Test if server is responsive"""
    print("\n--- Testing Server Health ---")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

def test_register_user():
    """Test user registration"""
    print("\n--- Testing User Registration ---")
    try:
        response = requests.post(
            f"{API_URL}/auth/register", 
            json=test_user,
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code in [200, 201]
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

def test_login():
    """Test login"""
    print("\n--- Testing Login ---")
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data=login_data,  # Note: login uses form data, not JSON
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

def test_auth_endpoint():
    """Test an authenticated endpoint"""
    print("\n--- Testing Protected Endpoint ---")
    try:
        # First login to get token
        login_response = requests.post(
            f"{API_URL}/auth/login",
            data=login_data,
            timeout=10
        )
        if login_response.status_code != 200:
            print("Login failed, cannot test protected endpoint")
            return False
            
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Call protected endpoint
        response = requests.get(
            f"{API_URL}/auth/me",
            headers=headers,
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    # Wait a bit for server to start
    print("Waiting for server to start...")
    time.sleep(5)
    
    # First check if server is responsive
    if test_server_health():
        print("\nServer is running!")
        
        # Test registration
        registration_result = test_register_user()
        print(f"\nRegistration test {'passed' if registration_result else 'failed'}!")
        
        # Test login
        login_result = test_login()
        print(f"\nLogin test {'passed' if login_result else 'failed'}!")
        
        # Test protected endpoint
        if login_result:
            auth_result = test_auth_endpoint()
            print(f"\nProtected endpoint test {'passed' if auth_result else 'failed'}!")
    else:
        print("\nServer is not responsive. Make sure it's running.")

import requests
import json
import time

API_URL = "http://localhost:8002"
print(f"Testing simplified auth server at: {API_URL}")

# Test user data
test_user = {
    "email": "simple_test@example.com",
    "username": "simple_testuser",
    "password": "simple_password123",
    "first_name": "Test",
    "last_name": "User"
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
            f"{API_URL}/register", 
            params=test_user,
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
        login_data = {
            "username": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(
            f"{API_URL}/login",
            data=login_data,
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

if __name__ == "__main__":
    # Wait a bit for server to start
    print("Waiting for server to start...")
    time.sleep(5)
    
    # Check if server is responsive
    if test_server_health():
        print("\nServer is running!")
        
        # Test registration
        registration_result = test_register_user()
        print(f"\nRegistration test {'passed' if registration_result else 'failed'}!")
        
        # Test login
        login_result = test_login()
        print(f"\nLogin test {'passed' if login_result else 'failed'}!")
    else:
        print("\nServer is not responsive. Make sure it's running.")

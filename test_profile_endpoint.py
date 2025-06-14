"""
Test script to verify the profile endpoint works without rate limiting.
"""
import requests
import time

BASE_URL = "http://localhost:8000"

def test_profile_endpoint():
    print("Testing profile endpoint without authentication (should fail with 401):")
    response = requests.get(f"{BASE_URL}/auth/me/profile")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:100]}...")
    print()

    print("Making 10 consecutive requests to test rate limiting removal:")
    for i in range(10):
        response = requests.get(f"{BASE_URL}/auth/me/profile")
        print(f"Request {i+1}: Status {response.status_code}")
        # No delay between requests to test that rate limiting is gone
    
    print("\nVerification complete!")

if __name__ == "__main__":
    test_profile_endpoint()

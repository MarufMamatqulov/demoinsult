import requests
import time
import sys

def test_rate_limiting():
    """Test the rate limiting implementation for profile requests."""
    print("Testing rate limiting for profile requests...")
    
    # Make multiple requests in quick succession
    url = "http://localhost:8000/profile"
    headers = {"host": "test-client"}
    
    # First request should succeed
    print("Making first request...")
    response1 = requests.get(url, headers=headers)
    print(f"First request status: {response1.status_code}")
    
    if response1.status_code != 200:
        print(f"First request failed: {response1.text}")
        return False
    
    # Second immediate request should be rate limited
    print("Making immediate second request (should be rate limited)...")
    response2 = requests.get(url, headers=headers)
    print(f"Second request status: {response2.status_code}")
    
    if response2.status_code != 429:
        print("Rate limiting not working - second request should have been blocked")
        return False
    
    # Check if the response contains the expected error message
    if "Too many profile requests" not in response2.text:
        print("Rate limiting error message is not as expected")
        return False
    
    # Wait for 6 seconds (more than the 5-second window)
    print("Waiting for 6 seconds...")
    time.sleep(6)
    
    # Third request after waiting should succeed
    print("Making third request after waiting...")
    response3 = requests.get(url, headers=headers)
    print(f"Third request status: {response3.status_code}")
    
    if response3.status_code != 200:
        print(f"Third request failed: {response3.text}")
        return False
    
    print("Rate limiting is working correctly!")
    return True

if __name__ == "__main__":
    success = test_rate_limiting()
    sys.exit(0 if success else 1)

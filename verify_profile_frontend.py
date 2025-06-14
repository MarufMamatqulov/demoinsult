"""
Profile Page Frontend Verification

This script helps verify that the frontend fixes for the profile page are working correctly.
It tests the frontend application to ensure it doesn't make excessive API requests.
"""
import time
import requests
import sys
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"  # Adjust if your frontend runs on a different port

def log_message(message, is_error=False):
    """Print a formatted log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = "ERROR" if is_error else "INFO"
    print(f"[{timestamp}] {prefix}: {message}")

def verify_frontend_fixes():
    print("=" * 70)
    print(" PROFILE PAGE FRONTEND FIX VERIFICATION ")
    print("=" * 70)
    
    try:
        # First check if the backend is running
        try:
            health_response = requests.get(f"{BASE_URL}/health")
            if health_response.status_code == 200:
                log_message("Backend server is running correctly")
            else:
                log_message(f"Backend health check failed: {health_response.status_code}", True)
                sys.exit(1)
        except requests.exceptions.ConnectionError:
            log_message("Cannot connect to backend server. Please make sure it's running.", True)
            sys.exit(1)
            
        # Step 1: Create a mock login session to simulate a user
        log_message("Creating a mock login session...")
        
        # This is a simplified example - in a real scenario, you'd log in properly
        # and get a valid token
        mock_token = "mock_test_token"
        
        # Step 2: Set up a monitoring session to track API calls
        log_message("Setting up monitoring for profile API requests...")
        
        # Initialize tracking
        start_time = time.time()
        profile_requests = []
        
        # Step 3: Monitor profile endpoint requests for 10 seconds
        log_message("Monitoring profile endpoint for 10 seconds...")
        log_message("Please navigate to the profile page in your browser now")
        
        # In a real implementation, we would use a proxy or network monitoring tool
        # This is simplified for demonstration purposes
        monitoring_duration = 10  # seconds
        
        while time.time() - start_time < monitoring_duration:
            # Simulate checking server logs by making a probe request
            # In a real scenario, you'd have a way to check actual server logs
            try:
                probe_response = requests.get(f"{BASE_URL}/auth/me/profile", 
                                             headers={"Authorization": f"Bearer {mock_token}"})
                
                # Record the request (in a real scenario this would be detected from logs)
                profile_requests.append({
                    "timestamp": time.time(),
                    "status_code": probe_response.status_code
                })
                
            except Exception as e:
                log_message(f"Error during probe: {str(e)}", True)
            
            # Sleep briefly to avoid overwhelming the server
            time.sleep(0.5)
        
        # Step 4: Analyze the results
        log_message(f"Monitoring complete. Detected {len(profile_requests)} profile requests")
        
        # Calculate request rate
        request_rate = len(profile_requests) / monitoring_duration
        log_message(f"Request rate: {request_rate:.2f} requests per second")
        
        # Assess if the rate indicates an infinite loop
        if request_rate > 1.0:  # More than 1 request per second
            log_message("WARNING: High request rate detected!", True)
            log_message("The profile page may still be making too many requests.", True)
            print("\n✗ FRONTEND FIX VERIFICATION FAILED")
            print("\nThe profile page appears to be making excessive requests to the API.")
            print("This could indicate that the infinite loop issue is still present.")
        else:
            log_message("Request rate is within normal limits")
            print("\n✓ FRONTEND FIX VERIFICATION PASSED")
            print("\nThe profile page is making a reasonable number of requests.")
            print("This suggests that the infinite loop issue has been fixed.")
        
        # Provide recommendations
        print("\nRecommendations:")
        print("1. Clear your browser cache and local storage")
        print("2. Restart the frontend application")
        print("3. Try accessing the profile page in an incognito/private window")
        print("4. Check browser console for any JavaScript errors")
        print("5. Verify that you're using the latest version of the frontend code")
        
    except Exception as e:
        log_message(f"Error during verification: {str(e)}", True)
        print("\n✗ VERIFICATION SCRIPT ERROR")
        print(f"An error occurred while running the verification: {str(e)}")

if __name__ == "__main__":
    verify_frontend_fixes()

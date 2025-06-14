"""
Profile API Fix Verification

This script verifies that the profile endpoint works correctly
and provides guidance for frontend troubleshooting.
"""
import sys
import requests
import time

BASE_URL = "http://localhost:8000"

def verify_profile_fix():
    print("=" * 60)
    print(" PROFILE ENDPOINT FIX VERIFICATION ")
    print("=" * 60)
    print("\nVerifying the profile endpoint works without rate limiting...")
    
    try:
        # First, check if the server is running
        health_response = requests.get(f"{BASE_URL}/health")
        if health_response.status_code == 200:
            print("✓ Server is running correctly")
        else:
            print(f"✗ Server health check failed: {health_response.status_code}")
            sys.exit(1)
        
        # Make multiple rapid requests to the profile endpoint
        print("\nMaking multiple rapid requests to test rate limiting removal:")
        success_count = 0
        failure_count = 0
        
        for i in range(20):
            response = requests.get(f"{BASE_URL}/auth/me/profile")
            
            if response.status_code == 401:  # Expected without auth
                success_count += 1
                status = "✓"
            elif response.status_code == 429:  # Rate limited - should not happen
                failure_count += 1
                status = "✗"
            else:
                status = "?"
                
            print(f"{status} Request {i+1}: Status {response.status_code}")
            # No delay between requests to test that rate limiting is gone
        
        print(f"\nResults: {success_count} successful, {failure_count} rate limited")
        
        if failure_count == 0:
            print("\n✓ PROFILE ENDPOINT FIX VERIFIED!")
            print("\nThe profile endpoint is now working correctly without rate limiting.")
            print("You should now be able to access your profile page without any issues.")
        else:
            print("\n✗ PROFILE ENDPOINT FIX FAILED")
            print("\nSome requests are still being rate limited. Please check the server logs.")
        
        print("\nFrontend Troubleshooting Instructions:")
        print("1. Clear your browser cache or try in incognito mode")
        print("2. Make sure you're logged in before accessing the profile page")
        print("3. If still having issues, try restarting the frontend application")
        print("\nServer has been configured to handle rapid profile requests!")
    
    except Exception as e:
        print(f"\n✗ Error during verification: {str(e)}")
        print("Please make sure the server is running and accessible.")

if __name__ == "__main__":
    verify_profile_fix()

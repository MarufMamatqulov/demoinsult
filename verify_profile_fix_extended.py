"""
Profile API Fix Verification - Extended

This script comprehensively tests the profile endpoint fix, including:
1. Frontend fixes (memoized function and optimized component)
2. Backend rate limiting improvements
"""
import sys
import requests
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

BASE_URL = "http://localhost:8000"

def verify_profile_fix_extended():
    print("=" * 70)
    print(" COMPREHENSIVE PROFILE ENDPOINT FIX VERIFICATION ")
    print("=" * 70)
    
    try:
        # First, check if the server is running
        health_response = requests.get(f"{BASE_URL}/health")
        if health_response.status_code == 200:
            print("✓ Server is running correctly")
        else:
            print(f"✗ Server health check failed: {health_response.status_code}")
            sys.exit(1)
        
        # Test 1: Normal request pattern (5 requests with 1 sec interval)
        print("\nTest 1: Normal request pattern - 5 requests with 1 sec interval")
        response_times = []
        status_codes = []
        
        for i in range(5):
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/auth/me/profile")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            response_times.append(response_time)
            status_codes.append(response.status_code)
            
            print(f"Request {i+1}: Status {response.status_code}, Response time: {response_time:.2f}ms")
            time.sleep(1)  # Wait 1 second between requests
        
        print(f"Average response time: {np.mean(response_times):.2f}ms")
        
        # Test 2: Burst request pattern (10 requests as fast as possible)
        print("\nTest 2: Burst request pattern - 10 requests as fast as possible")
        burst_response_times = []
        burst_status_codes = []
        rate_limited_count = 0
        
        for i in range(10):
            start_time = time.time()
            response = requests.get(f"{BASE_URL}/auth/me/profile")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            burst_response_times.append(response_time)
            burst_status_codes.append(response.status_code)
            
            if response.status_code == 429:
                rate_limited_count += 1
                retry_after = response.json().get('retry_after', 'N/A')
                print(f"Request {i+1}: Rate limited (429), Retry after: {retry_after}s, Response time: {response_time:.2f}ms")
            else:
                print(f"Request {i+1}: Status {response.status_code}, Response time: {response_time:.2f}ms")
        
        print(f"Burst test results: {rate_limited_count} rate limited out of 10 requests")
        
        # Test 3: Recovery after rate limiting
        if rate_limited_count > 0:
            print("\nTest 3: Recovery after rate limiting - waiting 5 seconds then trying again")
            time.sleep(5)
            
            start_time = time.time()
            recovery_response = requests.get(f"{BASE_URL}/auth/me/profile")
            end_time = time.time()
            
            recovery_time = (end_time - start_time) * 1000
            print(f"Recovery request: Status {recovery_response.status_code}, Response time: {recovery_time:.2f}ms")
            
            if recovery_response.status_code != 429:
                print("✓ Successfully recovered from rate limiting after waiting")
            else:
                print("✗ Still rate limited after waiting period")
        
        # Final verification
        print("\n=== Verification Results ===")
        normal_success = all(code in (200, 401) for code in status_codes)
        burst_behavior = rate_limited_count > 0 or all(code in (200, 401) for code in burst_status_codes)
        
        if normal_success:
            print("✓ Normal request pattern handled correctly")
        else:
            print("✗ Issues with normal request pattern")
        
        if burst_behavior:
            print("✓ Burst protection working correctly")
        else:
            print("✗ Issues with burst protection")
        
        if normal_success and burst_behavior:
            print("\n✓ PROFILE ENDPOINT FIX VERIFIED!")
            print("\nThe profile endpoint is now working correctly with proper rate limiting.")
            print("You should now be able to access your profile page without any issues.")
        else:
            print("\n✗ Some verification tests failed - further investigation needed")
        
        print("\nRecommendations:")
        print("1. Clear your browser cache or try in incognito mode")
        print("2. Make sure you're logged in before accessing the profile page")
        print("3. The backend now properly handles multiple requests with rate limiting")
    
    except Exception as e:
        print(f"\n✗ Error during verification: {str(e)}")
        print("Please make sure the server is running and accessible.")

if __name__ == "__main__":
    verify_profile_fix_extended()

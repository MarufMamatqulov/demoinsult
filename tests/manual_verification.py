"""
Manual test script for the API endpoint fixes.
"""

import requests
import json
import logging
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# API base URL
API_URL = "http://localhost:8000"

def check_server_status():
    """Check if the API server is running."""
    try:
        response = requests.get(f"{API_URL}/")
        logging.info(f"Server responded with status code: {response.status_code}")
        return True
    except Exception as e:
        logging.error(f"Server connection error: {str(e)}")
        return False

def manual_assessment_endpoint_test():
    """Manually test the assessment history endpoint."""
    print("\n=== MANUAL ASSESSMENT ENDPOINT TEST ===")
    print("This will make a request to the assessment history endpoint")
    print("It should return a 401 Unauthorized response, NOT a 500 error")
    print("Press Enter to continue...")
    input()
    
    try:
        response = requests.get(f"{API_URL}/assessments/history", timeout=5)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("✅ SUCCESS: Endpoint requires authentication (401) - This is expected")
            return True
        elif response.status_code == 500:
            print("❌ FAILED: Endpoint still returning 500 error")
            return False
        else:
            print(f"⚠️ WARNING: Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def manual_openai_integration_test():
    """Manually test the OpenAI integration."""
    print("\n=== MANUAL OPENAI INTEGRATION TEST ===")
    print("This will make a request to the OpenAI chat completion endpoint")
    print("It should return a 401 Unauthorized response, NOT a 500 error")
    print("Press Enter to continue...")
    input()
    
    try:
        response = requests.post(
            f"{API_URL}/openai/chat/completion", 
            json={"messages": [{"role": "user", "content": "Test message"}]},
            timeout=5
        )
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("✅ SUCCESS: Endpoint requires authentication (401) - This is expected")
            return True
        elif response.status_code == 500:
            print("❌ FAILED: Endpoint still returning 500 error")
            return False
        else:
            print(f"⚠️ WARNING: Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def patient_chat_test():
    """Test the patient chat endpoint specifically mentioned in the logs."""
    print("\n=== PATIENT CHAT ENDPOINT TEST ===")
    print("This will make a request to the patient chat endpoint")
    print("It should return a 401 Unauthorized response, NOT a 500 error")
    print("Press Enter to continue...")
    input()
    
    try:
        response = requests.post(
            f"{API_URL}/chat/patient-chat", 
            json={"message": "Test message"},
            timeout=5
        )
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("✅ SUCCESS: Endpoint requires authentication (401) - This is expected")
            return True
        elif response.status_code == 500:
            print("❌ FAILED: Endpoint still returning 500 error")
            return False
        else:
            print(f"⚠️ WARNING: Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def run_manual_tests():
    """Run manual tests with user interaction."""
    print("=== API Fixes Manual Verification ===")
    print("This script will help verify that the API fixes are working correctly")
    print("It will test:")
    print("1. The assessment history endpoint (should no longer return 500 errors)")
    print("2. The OpenAI integration (should no longer have API version issues)")
    print("3. The patient chat endpoint (specifically mentioned in the logs)")
    print("\nNote: You should expect 401 Unauthorized responses, not 500 errors")
    print("\nChecking if the API server is running...")
    
    if not check_server_status():
        print("Cannot connect to the API server. Please make sure it's running.")
        print("You can start it with: python backend/main.py")
        return False
    
    # Run the manual tests
    assessment_result = manual_assessment_endpoint_test()
    openai_result = manual_openai_integration_test()
    patient_chat_result = patient_chat_test()
    
    # Print summary
    print("\n=== TEST SUMMARY ===")
    print(f"Assessment History Endpoint: {'PASS' if assessment_result else 'FAIL'}")
    print(f"OpenAI Integration: {'PASS' if openai_result else 'FAIL'}")
    print(f"Patient Chat Endpoint: {'PASS' if patient_chat_result else 'FAIL'}")
    
    all_passed = all([assessment_result, openai_result, patient_chat_result])
    
    if all_passed:
        print("\n✅ SUCCESS: All tests passed! The API fixes are working correctly.")
    else:
        print("\n❌ FAILED: Some tests failed. Check the output above for details.")
    
    return all_passed

if __name__ == "__main__":
    run_manual_tests()

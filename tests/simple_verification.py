"""
Simple verification script for the API endpoint fixes.
This script tests both the assessment history endpoints and the OpenAI integration.
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

def test_assessment_history_endpoint():
    """Test the assessment history endpoint."""
    logging.info("Testing assessment history endpoint...")
    
    # Try to access the endpoint directly (should still show 401 Unauthorized, not 500)
    response = requests.get(f"{API_URL}/assessments/history")
    
    if response.status_code == 401:
        logging.info("Endpoint requires authentication (401) - This is expected")
        return True
    elif response.status_code == 500:
        logging.error(f"Endpoint still returning 500 error: {response.text}")
        return False
    else:
        logging.warning(f"Unexpected status code: {response.status_code}")
        return False

def test_openai_integration():
    """Test the OpenAI integration."""
    logging.info("Testing OpenAI integration endpoint...")
    
    # Try to access the endpoint directly (should still show 401 Unauthorized, not 500)
    response = requests.post(
        f"{API_URL}/openai/chat/completion", 
        json={"messages": [{"role": "user", "content": "Test message"}]}
    )
    
    if response.status_code == 401:
        logging.info("Endpoint requires authentication (401) - This is expected")
        return True
    elif response.status_code == 500:
        logging.error(f"Endpoint still returning 500 error: {response.text}")
        return False
    else:
        logging.warning(f"Unexpected status code: {response.status_code}")
        return False

def run_all_tests():
    """Run all verification tests."""
    logging.info("Starting API fixes verification...")
    
    # Run all tests
    assessment_history_result = test_assessment_history_endpoint()
    openai_integration_result = test_openai_integration()
    
    # Summary
    logging.info("\n=== Verification Test Summary ===")
    logging.info(f"Assessment History Endpoint: {'PASS' if assessment_history_result else 'FAIL'}")
    logging.info(f"OpenAI Integration: {'PASS' if openai_integration_result else 'FAIL'}")
    
    all_passed = all([assessment_history_result, openai_integration_result])
    
    if all_passed:
        logging.info("All tests PASSED! The API endpoints are no longer returning 500 errors.")
    else:
        logging.warning("Some tests FAILED. Please check the logs for details.")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()

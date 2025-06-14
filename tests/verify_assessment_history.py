"""
Final assessment history verification script.
This script specifically tests the assessment history endpoints
which were having issues with "'list' object has no attribute 'get'".
"""

import requests
import json
import logging
import sys
import os
import time
from datetime import datetime

# Add project root to Python path to ensure modules can be found
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('assessment_history_verification.log', encoding='utf-8')
    ]
)

# Log environment information for debugging
logging.info(f"Python version: {sys.version}")
logging.info(f"Python path: {sys.path}")
logging.info(f"Working directory: {os.getcwd()}")
logging.info(f"Script location: {os.path.abspath(__file__)}")

# API base URL
API_URL = "http://localhost:8000"

# Test user credentials - update with valid credentials for your test environment
TEST_USER = {
    "username": "test@example.com",  # Try both username and email
    "email": "test@example.com",
    "password": "Password123!"
}

def get_auth_token():
    """Get authentication token for the test user."""
    # Try different authentication methods
    auth_methods = [
        # Method 1: Using form data with email as username
        {"data": {"username": TEST_USER["email"], "password": TEST_USER["password"]}},
        # Method 2: Using form data with username
        {"data": {"username": TEST_USER["username"], "password": TEST_USER["password"]}},
        # Method 3: Using JSON with email
        {"json": {"email": TEST_USER["email"], "password": TEST_USER["password"]}},
        # Method 4: Using JSON with username
        {"json": {"username": TEST_USER["username"], "password": TEST_USER["password"]}},
        # Method 5: Using JSON with both email and username
        {"json": {"email": TEST_USER["email"], "username": TEST_USER["username"], "password": TEST_USER["password"]}},
    ]
    
    # Additional auth endpoints to try
    auth_endpoints = [
        "/auth/login",
        "/auth/token",
        "/auth/signin"
    ]
    
    for endpoint in auth_endpoints:
        for i, auth_method in enumerate(auth_methods, 1):
            try:
                logging.info(f"Trying authentication endpoint {endpoint} with method {i}...")
                response = requests.post(
                    f"{API_URL}{endpoint}",
                    **auth_method
                )                        
                if response.status_code == 200:
                    try:
                        data = response.json()
                        token = data.get("access_token")
                        if token:
                            logging.info("[SUCCESS] Successfully obtained authentication token")
                            return token
                        else:
                            logging.warning(f"[WARNING] Response didn't contain access_token. Got: {data.keys()}")
                            # Check for token under a different key
                            if "token" in data:
                                logging.info("[SUCCESS] Found token under 'token' key")
                                return data["token"]
                    except ValueError:
                        logging.warning("[WARNING] Response wasn't valid JSON")
                else:
                    logging.warning(f"[WARNING] Authentication attempt failed: {response.status_code}")
            except Exception as e:
                logging.warning(f"[WARNING] Error with authentication attempt: {str(e)}")
    
    logging.error("[ERROR] All authentication attempts failed")
    return None

def test_get_assessment_history(token):
    """Test the GET /assessments/history endpoint."""
    if not token:
        logging.error("❌ Cannot test without authentication token")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        logging.info("Testing GET /assessments/history endpoint...")
        response = requests.get(
            f"{API_URL}/assessments/history",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"✅ Successfully retrieved {len(data)} assessments")
            
            if data:
                logging.info("Sample assessment data structure:")
                logging.info(json.dumps(data[0], indent=2, default=str))
            
            return True
        else:
            logging.error(f"❌ Failed to get assessment history: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"❌ Error testing GET /assessments/history: {str(e)}")
        return False

def test_get_assessment_history_with_limit(token):
    """Test the GET /assessments/history?limit=3 endpoint."""
    if not token:
        logging.error("❌ Cannot test without authentication token")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        logging.info("Testing GET /assessments/history?limit=3 endpoint...")
        response = requests.get(
            f"{API_URL}/assessments/history?limit=3",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"✅ Successfully retrieved {len(data)} assessments with limit")
            
            if len(data) <= 3:
                logging.info("✅ Limit parameter is working correctly")
            else:
                logging.warning(f"⚠️ Limit parameter may not be working: got {len(data)} items")
            
            return True
        else:
            logging.error(f"❌ Failed to get assessment history with limit: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"❌ Error testing GET /assessments/history with limit: {str(e)}")
        return False

def test_create_and_get_assessment(token):
    """Test creating a new assessment and retrieving it by ID."""
    if not token:
        logging.error("❌ Cannot test without authentication token")
        return False
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    try:
        # Create a test assessment
        logging.info("Creating a test assessment...")
        test_data = {
            "type": "test_assessment",
            "data": {
                "score": 92,
                "maxScore": 100,
                "notes": "Test assessment created during verification",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        create_response = requests.post(
            f"{API_URL}/assessments/",
            headers=headers,
            json=test_data
        )
        
        if create_response.status_code == 201:
            assessment = create_response.json()
            assessment_id = assessment.get("id")
            logging.info(f"✅ Successfully created assessment with ID {assessment_id}")
            
            # Get the assessment by ID
            logging.info(f"Retrieving assessment with ID {assessment_id}...")
            get_response = requests.get(
                f"{API_URL}/assessments/{assessment_id}",
                headers=headers
            )
            
            if get_response.status_code == 200:
                retrieved = get_response.json()
                logging.info(f"✅ Successfully retrieved assessment with ID {assessment_id}")
                
                # Verify the assessment data
                if retrieved.get("type") == test_data["type"] and retrieved.get("data", {}).get("score") == test_data["data"]["score"]:
                    logging.info("✅ Retrieved assessment data matches the created data")
                    
                    # Try to delete the assessment
                    delete_response = requests.delete(
                        f"{API_URL}/assessments/{assessment_id}",
                        headers=headers
                    )
                    
                    if delete_response.status_code == 204:
                        logging.info(f"✅ Successfully deleted assessment with ID {assessment_id}")
                    else:
                        logging.warning(f"⚠️ Failed to delete assessment: {delete_response.status_code} - {delete_response.text}")
                    
                    return True
                else:
                    logging.error("❌ Retrieved assessment data does not match the created data")
                    return False
            else:
                logging.error(f"❌ Failed to retrieve assessment: {get_response.status_code} - {get_response.text}")
                return False
        else:
            logging.error(f"❌ Failed to create assessment: {create_response.status_code} - {create_response.text}")
            return False
    except Exception as e:
        logging.error(f"❌ Error testing assessment creation and retrieval: {str(e)}")
        return False

def run_verification():
    """Run all verification tests for assessment history endpoints."""
    logging.info("=== Starting Assessment History Endpoint Verification ===")
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        logging.error("Failed to get authentication token. Cannot proceed with tests.")
        sys.exit(1)  # Exit with non-zero code to indicate failure
    
    # Run all tests
    history_test = test_get_assessment_history(token)
    limit_test = test_get_assessment_history_with_limit(token)
    crud_test = test_create_and_get_assessment(token)
    
    # Summarize results
    logging.info("\n=== Verification Summary ===")
    logging.info(f"GET /assessments/history: {'✅ PASS' if history_test else '❌ FAIL'}")
    logging.info(f"GET /assessments/history?limit=3: {'✅ PASS' if limit_test else '❌ FAIL'}")
    logging.info(f"Create, Get, Delete Assessment: {'✅ PASS' if crud_test else '❌ FAIL'}")
    
    all_passed = history_test and limit_test and crud_test
    
    if all_passed:
        logging.info("\n✅ SUCCESS: All assessment history endpoints are working correctly!")
        return True
    else:
        logging.error("\n❌ FAILURE: Some assessment history endpoints are not working correctly.")
        sys.exit(1)  # Exit with non-zero code to indicate failure

if __name__ == "__main__":
    run_verification()

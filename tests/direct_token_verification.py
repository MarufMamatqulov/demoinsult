"""
Direct token-based assessment history verification script.
This script uses a directly generated JWT token to test the assessment history endpoints.
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

def get_token_from_file():
    """Get the JWT token from the token file."""
    token_path = os.path.join(project_root, "test_token.txt")
    try:
        if os.path.exists(token_path):
            with open(token_path, "r") as f:
                token = f.read().strip()
                logging.info("Successfully loaded token from file")
                return token
        else:
            logging.error(f"Token file not found at {token_path}")
            logging.info("Please run generate_test_token.py first")
            return None
    except Exception as e:
        logging.error(f"Error loading token: {str(e)}")
        return None

def test_get_assessment_history(token):
    """Test the GET /assessments/history endpoint."""
    if not token:
        logging.error("[ERROR] Cannot test without authentication token")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        logging.info("Testing GET /assessments/history endpoint...")
        logging.info(f"Using token: {token[:10]}...")
        logging.info(f"Full headers: {headers}")
        
        response = requests.get(
            f"{API_URL}/assessments/history",
            headers=headers
        )
        
        logging.info(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"[SUCCESS] Successfully retrieved {len(data)} assessments")
            
            if data:
                logging.info("Sample assessment data structure:")
                logging.info(json.dumps(data[0], indent=2, default=str))
            else:
                logging.info("No assessment records found (empty array returned)")
            
            return True
        else:
            logging.error(f"[ERROR] Failed to get assessment history: {response.status_code}")
            logging.error(f"Response text: {response.text}")
            return False
    except Exception as e:
        logging.error(f"[ERROR] Error testing GET /assessments/history: {str(e)}")
        return False

def test_get_assessment_history_with_limit(token):
    """Test the GET /assessments/history?limit=3 endpoint."""
    if not token:
        logging.error("[ERROR] Cannot test without authentication token")
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
            logging.info(f"[SUCCESS] Successfully retrieved {len(data)} assessments with limit")
            
            if len(data) <= 3:
                logging.info("[SUCCESS] Limit parameter is working correctly")
            else:
                logging.warning(f"[WARNING] Limit parameter may not be working: got {len(data)} items")
            
            return True
        else:
            logging.error(f"[ERROR] Failed to get assessment history with limit: {response.status_code}")
            logging.error(f"Response text: {response.text}")
            return False
    except Exception as e:
        logging.error(f"[ERROR] Error testing GET /assessments/history with limit: {str(e)}")
        return False

def test_create_and_get_assessment(token):
    """Test creating a new assessment and retrieving it by ID."""
    if not token:
        logging.error("[ERROR] Cannot test without authentication token")
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
        
        logging.info(f"Create response status: {create_response.status_code}")
        
        if create_response.status_code in [200, 201]:
            assessment = create_response.json()
            logging.info(f"Create response data: {assessment}")
            
            assessment_id = assessment.get("id")
            if not assessment_id:
                logging.error("[ERROR] Response did not contain assessment ID")
                return False
                
            logging.info(f"[SUCCESS] Successfully created assessment with ID {assessment_id}")
            
            # Get the assessment by ID
            logging.info(f"Retrieving assessment with ID {assessment_id}...")
            get_response = requests.get(
                f"{API_URL}/assessments/{assessment_id}",
                headers=headers
            )
            
            if get_response.status_code == 200:
                retrieved = get_response.json()
                logging.info(f"[SUCCESS] Successfully retrieved assessment with ID {assessment_id}")
                
                # Verify the assessment data
                if retrieved.get("type") == test_data["type"] and retrieved.get("data", {}).get("score") == test_data["data"]["score"]:
                    logging.info("[SUCCESS] Retrieved assessment data matches the created data")
                    
                    # Try to delete the assessment
                    delete_response = requests.delete(
                        f"{API_URL}/assessments/{assessment_id}",
                        headers=headers
                    )
                    
                    if delete_response.status_code in [200, 204]:
                        logging.info(f"[SUCCESS] Successfully deleted assessment with ID {assessment_id}")
                    else:
                        logging.warning(f"[WARNING] Failed to delete assessment: {delete_response.status_code}")
                        logging.warning(f"Response text: {delete_response.text}")
                    
                    return True
                else:
                    logging.error("[ERROR] Retrieved assessment data does not match the created data")
                    return False
            else:
                logging.error(f"[ERROR] Failed to retrieve assessment: {get_response.status_code}")
                logging.error(f"Response text: {get_response.text}")
                return False
        else:
            logging.error(f"[ERROR] Failed to create assessment: {create_response.status_code}")
            logging.error(f"Response text: {create_response.text}")
            return False
    except Exception as e:
        logging.error(f"[ERROR] Error testing assessment creation and retrieval: {str(e)}")
        return False

def run_verification():
    """Run all verification tests for assessment history endpoints."""
    logging.info("=== Starting Assessment History Endpoint Verification with Direct Token ===")
    
    # Get JWT token from file
    token = get_token_from_file()
    if not token:
        logging.error("Failed to get token. Cannot proceed with tests.")
        sys.exit(1)  # Exit with non-zero code to indicate failure
    
    # Run all tests
    history_test = test_get_assessment_history(token)
    limit_test = test_get_assessment_history_with_limit(token)
    crud_test = test_create_and_get_assessment(token)
    
    # Summarize results
    logging.info("\n=== Verification Summary ===")
    logging.info(f"GET /assessments/history: {'[PASS]' if history_test else '[FAIL]'}")
    logging.info(f"GET /assessments/history?limit=3: {'[PASS]' if limit_test else '[FAIL]'}")
    logging.info(f"Create, Get, Delete Assessment: {'[PASS]' if crud_test else '[FAIL]'}")
    
    all_passed = history_test and limit_test and crud_test
    
    if all_passed:
        logging.info("\n[SUCCESS] All assessment history endpoints are working correctly!")
        return True
    else:
        logging.error("\n[FAILURE] Some assessment history endpoints are not working correctly.")
        sys.exit(1)  # Exit with non-zero code to indicate failure

if __name__ == "__main__":
    run_verification()

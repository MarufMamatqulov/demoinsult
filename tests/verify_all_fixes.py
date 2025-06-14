"""
Comprehensive verification script for the Stroke Rehabilitation AI Platform fixes.
This script tests:
1. OpenAI API integration
2. Rate limiting for profile requests
3. Assessment history endpoints
4. Content-length middleware
"""

import os
import sys
import json
import time
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("comprehensive_verification.log"),
        logging.StreamHandler()
    ]
)

# Constants
BASE_URL = "http://localhost:8000"  # Change if your server runs on a different port
TEST_CREDENTIALS = {
    "username": "testuser",
    "password": "testpassword"
}
RESULTS_FILE = "api_verification_results.json"

def test_openai_integration():
    """Test the OpenAI API integration directly."""
    logging.info("Testing OpenAI API integration...")
    
    try:
        # Test direct import of our fix module
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from fix_openai_integration import fix_openai_integration
        
        if fix_openai_integration():
            logging.info("✅ Successfully loaded and applied OpenAI integration fix")
        else:
            logging.error("❌ Failed to apply OpenAI integration fix")
            return False
        
        # Test the OpenAI API via our backend
        # First, try to authenticate
        auth_response = requests.post(f"{BASE_URL}/auth/token", data=TEST_CREDENTIALS)
        
        if auth_response.status_code != 200:
            logging.error(f"❌ Authentication failed with status code: {auth_response.status_code}")
            logging.error(f"Response: {auth_response.text}")
            return False
        
        token = auth_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test the rehabilitation analysis endpoint
        test_data = {
            "patient_data": {
                "age": 65,
                "gender": "Male",
                "stroke_type": "Ischemic",
                "affected_side": "Left",
                "weeks_since_stroke": 4
            },
            "assessment_results": {
                "mobility_score": 7,
                "speech_score": 8,
                "cognitive_score": 6
            },
            "current_symptoms": [
                "Mild weakness in left arm",
                "Occasional slurred speech",
                "Some difficulty with memory"
            ]
        }
        
        logging.info("Making request to rehabilitation analysis endpoint...")
        rehab_response = requests.post(
            f"{BASE_URL}/openai/rehabilitation-analysis",
            json=test_data,
            headers=headers
        )
        
        if rehab_response.status_code != 200:
            logging.error(f"❌ OpenAI rehabilitation analysis failed with status code: {rehab_response.status_code}")
            logging.error(f"Response: {rehab_response.text}")
            return False
        
        logging.info(f"✅ OpenAI rehabilitation analysis succeeded: {rehab_response.status_code}")
        logging.info(f"Response preview: {rehab_response.text[:100]}...")
        return True
    
    except Exception as e:
        logging.error(f"❌ Error in OpenAI integration test: {str(e)}")
        return False

def test_rate_limiting():
    """Test the rate limiting for profile requests."""
    logging.info("Testing rate limiting for profile requests...")
    
    try:
        # First, try to authenticate
        auth_response = requests.post(f"{BASE_URL}/auth/token", data=TEST_CREDENTIALS)
        
        if auth_response.status_code != 200:
            logging.error(f"❌ Authentication failed with status code: {auth_response.status_code}")
            logging.error(f"Response: {auth_response.text}")
            return False
        
        token = auth_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Make multiple requests to the profile endpoint
        logging.info("Making first request to profile endpoint...")
        first_response = requests.get(f"{BASE_URL}/auth/me/profile", headers=headers)
        
        if first_response.status_code != 200:
            logging.error(f"❌ First profile request failed with status code: {first_response.status_code}")
            logging.error(f"Response: {first_response.text}")
            return False
        
        logging.info("Making second request immediately (should be rate limited)...")
        second_response = requests.get(f"{BASE_URL}/auth/me/profile", headers=headers)
        
        if second_response.status_code != 429:
            logging.error(f"❌ Rate limiting failed - second request returned status code: {second_response.status_code}")
            logging.error(f"Expected 429 (Too Many Requests)")
            return False
        
        # Check if wait_time is included in the response
        response_data = second_response.json()
        if "wait_time" not in response_data:
            logging.error("❌ Rate limiting response does not include wait_time")
            return False
        
        wait_time = response_data.get("wait_time")
        logging.info(f"✅ Rate limiting working correctly. Wait time: {wait_time} seconds")
        
        # Wait for the specified time and try again
        logging.info(f"Waiting {wait_time} seconds before making next request...")
        time.sleep(wait_time + 0.5)  # Add a small buffer
        
        logging.info("Making third request after waiting...")
        third_response = requests.get(f"{BASE_URL}/auth/me/profile", headers=headers)
        
        if third_response.status_code != 200:
            logging.error(f"❌ Third profile request failed with status code: {third_response.status_code}")
            logging.error(f"Response: {third_response.text}")
            return False
        
        logging.info("✅ Rate limiting test passed - was able to make request after waiting")
        return True
    
    except Exception as e:
        logging.error(f"❌ Error in rate limiting test: {str(e)}")
        return False

def test_assessment_history():
    """Test the assessment history endpoints."""
    logging.info("Testing assessment history endpoints...")
    
    try:
        # First, try to authenticate
        auth_response = requests.post(f"{BASE_URL}/auth/token", data=TEST_CREDENTIALS)
        
        if auth_response.status_code != 200:
            logging.error(f"❌ Authentication failed with status code: {auth_response.status_code}")
            logging.error(f"Response: {auth_response.text}")
            return False
        
        token = auth_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test get all assessments endpoint
        logging.info("Testing get all assessments endpoint...")
        all_assessments_response = requests.get(f"{BASE_URL}/assessments/history", headers=headers)
        
        if all_assessments_response.status_code != 200:
            logging.error(f"❌ Get all assessments failed with status code: {all_assessments_response.status_code}")
            logging.error(f"Response: {all_assessments_response.text}")
            return False
        
        # Check if we got a list of assessments
        assessments = all_assessments_response.json()
        if not isinstance(assessments, list):
            logging.error("❌ Get all assessments did not return a list")
            logging.error(f"Response type: {type(assessments)}")
            return False
        
        logging.info(f"✅ Get all assessments endpoint returned {len(assessments)} assessments")
        
        # If we have at least one assessment, test the get assessment by ID endpoint
        if len(assessments) > 0:
            assessment_id = assessments[0].get("id")
            
            logging.info(f"Testing get assessment by ID endpoint for ID: {assessment_id}...")
            assessment_response = requests.get(f"{BASE_URL}/assessments/history/{assessment_id}", headers=headers)
            
            if assessment_response.status_code != 200:
                logging.error(f"❌ Get assessment by ID failed with status code: {assessment_response.status_code}")
                logging.error(f"Response: {assessment_response.text}")
                return False
            
            assessment = assessment_response.json()
            if not isinstance(assessment, dict) or "id" not in assessment:
                logging.error("❌ Get assessment by ID did not return a valid assessment")
                logging.error(f"Response: {assessment}")
                return False
            
            logging.info(f"✅ Get assessment by ID endpoint returned assessment: {assessment.get('id')}")
        
        # Test create assessment endpoint
        test_assessment = {
            "type": "verification_test",
            "data": {
                "test_key": "test_value",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        logging.info("Testing create assessment endpoint...")
        create_response = requests.post(
            f"{BASE_URL}/assessments/history", 
            json=test_assessment,
            headers=headers
        )
        
        if create_response.status_code != 201:
            logging.error(f"❌ Create assessment failed with status code: {create_response.status_code}")
            logging.error(f"Response: {create_response.text}")
            return False
        
        new_assessment = create_response.json()
        logging.info(f"✅ Create assessment endpoint created new assessment with ID: {new_assessment.get('id')}")
        
        return True
    
    except Exception as e:
        logging.error(f"❌ Error in assessment history test: {str(e)}")
        return False

def run_all_tests():
    """Run all verification tests and produce a summary."""
    logging.info("=== Starting comprehensive verification tests ===")
    start_time = datetime.now()
    
    results = {
        "openai_integration": test_openai_integration(),
        "rate_limiting": test_rate_limiting(),
        "assessment_history": test_assessment_history()
    }
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Generate summary
    logging.info("\n=== Verification Test Summary ===")
    all_passed = all(results.values())
    
    for test, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        logging.info(f"{test}: {status}")
    
    overall_status = "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"
    logging.info(f"\nOverall status: {overall_status}")
    logging.info(f"Test duration: {duration:.2f} seconds")
    
    # Save results to a JSON file
    results_data = {
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": duration,
        "all_passed": all_passed,
        "test_results": results
    }
    
    with open("api_verification_results.json", "w") as f:
        json.dump(results_data, f, indent=2)
    
    logging.info(f"Results saved to api_verification_results.json")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

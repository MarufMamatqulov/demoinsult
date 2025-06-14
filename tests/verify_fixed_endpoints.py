"""
Final endpoint verification script for the Stroke Rehabilitation AI Platform.
This script tests all previously failing endpoints to ensure they're now working properly.
"""

import requests
import json
import logging
import sys
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('final_endpoint_verification.log')
    ]
)

# API base URL
API_URL = "http://localhost:8000"

# Test user credentials
TEST_USER = {
    "email": "test@example.com",
    "password": "Password123!"
}

def test_server_health():
    """Check if the server is running and responding."""
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            logging.info("✅ Server is running")
            return True
        else:
            logging.error(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"❌ Server connection failed: {str(e)}")
        return False

def get_auth_token():
    """Get authentication token for the test user."""
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={
                "username": TEST_USER["email"],
                "password": TEST_USER["password"]
            }
        )
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            logging.info("✅ Successfully obtained authentication token")
            return token
        else:
            logging.error(f"❌ Authentication failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"❌ Authentication error: {str(e)}")
        return None

def test_assessment_history(token):
    """Test assessment history endpoints."""
    if not token:
        logging.error("❌ Cannot test assessment history without authentication")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    success = True
    
    # Test getting assessment history
    try:
        response = requests.get(f"{API_URL}/assessments/history", headers=headers)
        
        if response.status_code == 200:
            assessments = response.json()
            logging.info(f"✅ Successfully retrieved {len(assessments)} assessments")
            
            # Log the first assessment data structure if available
            if assessments:
                logging.info(f"Sample assessment data structure: {json.dumps(assessments[0], indent=2, default=str)}")
        else:
            logging.error(f"❌ Failed to get assessment history: {response.status_code} - {response.text}")
            success = False
    except Exception as e:
        logging.error(f"❌ Error testing assessment history: {str(e)}")
        success = False
    
    # Test creating a new assessment
    try:
        test_data = {
            "type": "test_assessment",
            "data": {
                "score": 85,
                "maxScore": 100,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        response = requests.post(
            f"{API_URL}/assessments/",
            headers=headers,
            json=test_data
        )
        
        if response.status_code == 201:
            new_assessment = response.json()
            assessment_id = new_assessment.get("id")
            logging.info(f"✅ Successfully created assessment with ID {assessment_id}")
            
            # Test getting a specific assessment
            try:
                response = requests.get(
                    f"{API_URL}/assessments/{assessment_id}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    assessment = response.json()
                    logging.info(f"✅ Successfully retrieved assessment with ID {assessment_id}")
                    logging.info(f"Retrieved assessment data: {json.dumps(assessment, indent=2, default=str)}")
                else:
                    logging.error(f"❌ Failed to get specific assessment: {response.status_code} - {response.text}")
                    success = False
            except Exception as e:
                logging.error(f"❌ Error getting specific assessment: {str(e)}")
                success = False
        else:
            logging.error(f"❌ Failed to create assessment: {response.status_code} - {response.text}")
            success = False
    except Exception as e:
        logging.error(f"❌ Error creating assessment: {str(e)}")
        success = False
    
    return success

def test_patient_chat(token):
    """Test patient chat endpoint."""
    if not token:
        logging.error("❌ Cannot test patient chat without authentication")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    success = True
    
    try:
        chat_data = {
            "messages": [
                {"role": "user", "content": "What exercises can help me recover from a stroke?"}
            ],
            "language": "en"
        }
        
        response = requests.post(
            f"{API_URL}/chat/patient-chat",
            headers=headers,
            json=chat_data,
            timeout=15  # Longer timeout for AI response
        )
        
        if response.status_code == 200:
            chat_response = response.json()
            logging.info("✅ Successfully received patient chat response")
            
            # Log partial response content
            response_text = chat_response.get("response", "")
            logging.info(f"Response preview: {response_text[:100]}...")
        else:
            logging.error(f"❌ Failed to get patient chat response: {response.status_code} - {response.text}")
            success = False
    except Exception as e:
        logging.error(f"❌ Error testing patient chat: {str(e)}")
        success = False
    
    return success

def test_openai_completion(token):
    """Test OpenAI chat completion endpoint."""
    if not token:
        logging.error("❌ Cannot test OpenAI completion without authentication")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    success = True
    
    try:
        completion_data = {
            "messages": [
                {"role": "system", "content": "You are a helpful medical assistant specializing in stroke rehabilitation."},
                {"role": "user", "content": "What are some good exercises for improving hand mobility after a stroke?"}
            ]
        }
        
        response = requests.post(
            f"{API_URL}/openai/chat/completion",
            headers=headers,
            json=completion_data,
            timeout=15  # Longer timeout for AI response
        )
        
        if response.status_code == 200:
            completion_response = response.json()
            logging.info("✅ Successfully received OpenAI chat completion")
            
            # Log partial response content
            response_text = completion_response.get("response", "")
            logging.info(f"Response preview: {response_text[:100]}...")
        else:
            logging.error(f"❌ Failed to get OpenAI completion: {response.status_code} - {response.text}")
            success = False
    except Exception as e:
        logging.error(f"❌ Error testing OpenAI completion: {str(e)}")
        success = False
    
    return success

def run_verification():
    """Run the complete verification of all fixed endpoints."""
    logging.info("=== Starting Final Endpoint Verification ===")
    
    # Check if server is running
    if not test_server_health():
        logging.error("Server is not running. Cannot proceed with verification.")
        return False
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        logging.error("Failed to get authentication token. Cannot proceed with verification.")
        return False
    
    # Test all fixed endpoints
    assessment_success = test_assessment_history(token)
    chat_success = test_patient_chat(token)
    openai_success = test_openai_completion(token)
    
    # Summarize results
    logging.info("\n=== Verification Summary ===")
    logging.info(f"Assessment History Endpoints: {'✅ PASS' if assessment_success else '❌ FAIL'}")
    logging.info(f"Patient Chat Endpoint: {'✅ PASS' if chat_success else '❌ FAIL'}")
    logging.info(f"OpenAI Chat Completion: {'✅ PASS' if openai_success else '❌ FAIL'}")
    
    all_passed = assessment_success and chat_success and openai_success
    
    if all_passed:
        logging.info("\n✅ SUCCESS: All endpoints are working correctly!")
    else:
        logging.warning("\n⚠️ PARTIAL SUCCESS: Some endpoints are still not working correctly.")
    
    logging.info("=== Verification Complete ===")
    
    return all_passed

if __name__ == "__main__":
    run_verification()

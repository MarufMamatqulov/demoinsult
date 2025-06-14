"""
Verification script for the API endpoint fixes.
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
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('api_fixes_verification.log')
    ]
)

# API base URL
API_URL = os.getenv("API_URL", "http://localhost:8000")
TOKEN = None  # Will be set after login

def test_login():
    """Test user login and get token."""
    global TOKEN
    
    logging.info("Testing user login...")
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": "test@example.com", "password": "password123"}
        )
        
        if response.status_code == 200:
            data = response.json()
            TOKEN = data.get("access_token")
            logging.info(f"Login successful! Token received")
            return True
        else:
            logging.error(f"Login failed with status code {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Exception during login: {str(e)}")
        return False

def test_assessment_history():
    """Test the assessment history endpoints."""
    logging.info("\n=== Testing Assessment History Endpoints ===")
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Test GET /assessments/history
    logging.info("Testing GET /assessments/history...")
    try:
        response = requests.get(f"{API_URL}/assessments/history", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Successfully retrieved assessment history. Found {len(data)} assessments.")
            return True
        else:
            logging.error(f"Error retrieving assessment history: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"Exception during assessment history retrieval: {str(e)}")
        return False

def test_create_assessment():
    """Test creating a new assessment."""
    logging.info("\n=== Testing Assessment Creation ===")
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Sample assessment data
    assessment_data = {
        "type": "blood_pressure",
        "data": {
            "systolic": 120,
            "diastolic": 80,
            "pulse": 72,
            "timestamp": datetime.now().isoformat()
        }
    }
    
    # Test POST /assessments/
    logging.info("Testing POST /assessments/...")
    try:
        response = requests.post(
            f"{API_URL}/assessments/", 
            headers=headers, 
            json=assessment_data
        )
        
        if response.status_code == 201:
            data = response.json()
            assessment_id = data.get("id")
            logging.info(f"Successfully created assessment with ID: {assessment_id}")
            
            # Now test getting this specific assessment
            return test_get_assessment_by_id(assessment_id)
        else:
            logging.error(f"Error creating assessment: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"Exception during assessment creation: {str(e)}")
        return False

def test_get_assessment_by_id(assessment_id):
    """Test getting a specific assessment by ID."""
    logging.info(f"\n=== Testing Get Assessment by ID ({assessment_id}) ===")
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Test GET /assessments/{assessment_id}
    logging.info(f"Testing GET /assessments/{assessment_id}...")
    try:
        response = requests.get(f"{API_URL}/assessments/{assessment_id}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Successfully retrieved assessment with ID: {assessment_id}")
            return True
        else:
            logging.error(f"Error retrieving assessment: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"Exception during assessment retrieval: {str(e)}")
        return False

def test_openai_chat():
    """Test the OpenAI chat integration."""
    logging.info("\n=== Testing OpenAI Chat Integration ===")
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Sample chat message
    chat_data = {
        "messages": [
            {"role": "user", "content": "What are some tips for stroke recovery?"}
        ],
        "language": "en"
    }
    
    # Test POST /openai/chat/completion
    logging.info("Testing POST /openai/chat/completion...")
    try:
        response = requests.post(
            f"{API_URL}/openai/chat/completion", 
            headers=headers, 
            json=chat_data
        )
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Successfully received chat response")
            # Log a snippet of the response
            response_text = data.get("response", "")
            logging.info(f"Response snippet: {response_text[:100]}...")
            return True
        else:
            logging.error(f"Error in chat completion: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"Exception during chat completion: {str(e)}")
        return False

def test_rehabilitation_analysis():
    """Test the rehabilitation analysis endpoint."""
    logging.info("\n=== Testing Rehabilitation Analysis ===")
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Sample assessment data for analysis
    analysis_data = {
        "assessment_type": "blood_pressure",
        "assessment_data": {
            "systolic": 140,
            "diastolic": 90,
            "pulse": 85,
            "timestamp": datetime.now().isoformat()
        },
        "language": "en"
    }
    
    # Test POST /openai/rehabilitation/analysis
    logging.info("Testing POST /openai/rehabilitation/analysis...")
    try:
        response = requests.post(
            f"{API_URL}/openai/rehabilitation/analysis", 
            headers=headers, 
            json=analysis_data
        )
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Successfully received rehabilitation analysis")
            # Log a snippet of the response
            response_text = data.get("response", "")
            logging.info(f"Response snippet: {response_text[:100]}...")
            
            # Check if recommendations were parsed
            recommendations = data.get("recommendations", [])
            logging.info(f"Received {len(recommendations)} recommendations")
            return True
        else:
            logging.error(f"Error in rehabilitation analysis: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"Exception during rehabilitation analysis: {str(e)}")
        return False

def run_all_tests():
    """Run all verification tests."""
    logging.info("Starting API fixes verification...")
    
    # Login first
    if not test_login():
        logging.error("Login failed. Cannot proceed with other tests.")
        return False
    
    # Run all tests
    assessment_history_result = test_assessment_history()
    create_assessment_result = test_create_assessment()
    openai_chat_result = test_openai_chat()
    rehabilitation_analysis_result = test_rehabilitation_analysis()
    
    # Summary
    logging.info("\n=== Verification Test Summary ===")
    logging.info(f"Assessment History Endpoint: {'PASS' if assessment_history_result else 'FAIL'}")
    logging.info(f"Assessment Creation & Retrieval: {'PASS' if create_assessment_result else 'FAIL'}")
    logging.info(f"OpenAI Chat Integration: {'PASS' if openai_chat_result else 'FAIL'}")
    logging.info(f"Rehabilitation Analysis: {'PASS' if rehabilitation_analysis_result else 'FAIL'}")
    
    all_passed = all([
        assessment_history_result, 
        create_assessment_result,
        openai_chat_result,
        rehabilitation_analysis_result
    ])
    
    if all_passed:
        logging.info("All tests PASSED! The API fixes are working correctly.")
    else:
        logging.warning("Some tests FAILED. Please check the logs for details.")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()

"""
Final verification script for the API endpoint fixes.
This script will test all endpoints that were fixed to ensure they're working correctly.
"""

import requests
import time
import logging
import sys
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('final_api_verification.log')
    ]
)

# API base URL
API_URL = "http://localhost:8000"

# Test data
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "Password123!"
}

def check_server_status():
    """Check if the API server is running."""
    logging.info("Checking server status...")
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            logging.info("Server is running!")
            return True
        else:
            logging.error(f"Server responded with status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Failed to connect to server: {str(e)}")
        return False

def test_endpoints_without_auth():
    """Test the endpoints without authentication to verify they respond with 401 and not 500."""
    logging.info("\n=== Testing endpoints without authentication ===")
    endpoints = [
        ("/assessments/history", "GET"),
        ("/openai/chat/completion", "POST", {"messages": [{"role": "user", "content": "test"}]}),
        ("/chat/patient-chat", "POST", {"messages": [{"role": "user", "content": "test"}]})
    ]
    
    results = {}
    
    for endpoint_info in endpoints:
        if len(endpoint_info) == 2:
            endpoint, method = endpoint_info
            data = None
        else:
            endpoint, method, data = endpoint_info
            
        logging.info(f"Testing {method} {endpoint}")
        
        try:
            if method == "GET":
                response = requests.get(f"{API_URL}{endpoint}", timeout=5)
            else:
                response = requests.post(f"{API_URL}{endpoint}", json=data, timeout=5)
                
            if response.status_code == 401 or response.status_code == 403:
                logging.info(f"✅ Success: {method} {endpoint} requires authentication (status: {response.status_code})")
                results[endpoint] = "PASS"
            elif response.status_code == 500:
                logging.error(f"❌ Failed: {method} {endpoint} returned 500 error")
                results[endpoint] = "FAIL"
            else:
                logging.warning(f"⚠️ Warning: {method} {endpoint} returned unexpected status code {response.status_code}")
                results[endpoint] = "WARNING"
        except Exception as e:
            logging.error(f"❌ Error testing {method} {endpoint}: {str(e)}")
            results[endpoint] = "ERROR"
    
    return results

def register_user():
    """Register a test user for authenticated tests."""
    logging.info("\n=== Registering test user ===")
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json=TEST_USER
        )
        
        if response.status_code == 201 or response.status_code == 200:
            logging.info("✅ User registered successfully")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
            logging.info("ℹ️ User already exists, proceeding with login")
            return True
        else:
            logging.error(f"❌ Failed to register user: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"❌ Error registering user: {str(e)}")
        return False

def login_user():
    """Log in the test user and get authentication token."""
    logging.info("\n=== Logging in test user ===")
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={
                "username": TEST_USER["email"],
                "password": TEST_USER["password"]
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            logging.info("✅ Login successful")
            return token
        else:
            logging.error(f"❌ Failed to login: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"❌ Error logging in: {str(e)}")
        return None

def test_assessment_history(token):
    """Test the assessment history endpoints with authentication."""
    logging.info("\n=== Testing assessment history endpoints ===")
    
    if not token:
        logging.error("❌ No authentication token available")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    results = {}
    
    # Test GET /assessments/history
    try:
        logging.info("Testing GET /assessments/history")
        response = requests.get(
            f"{API_URL}/assessments/history",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"✅ Success: GET /assessments/history returned {len(data)} assessments")
            results["GET /assessments/history"] = "PASS"
        else:
            logging.error(f"❌ Failed: GET /assessments/history returned status {response.status_code}")
            results["GET /assessments/history"] = "FAIL"
    except Exception as e:
        logging.error(f"❌ Error testing GET /assessments/history: {str(e)}")
        results["GET /assessments/history"] = "ERROR"
    
    # Test POST /assessments/
    try:
        logging.info("Testing POST /assessments/")
        test_assessment = {
            "type": "test_assessment",
            "data": {
                "score": 10,
                "maxScore": 20,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        response = requests.post(
            f"{API_URL}/assessments/",
            headers=headers,
            json=test_assessment,
            timeout=5
        )
        
        if response.status_code == 201:
            data = response.json()
            assessment_id = data.get("id")
            logging.info(f"✅ Success: Created assessment with ID {assessment_id}")
            results["POST /assessments/"] = "PASS"
            
            # Test GET /assessments/{id}
            try:
                logging.info(f"Testing GET /assessments/{assessment_id}")
                response = requests.get(
                    f"{API_URL}/assessments/{assessment_id}",
                    headers=headers,
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logging.info(f"✅ Success: Retrieved assessment with ID {assessment_id}")
                    results[f"GET /assessments/{assessment_id}"] = "PASS"
                else:
                    logging.error(f"❌ Failed: GET /assessments/{assessment_id} returned status {response.status_code}")
                    results[f"GET /assessments/{assessment_id}"] = "FAIL"
            except Exception as e:
                logging.error(f"❌ Error testing GET /assessments/{assessment_id}: {str(e)}")
                results[f"GET /assessments/{assessment_id}"] = "ERROR"
        else:
            logging.error(f"❌ Failed: POST /assessments/ returned status {response.status_code}")
            results["POST /assessments/"] = "FAIL"
    except Exception as e:
        logging.error(f"❌ Error testing POST /assessments/: {str(e)}")
        results["POST /assessments/"] = "ERROR"
    
    return results

def test_openai_integration(token):
    """Test the OpenAI integration endpoints with authentication."""
    logging.info("\n=== Testing OpenAI integration endpoints ===")
    
    if not token:
        logging.error("❌ No authentication token available")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    results = {}
    
    # Test POST /openai/chat/completion
    try:
        logging.info("Testing POST /openai/chat/completion")
        chat_data = {
            "messages": [
                {"role": "user", "content": "What are some tips for stroke recovery?"}
            ],
            "language": "en"
        }
        
        response = requests.post(
            f"{API_URL}/openai/chat/completion",
            headers=headers,
            json=chat_data,
            timeout=10  # Longer timeout for AI response
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get("response", "")
            logging.info(f"✅ Success: OpenAI chat completion (first 50 chars): {response_text[:50]}...")
            results["POST /openai/chat/completion"] = "PASS"
        else:
            logging.error(f"❌ Failed: POST /openai/chat/completion returned status {response.status_code}")
            logging.error(f"Response: {response.text}")
            results["POST /openai/chat/completion"] = "FAIL"
    except Exception as e:
        logging.error(f"❌ Error testing POST /openai/chat/completion: {str(e)}")
        results["POST /openai/chat/completion"] = "ERROR"
    
    # Test POST /chat/patient-chat
    try:
        logging.info("Testing POST /chat/patient-chat")
        patient_chat_data = {
            "messages": [
                {"role": "user", "content": "What exercises can help me recover from a stroke?"}
            ],
            "language": "en"
        }
        
        response = requests.post(
            f"{API_URL}/chat/patient-chat",
            headers=headers,
            json=patient_chat_data,
            timeout=10  # Longer timeout for AI response
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get("response", "")
            logging.info(f"✅ Success: Patient chat (first 50 chars): {response_text[:50]}...")
            results["POST /chat/patient-chat"] = "PASS"
        else:
            logging.error(f"❌ Failed: POST /chat/patient-chat returned status {response.status_code}")
            logging.error(f"Response: {response.text}")
            results["POST /chat/patient-chat"] = "FAIL"
    except Exception as e:
        logging.error(f"❌ Error testing POST /chat/patient-chat: {str(e)}")
        results["POST /chat/patient-chat"] = "ERROR"
    
    return results

def run_verification():
    """Run the complete verification process."""
    logging.info("=== Starting API Fixes Verification ===")
    logging.info(f"Testing API at: {API_URL}")
    
    # Check if server is running
    if not check_server_status():
        logging.error("Server is not running or not responding. Please start the server and try again.")
        return False
    
    # Test endpoints without authentication
    unauthenticated_results = test_endpoints_without_auth()
    
    # Register and login a test user
    if not register_user():
        logging.error("Failed to register test user. Cannot proceed with authenticated tests.")
        return False
    
    token = login_user()
    if not token:
        logging.error("Failed to login. Cannot proceed with authenticated tests.")
        return False
    
    # Test with authentication
    assessment_results = test_assessment_history(token)
    openai_results = test_openai_integration(token)
    
    # Combine all results
    all_results = {
        "Unauthenticated Endpoints": unauthenticated_results,
        "Assessment History Endpoints": assessment_results,
        "OpenAI Integration Endpoints": openai_results
    }
    
    # Generate overall result
    all_tests_passed = all(
        result == "PASS" 
        for category in all_results.values() 
        for result in category.values()
    )
    
    # Print summary
    logging.info("\n=== Verification Summary ===")
    for category, results in all_results.items():
        logging.info(f"\n{category}:")
        for endpoint, result in results.items():
            icon = "✅" if result == "PASS" else "❌" if result == "FAIL" else "⚠️"
            logging.info(f"{icon} {endpoint}: {result}")
    
    if all_tests_passed:
        logging.info("\n✅ SUCCESS: All tests passed! The API fixes are working correctly.")
    else:
        logging.warning("\n⚠️ PARTIAL SUCCESS: Some tests failed. Check the log for details.")
    
    # Write results to a JSON file
    with open("api_verification_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    logging.info(f"\nDetailed results written to api_verification_results.json")
    logging.info("=== Verification Complete ===")
    
    return all_tests_passed

if __name__ == "__main__":
    run_verification()

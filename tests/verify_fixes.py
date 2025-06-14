import requests
import json
import time
import sys
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fixes_verification.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def test_openai_integration():
    """Test the OpenAI integration with a simple request."""
    logging.info("Testing OpenAI integration...")
    
    # Make a request to the rehabilitation analysis endpoint
    url = "http://localhost:8000/ai/rehabilitation/analysis"
    headers = {"Content-Type": "application/json"}
    data = {
        "assessment_data": {"score": 5, "max_score": 10},
        "assessment_type": "test",
        "language": "en"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        logging.info(f"OpenAI integration status code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            logging.info(f"OpenAI response received: {response_data}")
            
            # Check for error messages indicating API key issues
            if "trouble connecting" in response_data.get("response", ""):
                logging.error("OpenAI API key issue detected in response")
                return False
            
            logging.info("OpenAI integration test passed!")
            return True
        else:
            logging.error(f"OpenAI integration test failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error testing OpenAI integration: {str(e)}")
        return False

def test_rate_limiting():
    """Test the rate limiting implementation for profile requests."""
    logging.info("Testing rate limiting for profile requests...")
    
    # Make multiple requests in quick succession
    url = "http://localhost:8000/auth/me/profile"
    headers = {"host": "test-client"}
    
    # Try to get a valid JWT token
    try:
        auth_url = "http://localhost:8000/auth/login"
        auth_data = {
            "username": "test@example.com",
            "password": "Password123!"
        }
        auth_response = requests.post(auth_url, json=auth_data)
        
        if auth_response.status_code == 200:
            token = auth_response.json().get("access_token")
            headers["Authorization"] = f"Bearer {token}"
        else:
            logging.warning(f"Could not get authentication token: {auth_response.status_code} - {auth_response.text}")
    except Exception as e:
        logging.warning(f"Error getting authentication token: {str(e)}")
    
    # First request should succeed
    logging.info("Making first request...")
    try:
        response1 = requests.get(url, headers=headers)
        logging.info(f"First request status: {response1.status_code}")
        
        # Second immediate request should be rate limited
        logging.info("Making immediate second request (should be rate limited)...")
        response2 = requests.get(url, headers=headers)
        logging.info(f"Second request status: {response2.status_code}")
        
        if response2.status_code == 429:
            logging.info(f"Rate limiting working correctly! Response: {response2.text}")
            
            # Check if the response contains wait_time
            try:
                response_data = response2.json()
                if "wait_time" in response_data:
                    logging.info(f"Wait time included in response: {response_data['wait_time']} seconds")
                else:
                    logging.warning("Wait time not included in rate limiting response")
            except:
                logging.warning("Could not parse rate limiting response as JSON")
            
            # Wait for 11 seconds (more than the 10-second window)
            logging.info("Waiting for 11 seconds...")
            time.sleep(11)
            
            # Third request after waiting should succeed
            logging.info("Making third request after waiting...")
            response3 = requests.get(url, headers=headers)
            logging.info(f"Third request status: {response3.status_code}")
            
            if response3.status_code == 200 or response3.status_code == 401:
                # 401 is acceptable if we couldn't get a valid token
                logging.info("Rate limiting test passed!")
                return True
            else:
                logging.error(f"Third request failed with unexpected status: {response3.status_code}")
                return False
        else:
            logging.error(f"Rate limiting not working - second request should have been blocked but got {response2.status_code}")
            return False
    except Exception as e:
        logging.error(f"Error testing rate limiting: {str(e)}")
        return False

def test_assessment_history():
    """Test the assessment history endpoints."""
    logging.info("Testing assessment history endpoints...")
    
    # Get authentication token
    try:
        auth_url = "http://localhost:8000/auth/login"
        auth_data = {
            "username": "test@example.com",
            "password": "Password123!"
        }
        auth_response = requests.post(auth_url, json=auth_data)
        
        if auth_response.status_code != 200:
            logging.error(f"Could not get authentication token: {auth_response.status_code} - {auth_response.text}")
            return False
        
        token = auth_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test assessment history endpoint
        url = "http://localhost:8000/assessments/history"
        logging.info(f"Testing GET {url}...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            assessments = response.json()
            logging.info(f"Successfully retrieved {len(assessments)} assessments")
            
            # Test with limit parameter
            url_with_limit = "http://localhost:8000/assessments/history?limit=3"
            logging.info(f"Testing GET {url_with_limit}...")
            response_with_limit = requests.get(url_with_limit, headers=headers)
            
            if response_with_limit.status_code == 200:
                limited_assessments = response_with_limit.json()
                logging.info(f"Successfully retrieved {len(limited_assessments)} assessments with limit")
                
                if len(limited_assessments) <= 3:
                    logging.info("Assessment history tests passed!")
                    return True
                else:
                    logging.error(f"Limit parameter not working correctly. Got {len(limited_assessments)} assessments with limit=3")
                    return False
            else:
                logging.error(f"Assessment history with limit test failed: {response_with_limit.status_code} - {response_with_limit.text}")
                return False
        else:
            logging.error(f"Assessment history test failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error testing assessment history: {str(e)}")
        return False

if __name__ == "__main__":
    logging.info("Starting verification of fixes...")
    
    # Test OpenAI integration
    openai_success = test_openai_integration()
    
    # Test rate limiting
    rate_limiting_success = test_rate_limiting()
    
    # Test assessment history
    assessment_history_success = test_assessment_history()
    
    # Print summary
    logging.info("\n=== Verification Summary ===")
    logging.info(f"OpenAI Integration: {'✅ PASS' if openai_success else '❌ FAIL'}")
    logging.info(f"Rate Limiting: {'✅ PASS' if rate_limiting_success else '❌ FAIL'}")
    logging.info(f"Assessment History: {'✅ PASS' if assessment_history_success else '❌ FAIL'}")
    
    # Exit with appropriate code
    if openai_success and rate_limiting_success and assessment_history_success:
        logging.info("All tests passed! The fixes are working correctly.")
        sys.exit(0)
    else:
        logging.error("Some tests failed. Check the logs for details.")
        sys.exit(1)

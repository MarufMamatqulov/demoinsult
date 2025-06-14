"""
Comprehensive Authentication System Verification Script

This script verifies that all parts of the authentication system are working correctly,
including user registration, login, token-based authentication, and model relationships.
"""

import os
import sys
import logging
import random
import string
import json
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("auth_verification.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("auth_verification")

# Configuration
BASE_URL = "http://localhost:8000"
AUTH_ENDPOINTS = {
    "register": "/auth/register",
    "login": "/auth/login",
    "me": "/auth/me"
}

def generate_random_string(length=8):
    """Generate a random string for test user data."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_test_user():
    """Generate random test user data."""
    random_suffix = generate_random_string()
    return {
        "email": f"test_verify_{random_suffix}@example.com",
        "username": f"testuser_verify_{random_suffix}",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "Verification"
    }

def test_registration(test_user):
    """Test the user registration endpoint."""
    url = f"{BASE_URL}{AUTH_ENDPOINTS['register']}"
    
    logger.info("=== Testing User Registration ===")
    logger.info(f"POST {url}")
    logger.info(f"Data: {json.dumps(test_user, indent=2)}")
    
    try:
        response = requests.post(url, json=test_user, timeout=30)
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            response_data = response.json()
            logger.info(f"Response: {json.dumps(response_data, indent=2)}")
            logger.info("✅ Registration successful!")
            return response_data
        else:
            logger.error(f"Response: {response.text}")
            logger.error("❌ Registration failed.")
            return None
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        logger.error("❌ Registration failed.")
        return None

def test_login(credentials):
    """Test the user login endpoint."""
    url = f"{BASE_URL}{AUTH_ENDPOINTS['login']}"
    
    logger.info("\n=== Testing User Login ===")
    logger.info(f"POST {url}")
    
    login_data = {
        "username": credentials["email"],  # Try with email
        "password": credentials["password"]
    }
    
    logger.info(f"Form data: {json.dumps(login_data, indent=2)}")
    
    try:
        response = requests.post(url, data=login_data, timeout=30)
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            logger.info(f"Response: {json.dumps(response_data, indent=2)}")
            logger.info("✅ Login successful!")
            return response_data.get("access_token")
        else:
            logger.error(f"Response: {response.text}")
            logger.error("❌ Login failed.")
            
            # Try with username instead of email
            logger.info("Trying login with username instead of email...")
            login_data["username"] = credentials["username"]
            
            response = requests.post(url, data=login_data, timeout=30)
            logger.info(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                logger.info(f"Response: {json.dumps(response_data, indent=2)}")
                logger.info("✅ Login successful with username!")
                return response_data.get("access_token")
            else:
                logger.error(f"Response: {response.text}")
                logger.error("❌ Login failed with username too.")
                return None
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        logger.error("❌ Login failed.")
        return None

def test_current_user(token):
    """Test getting the current user using the token."""
    if not token:
        logger.error("\n⚠️ Skipping current user test due to missing token.")
        return None
    
    url = f"{BASE_URL}{AUTH_ENDPOINTS['me']}"
    
    logger.info("\n=== Testing Get Current User ===")
    logger.info(f"GET {url}")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            logger.info(f"Response: {json.dumps(response_data, indent=2)}")
            logger.info("✅ Get current user successful!")
            return response_data
        else:
            logger.error(f"Response: {response.text}")
            logger.error("❌ Get current user failed.")
            return None
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        logger.error("❌ Get current user failed.")
        return None

def verify_user_profile_relationship():
    """Verify the user-profile relationship in the database."""
    logger.info("\n=== Verifying User-Profile Relationship ===")
    
    # Add the backend directory to Python path
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(parent_dir, "backend")
    sys.path.insert(0, backend_dir)
    
    try:
        # Import after setting up the path
        from models.user import User, UserProfile
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        # Database connection
        DB_PATH = os.path.join(backend_dir, "test.db")
        DB_URL = f"sqlite:///{DB_PATH}"
        engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        session = SessionLocal()
        
        try:
            # Get our test user
            user = session.query(User).filter(User.email.like("test_%")).first()
            
            if not user:
                logger.error("No test user found in the database!")
                return False
                
            logger.info(f"Found user: {user.username} (ID: {user.id})")
            
            # Check profile relationship
            if user.profile:
                logger.info(f"User has profile with ID: {user.profile.id}")
                logger.info("✓ User-profile relationship works correctly!")
                return True
            else:
                logger.error("User doesn't have a profile or relationship is broken")
                
                # Check if profile exists but relationship is broken
                profile = session.query(UserProfile).filter(UserProfile.user_id == user.id).first()
                if profile:
                    logger.error(f"Profile exists (ID: {profile.id}) but relationship is broken")
                    return False
                else:
                    logger.info("No profile found, which is unusual for a registered user")
                    return False
        finally:
            session.close()
    except Exception as e:
        logger.error(f"Error verifying relationship: {str(e)}")
        return False

def main():
    """Run all verification tests."""
    logger.info("=================================================")
    logger.info(f"AUTH SYSTEM VERIFICATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=================================================")
    
    # 1. Test registration
    test_user = generate_test_user()
    user_data = test_registration(test_user)
    
    # 2. Test login
    if user_data:
        token = test_login(test_user)
    else:
        logger.error("Skipping login test because registration failed")
        token = None
    
    # 3. Test current user
    if token:
        user_info = test_current_user(token)
    else:
        logger.error("Skipping current user test because login failed")
        user_info = None
    
    # 4. Verify database relationships
    db_verification = verify_user_profile_relationship()
    
    # Check overall results
    if user_data and token and user_info and db_verification:
        logger.info("\n✅ ALL AUTHENTICATION VERIFICATION TESTS PASSED SUCCESSFULLY!")
        return True
    else:
        failed_tests = []
        if not user_data:
            failed_tests.append("Registration")
        if not token:
            failed_tests.append("Login")
        if not user_info:
            failed_tests.append("Current User")
        if not db_verification:
            failed_tests.append("Database Relationships")
        
        logger.error(f"\n❌ AUTHENTICATION VERIFICATION FAILED! Failed tests: {', '.join(failed_tests)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)  # Exit with status code based on test results
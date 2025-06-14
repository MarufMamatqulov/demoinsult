"""
JWT Token Validation Check Script for Assessment History Endpoints

This script inspects the JWT token validation in the assessment history endpoints.
"""

import os
import sys
import logging
import inspect
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def check_jwt_secret_consistency():
    """Check if the JWT secret key is consistent across the application."""
    try:
        # Import secrets from auth module
        from backend.core.auth import SECRET_KEY as auth_secret
        
        # Check if there are other places where JWT secrets are defined
        jwt_secrets = []
        
        # Check in config
        try:
            from backend.core.config import JWT_SECRET_KEY as config_secret
            jwt_secrets.append(("config.py", config_secret))
        except ImportError:
            logging.info("No JWT_SECRET_KEY found in config.py")
        
        # Add the auth secret
        jwt_secrets.append(("auth.py", auth_secret))
        
        # Report findings
        if len(jwt_secrets) > 1:
            logging.warning("Multiple JWT secret keys found:")
            for location, secret in jwt_secrets:
                masked_secret = secret[:5] + "..." + secret[-5:] if len(secret) > 10 else "***"
                logging.warning(f"  - {location}: {masked_secret}")
            
            # Check if they're all the same
            all_same = all(secret == jwt_secrets[0][1] for _, secret in jwt_secrets[1:])
            if all_same:
                logging.info("All JWT secrets are identical (good)")
            else:
                logging.error("JWT secrets are different! This will cause authentication failures")
                return False
        else:
            logging.info(f"Found single JWT secret in {jwt_secrets[0][0]}")
        
        return True
    except Exception as e:
        logging.error(f"Error checking JWT secrets: {e}")
        return False

def check_token_validation_code():
    """Check the token validation code in the auth module."""
    try:
        # Import token validation function
        from backend.core.auth import decode_access_token
        
        # Get the source code of the function
        source = inspect.getsource(decode_access_token)
        logging.info("Token validation function source:")
        logging.info(source)
        
        # Check for common issues
        if "try:" in source and "except" in source:
            logging.info("Function has error handling (good)")
        else:
            logging.warning("Function lacks error handling")
        
        if "verify_signature=True" in source:
            logging.info("JWT signature verification is enabled (good)")
        
        return True
    except Exception as e:
        logging.error(f"Error checking token validation code: {e}")
        return False

def check_assessment_auth_dependencies():
    """Check what authentication dependencies the assessment endpoints use."""
    try:
        # Import the assessment history router
        from backend.api.assessment_history import router
        
        # Find all route dependencies
        auth_deps = set()
        for route in router.routes:
            for dep in route.dependencies:
                # Convert dependency to string to check what it is
                dep_str = str(dep)
                if "auth" in dep_str.lower() or "token" in dep_str.lower() or "current_user" in dep_str.lower():
                    auth_deps.add(dep_str)
        
        logging.info(f"Found {len(auth_deps)} authentication dependencies in assessment history endpoints:")
        for dep in auth_deps:
            logging.info(f"  - {dep}")
        
        # Import the get_current_user function
        from backend.core.auth import get_current_user
        logging.info("Current user function source:")
        logging.info(inspect.getsource(get_current_user))
        
        return True
    except Exception as e:
        logging.error(f"Error checking assessment auth dependencies: {e}")
        return False

def main():
    """Main function to check JWT token validation."""
    logging.info("Starting JWT Token Validation Checks...")
    
    # Check JWT secret consistency
    logging.info("\n=== Checking JWT Secret Consistency ===")
    check_jwt_secret_consistency()
    
    # Check token validation code
    logging.info("\n=== Checking Token Validation Code ===")
    check_token_validation_code()
    
    # Check assessment auth dependencies
    logging.info("\n=== Checking Assessment Auth Dependencies ===")
    check_assessment_auth_dependencies()
    
    # Report summary
    logging.info("\n=== JWT Token Validation Check Summary ===")
    logging.info("1. JWT Secret Consistency: Checked")
    logging.info("2. Token Validation Code: Checked")
    logging.info("3. Assessment Auth Dependencies: Checked")
    
    logging.info("\nRecommended fix: Add better error handling to JWT token validation")
    
    return True

if __name__ == "__main__":
    main()

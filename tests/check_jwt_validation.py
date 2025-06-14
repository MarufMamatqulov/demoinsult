"""
JWT Token Validation Fix Script for Assessment History Endpoints

This script inspects and patches the JWT token validation in the assessment history endpoints.
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

def create_auth_patch_file():
    """Create a patch file to fix authentication issues."""
    patch_file = os.path.join(project_root, "backend", "fixes", "auth_fixes.py")
    os.makedirs(os.path.dirname(patch_file), exist_ok=True)
    
    content = """
# Authentication Fixes for Assessment History Endpoints

from functools import wraps
import logging
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

# Import the original functions we need to fix
from backend.core.auth import (
    oauth2_scheme, 
    SECRET_KEY, 
    ALGORITHM,
    get_user_by_id
)

# Enhanced token decoding with better error handling
def enhanced_decode_access_token(token):
    """
    Enhanced token decoding with better error logging.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            logging.error("Token missing 'sub' claim")
            return None
        return payload
    except JWTError as e:
        logging.error(f"JWT Error: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error decoding token: {str(e)}")
        return None

# Enhanced current user function with better error reporting
async def enhanced_get_current_user(token: str = Depends(oauth2_scheme), db = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Log the token for debugging (masked for security)
    token_sample = token[:10] + "..." if token and len(token) > 10 else "Invalid token"
    logging.info(f"Processing authentication token: {token_sample}")
    
    try:
        payload = enhanced_decode_access_token(token)
        if payload is None:
            logging.error("Token decode returned None")
            raise credentials_exception
            
        user_id = payload.get("sub")
        if user_id is None:
            logging.error("Token missing 'sub' claim")
            raise credentials_exception
            
        # Check if db is provided for user lookup
        if db is None:
            logging.warning("Database session not provided, skipping user lookup")
            return {"id": int(user_id)}
            
        # Look up the user
        user = get_user_by_id(db, int(user_id))
        if user is None:
            logging.error(f"User with ID {user_id} not found in database")
            raise credentials_exception
            
        return user
    except Exception as e:
        logging.error(f"Error in enhanced_get_current_user: {str(e)}")
        raise credentials_exception

# Patch function to apply the enhanced functions
def apply_auth_fixes():
    # Import the modules to patch
    import backend.core.auth
    import backend.api.assessment_history
    
    # Apply the patches
    backend.core.auth.decode_access_token = enhanced_decode_access_token
    logging.info("✅ Enhanced token decoding function applied")
    
    # Only replace the get_current_user if it's being used directly
    # This could cause issues if there are dependencies, so use with caution
    # backend.core.auth.get_current_user = enhanced_get_current_user
    
    logging.info("✅ Authentication fixes applied")
    
    return True
"""
    
    try:
        with open(patch_file, "w") as f:
            f.write(content)
        logging.info(f"Created auth patch file at {patch_file}")
        return True
    except Exception as e:
        logging.error(f"Error creating auth patch file: {e}")
        return False

def main():
    """Main function to check and fix JWT token validation."""
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
    
    # Create auth patch file
    logging.info("\n=== Creating Auth Patch File ===")
    create_auth_patch_file()
    
    # Report summary
    logging.info("\n=== JWT Token Validation Check Summary ===")
    logging.info("1. JWT Secret Consistency: Checked")
    logging.info("2. Token Validation Code: Checked")
    logging.info("3. Assessment Auth Dependencies: Checked")
    logging.info("4. Auth Patch File: Created")
    
    logging.info("\nTo apply the fixes, import and run 'apply_auth_fixes()' from 'backend.fixes.auth_fixes'")
    
    return True

if __name__ == "__main__":
    main()

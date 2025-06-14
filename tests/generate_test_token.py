"""
Direct token generation script that bypasses the API to create a valid JWT token
for testing the assessment history endpoints.
"""

import os
import sys
import logging
import sqlite3
from datetime import datetime, timedelta
import json
import jwt
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Default JWT settings - these must match what's used in the backend
SECRET_KEY = "your-secret-key-for-jwt-which-should-be-kept-secret"  # Default testing key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def find_database():
    """Find the SQLite database file."""
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Possible database locations
    possible_paths = [
        os.path.join(project_root, "backend", "test.db"),
        os.path.join(project_root, "test.db"),
        os.path.join(project_root, "backend", "fixed_auth.db"),
        os.path.join(project_root, "backend", "auth_test.db"),
        os.path.join(project_root, "backend", "standalone_auth.db")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logging.info(f"Found database at: {path}")
            return path
    
    # If no database found, try to create one
    default_path = os.path.join(project_root, "test.db")
    logging.info(f"No existing database found. Will create one at: {default_path}")
    return default_path

def get_user_id(db_path):
    """Get the ID of the test user."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Query for test user
        cursor.execute("SELECT id FROM users WHERE email = ?", ("test@example.com",))
        user = cursor.fetchone()
        
        if user:
            user_id = user[0]
            logging.info(f"Found test user with ID: {user_id}")
            return user_id
        else:
            logging.error("Test user not found in database")
            return None
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def create_jwt_token(user_id):
    """Create a JWT token for the given user ID."""
    try:
        # First try to import the secret key from the backend
        try:
            from backend.core.config import JWT_SECRET_KEY
            secret_key = JWT_SECRET_KEY
            logging.info("Using JWT_SECRET_KEY from backend.core.config")
        except ImportError:
            # Fallback to default key
            secret_key = SECRET_KEY
            logging.info("Using default SECRET_KEY")
        
        # Set token expiration
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + expires_delta
        
        # Create token payload
        to_encode = {
            "sub": str(user_id),
            "exp": expire
        }
        
        # Create the JWT token
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logging.error(f"Error creating JWT token: {e}")
        return None

def main():
    """Main function to generate a JWT token for the test user."""
    logging.info("Starting direct token generation process...")
    
    # Find database file
    db_path = find_database()
    
    # Get user ID
    user_id = get_user_id(db_path)
    if not user_id:
        logging.error("Failed to find test user. Make sure to run create_test_user_direct.py first.")
        return False
    
    # Create JWT token
    token = create_jwt_token(user_id)
    if not token:
        logging.error("Failed to create JWT token.")
        return False
    
    # Output token information
    logging.info("Successfully generated JWT token:")
    logging.info(f"USER_ID: {user_id}")
    logging.info(f"TOKEN: {token}")
    
    # Save token to file for easy access in other scripts
    token_file = os.path.join(project_root, "test_token.txt")
    with open(token_file, "w") as f:
        f.write(token)
    logging.info(f"Token saved to: {token_file}")
    
    # Print token in format ready for use in authorization header
    print(f"Bearer {token}")
    return True

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)

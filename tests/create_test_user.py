"""
Create a test user in the database for API testing.
"""

import sys
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add the project root directory to the path so we can import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Now try importing our modules
try:
    from backend.models.user import User, UserRole
    from backend.core.config import get_db
    from backend.core.database import engine, Base
    from passlib.context import CryptContext
    
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
except ImportError as e:
    logging.error(f"Error importing modules: {str(e)}")
    logging.info("Trying direct database connection instead...")
    
    try:
        # Alternative approach with direct SQL connection
        import sqlite3
        from sqlite3 import Error
        from werkzeug.security import generate_password_hash
        
        def create_connection():
            """Create a database connection to the SQLite database"""
            conn = None
            try:
                db_path = os.path.join(project_root, "backend", "test.db")
                if not os.path.exists(db_path):
                    # Try different locations
                    db_path = os.path.join(project_root, "test.db")
                
                logging.info(f"Connecting to database at: {db_path}")
                conn = sqlite3.connect(db_path)
                return conn
            except Error as e:
                logging.error(f"Error connecting to database: {e}")
                return None
        
        # Create a direct connection to the database
        conn = create_connection()
        if conn is None:
            logging.error("Cannot create database connection")
            sys.exit(1)
            
        # Check if users table exists
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users';
        """)
        
        if cursor.fetchone() is None:
            logging.error("Users table does not exist in the database")
            sys.exit(1)
            
        # Create test user directly
        test_email = "test@example.com"
        test_username = "testuser"
        test_password = generate_password_hash("Password123!")
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (test_email,))
        user = cursor.fetchone()
        
        if user:
            user_id = user[0]
            logging.info(f"Test user {test_email} already exists with ID {user_id}")
            # Update password
            cursor.execute(
                "UPDATE users SET hashed_password = ? WHERE id = ?", 
                (test_password, user_id)
            )
            conn.commit()
            logging.info(f"Updated password for test user {test_email}")
            sys.exit(0)
        else:
            # Insert new user
            cursor.execute("""
                INSERT INTO users (email, username, hashed_password, is_active, is_verified, role, created_at, first_name, last_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                test_email, test_username, test_password, 1, 1, "PATIENT", 
                datetime.now().isoformat(), "Test", "User"
            ))
            conn.commit()
            user_id = cursor.lastrowid
            logging.info(f"Created new test user {test_email} with ID {user_id}")
            sys.exit(0)
            
    except Exception as e:
        logging.error(f"Alternative approach failed: {str(e)}")
        sys.exit(1)

def create_test_user():
    """Create a test user in the database."""
    db = next(get_db())
    
    # Check if user already exists
    test_email = "test@example.com"
    existing_user = db.query(User).filter(User.email == test_email).first()
    
    if existing_user:
        logging.info(f"Test user {test_email} already exists.")
        # Update password just to be sure
        existing_user.hashed_password = get_password_hash("Password123!")
        db.commit()
        logging.info(f"Updated password for test user {test_email}")
        return existing_user
    
    # Create new test user
    try:
        new_user = User(
            email=test_email,
            username="testuser",
            hashed_password=get_password_hash("Password123!"),
            is_active=True,
            is_verified=True,
            role=UserRole.PATIENT,
            created_at=datetime.now(),
            first_name="Test",
            last_name="User"
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logging.info(f"Created new test user {test_email} with ID {new_user.id}")
        return new_user
    
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating test user: {e}")
        return None

if __name__ == "__main__":
    logging.info("Creating test user for API verification...")
    user = create_test_user()
    
    if user:
        logging.info(f"Test user ready for verification: {user.email} (ID: {user.id})")
        logging.info("Username: testuser")
        logging.info("Password: Password123!")
        sys.exit(0)
    else:
        logging.error("Failed to create or update test user")
        sys.exit(1)

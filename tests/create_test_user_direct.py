"""
Direct database approach to create a test user for API verification.
This script uses direct SQL commands to create a test user without relying on ORM.
"""

import os
import sys
import logging
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add project root to Python path to ensure modules can be found
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

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

def create_connection(db_path):
    """Create a database connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        logging.info(f"Connected to database: {db_path}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None

def ensure_users_table(conn):
    """Make sure the users table exists."""
    try:
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone() is None:
            logging.info("Creating users table...")
            
            # Create users table
            cursor.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    hashed_password TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    is_active INTEGER DEFAULT 1,
                    is_verified INTEGER DEFAULT 0,
                    role TEXT DEFAULT 'PATIENT',
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            conn.commit()
            logging.info("Users table created successfully")
        else:
            logging.info("Users table already exists")
            
        return True
    except sqlite3.Error as e:
        logging.error(f"Error ensuring users table: {e}")
        return False

def create_test_user(conn):
    """Create a test user in the database."""
    try:
        cursor = conn.cursor()
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
            return True
        else:
            # Insert new user
            current_time = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO users (
                    email, username, hashed_password, first_name, last_name,
                    is_active, is_verified, role, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                test_email, test_username, test_password, "Test", "User",
                1, 1, "PATIENT", current_time, current_time
            ))
            conn.commit()
            user_id = cursor.lastrowid
            logging.info(f"Created new test user {test_email} with ID {user_id}")
            return True
    except sqlite3.Error as e:
        logging.error(f"Error creating test user: {e}")
        return False

def main():
    """Main function to create a test user."""
    logging.info("Starting test user creation process...")
    
    # Find database file
    db_path = find_database()
    
    # Create connection
    conn = create_connection(db_path)
    if not conn:
        logging.error("Failed to connect to database")
        return False
    
    # Ensure users table exists
    if not ensure_users_table(conn):
        logging.error("Failed to ensure users table exists")
        conn.close()
        return False
    
    # Create test user
    success = create_test_user(conn)
    conn.close()
    
    if success:
        logging.info("Test user creation process completed successfully")
        logging.info("Test User Credentials:")
        logging.info("Email: test@example.com")
        logging.info("Username: testuser")
        logging.info("Password: Password123!")
        return True
    else:
        logging.error("Test user creation process failed")
        return False

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit(1)

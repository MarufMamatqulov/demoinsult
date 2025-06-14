"""
Script to run the main server with the fixed authentication models.
This will start the main FastAPI application with the corrected models.
"""

import uvicorn
import os
import sys
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Create or update tables in the database
def initialize_database():
    from backend.core.config import engine, Base
    from backend.models.user import User, UserProfile, PHQ9Assessment, NIHSSAssessment
    
    # Create tables if they don't exist
    inspector = inspect(engine)
    if not inspector.has_table("users"):
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    else:
        print("Database tables already exist")

if __name__ == "__main__":
    print("Initializing database...")
    initialize_database()
    
    print("Starting server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

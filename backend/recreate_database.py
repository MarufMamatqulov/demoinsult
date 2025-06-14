"""
Script to recreate the database with the fixed models.
This will drop all tables and recreate them with the corrected models.
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_database():
    # Import database configuration
    from backend.core.config import engine, Base, SessionLocal
    
    # Import all models to ensure they're registered with Base
    from backend.models.user import User, UserProfile, PHQ9Assessment, NIHSSAssessment
    from backend.models.user import BloodPressureReading, SpeechHearingAssessment, MovementAssessment, Assessment
    
    try:
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Drop all tables
        logger.info("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully")
        
        # Create all tables
        logger.info("Creating all tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully")
        
        # Create a test user to verify the models work
        logger.info("Creating test user...")
        from backend.core.auth import get_password_hash
        from backend.models.user import User, UserRole, UserProfile
        
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("test1234"),
            first_name="Test",
            last_name="User",
            role=UserRole.PATIENT,
            is_verified=True,
            is_active=True
        )
        
        session.add(test_user)
        session.commit()
        
        # Create a profile for the test user
        test_profile = UserProfile(
            user_id=test_user.id,
            gender="Other"
        )
        
        session.add(test_profile)
        session.commit()
        
        # Verify the relationships work
        logger.info("Verifying relationships...")
        user_with_profile = session.query(User).filter(User.email == "test@example.com").first()
        
        if user_with_profile and user_with_profile.profile:
            logger.info(f"Test user created successfully with ID: {user_with_profile.id}")
            logger.info(f"Test profile created successfully with ID: {user_with_profile.profile.id}")
        else:
            logger.error("Failed to create test user with profile")
        
        session.close()
        logger.info("Database recreation completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error recreating database: {str(e)}")
        return False

if __name__ == "__main__":
    recreate_database()

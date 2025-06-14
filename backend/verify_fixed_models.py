"""
Script to verify the fixed SQLAlchemy models with fully qualified paths.
This will create the database tables and test basic CRUD operations to ensure
the relationships are working correctly.
"""

import os
import sys
import logging

# Add parent directory to path to ensure modules can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import necessary modules
from sqlalchemy.orm import sessionmaker
from backend.core.config import engine, Base
from backend.models.user import User, UserProfile, UserRole, PHQ9Assessment, NIHSSAssessment
from backend.core.auth import get_password_hash

def verify_models():
    """Verify the models by creating tables and testing relationships."""
    try:
        logger.info("Creating database tables...")
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully")
        
        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()
          # Create a test user
        logger.info("Creating test user...")
        
        # Check if test user already exists
        existing_user = session.query(User).filter(User.email == "test@example.com").first()
        
        if existing_user:
            logger.info(f"Test user already exists with ID: {existing_user.id}")
            test_user = existing_user
        else:
            test_user = User(
                email="test@example.com",
                username="testuser",
                hashed_password=get_password_hash("testpassword"),
                first_name="Test",
                last_name="User",
                is_active=True,
                is_verified=True,
                role=UserRole.PATIENT
            )
            
            session.add(test_user)
            session.commit()
            logger.info(f"Test user created with ID: {test_user.id}")
          # Create a profile for the test user
        logger.info("Creating user profile...")
        
        # Check if profile already exists
        existing_profile = session.query(UserProfile).filter(UserProfile.user_id == test_user.id).first()
        
        if existing_profile:
            logger.info(f"User profile already exists with ID: {existing_profile.id}")
            profile = existing_profile
        else:
            profile = UserProfile(
                user_id=test_user.id,
                gender="Other",
                date_of_birth=None,
                height=175,
                weight=70
            )
            
            session.add(profile)
            session.commit()
            logger.info(f"User profile created with ID: {profile.id}")
          # Create a PHQ9 assessment for the user
        logger.info("Creating PHQ9 assessment...")
        
        # Check if an assessment already exists
        existing_assessment = session.query(PHQ9Assessment).filter(PHQ9Assessment.user_id == test_user.id).first()
        
        if existing_assessment:
            logger.info(f"PHQ9 assessment already exists with ID: {existing_assessment.id}")
            assessment = existing_assessment
        else:
            assessment = PHQ9Assessment(
                user_id=test_user.id,
                score=5,
                answers="{'q1': 1, 'q2': 0, 'q3': 1, 'q4': 0, 'q5': 1, 'q6': 0, 'q7': 1, 'q8': 0, 'q9': 1}"
            )
            
            session.add(assessment)
            session.commit()
            logger.info(f"PHQ9 assessment created with ID: {assessment.id}")
        
        # Verify relationships
        logger.info("Verifying relationships...")
        
        # Fetch user with relationships
        user_with_relationships = session.query(User).filter(User.id == test_user.id).first()
        
        if user_with_relationships.profile:
            logger.info(f"User profile relationship verified: {user_with_relationships.profile.id}")
        else:
            logger.error("User profile relationship failed")
            
        if user_with_relationships.phq9_assessments:
            logger.info(f"PHQ9 assessments relationship verified: {len(user_with_relationships.phq9_assessments)} assessments found")
        else:
            logger.error("PHQ9 assessments relationship failed")
            
        # Verify reverse relationships
        profile_with_user = session.query(UserProfile).filter(UserProfile.id == profile.id).first()
        if profile_with_user.user:
            logger.info(f"Profile to user relationship verified: {profile_with_user.user.id}")
        else:
            logger.error("Profile to user relationship failed")
            
        assessment_with_user = session.query(PHQ9Assessment).filter(PHQ9Assessment.id == assessment.id).first()
        if assessment_with_user.user:
            logger.info(f"Assessment to user relationship verified: {assessment_with_user.user.id}")
        else:
            logger.error("Assessment to user relationship failed")
            
        # Clean up
        session.close()
        logger.info("Model verification completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error verifying models: {str(e)}")
        return False

if __name__ == "__main__":
    verify_models()

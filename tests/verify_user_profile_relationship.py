"""
Test script to verify that the user-profile relationship is working correctly.
"""

import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path so we can import from models
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.user import User, UserProfile

# Use the main database
DB_URL = "sqlite:///./test.db"  # Use the main app's database
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify_user_profile_relationship():
    """Verify that a user has a profile."""
    session = SessionLocal()
    
    try:
        # Get a user from the database
        user = session.query(User).filter(User.email.like('test_main_%')).first()
        
        if not user:
            logger.error("No test user found in the database")
            return False
        
        logger.info(f"Found user with ID: {user.id}, username: {user.username}")
        
        # Check if the user has a profile
        if user.profile:
            logger.info(f"User has a profile with ID: {user.profile.id}")
            return True
        else:
            # If not, it might be due to the registration function not creating a profile
            # Let's check if there's a profile with this user_id
            profile = session.query(UserProfile).filter(UserProfile.user_id == user.id).first()
            
            if profile:
                logger.info(f"Found profile with ID: {profile.id} for user ID: {user.id}")
                # This means the relationship is not working properly even though the profile exists
                logger.warning("Profile exists but user.profile is None - relationship not working")
                return False
            else:
                logger.info("No profile found for user - creating one now")
                # Create a profile for the user
                profile = UserProfile(user_id=user.id)
                session.add(profile)
                session.commit()
                
                # Refresh the user to check if the relationship works
                session.refresh(user)
                
                if user.profile:
                    logger.info(f"Created profile and verified relationship works. Profile ID: {user.profile.id}")
                    return True
                else:
                    logger.error("Created profile but user.profile is still None - relationship not working")
                    return False
    except Exception as e:
        logger.error(f"Error verifying user-profile relationship: {str(e)}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    result = verify_user_profile_relationship()
    
    if result:
        logger.info("✅ User-profile relationship verification passed!")
    else:
        logger.error("❌ User-profile relationship verification failed!")

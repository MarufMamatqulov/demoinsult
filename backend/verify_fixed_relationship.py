"""
Simplified test to verify the user-profile relationship.
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, backend_dir)

# Import after setting up the path
from backend.models.user import User, UserProfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection
DB_PATH = os.path.join(backend_dir, "test.db")
DB_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def main():
    session = SessionLocal()
    
    try:
        # Get our test user
        user = session.query(User).filter(User.email.like("test_main_%")).first()
        
        if not user:
            logger.error("No test user found!")
            return
            
        logger.info(f"Found user: {user.username} (ID: {user.id})")
        
        # Check profile relationship
        if user.profile:
            logger.info(f"User has profile with ID: {user.profile.id}")
            logger.info("✓ User-profile relationship works correctly!")
        else:
            logger.error("User doesn't have a profile or relationship is broken")
            
            # Check if profile exists but relationship is broken
            profile = session.query(UserProfile).filter(UserProfile.user_id == user.id).first()
            if profile:
                logger.error(f"Profile exists (ID: {profile.id}) but relationship is broken")
            else:
                logger.info("Creating profile...")
                profile = UserProfile(user_id=user.id)
                session.add(profile)
                session.commit()
                session.refresh(user)
                
                if user.profile:
                    logger.info(f"Created profile (ID: {user.profile.id})")
                    logger.info("✓ User-profile relationship works correctly!")
                else:
                    logger.error("Created profile but relationship still broken")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        session.close()
        
if __name__ == "__main__":
    main()

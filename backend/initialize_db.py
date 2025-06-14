import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import models
from backend.models.user import Base, User, UserRole
from backend.core.auth import get_password_hash

def init_db():
    # Get database URL from environment or use default
    database_url = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    logger.info(f"Initializing database with URL: {database_url}")
    
    # Create engine
    engine = create_engine(database_url)
    
    # Create database if it doesn't exist
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info(f"Created database at {database_url}")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Created all tables")
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin_exists = db.query(User).filter(User.role == UserRole.ADMIN).first()
        
        if not admin_exists:
            # Create admin user
            admin_password = os.getenv("ADMIN_PASSWORD", "admin123456")
            admin_email = os.getenv("ADMIN_EMAIL", "admin@insultmedai.com")
            
            admin_user = User(
                username="admin",
                email=admin_email,
                hashed_password=get_password_hash(admin_password),
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True,
                first_name="Admin",
                last_name="User"
            )
            
            db.add(admin_user)
            db.commit()
            logger.info(f"Created admin user with email: {admin_email}")
        else:
            logger.info("Admin user already exists")
            
        # Create test doctor user if needed
        doctor_exists = db.query(User).filter(
            User.role == UserRole.DOCTOR, 
            User.username == "doctor"
        ).first()
        
        if not doctor_exists:
            doctor_user = User(
                username="doctor",
                email="doctor@insultmedai.com",
                hashed_password=get_password_hash("doctor123456"),
                role=UserRole.DOCTOR,
                is_active=True,
                is_verified=True,
                first_name="Doctor",
                last_name="Test"
            )
            
            db.add(doctor_user)
            db.commit()
            logger.info("Created test doctor user")
        else:
            logger.info("Test doctor user already exists")
            
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
    
    logger.info("Database initialization completed successfully")

if __name__ == "__main__":
    init_db()

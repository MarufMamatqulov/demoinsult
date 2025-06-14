from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, Table, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

# Create a standalone database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./fixed_auth.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define model classes with better relationship handling
class UserRole(enum.Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    CAREGIVER = "caregiver"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True, index=True)
    verification_token_expires = Column(DateTime(timezone=True), nullable=True)
    password_reset_token = Column(String, nullable=True, index=True)
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.PATIENT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    google_id = Column(String, unique=True, nullable=True)
    
    # Relationship definitions will be added later to avoid circular references

class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String, nullable=True)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    medical_history = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Define relationship later

class PHQ9Assessment(Base):
    __tablename__ = "phq9_assessments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    answers = Column(Text, nullable=True)
    
    # Define relationship later

class NIHSSAssessment(Base):
    __tablename__ = "nihss_assessments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    answers = Column(Text, nullable=True)
    
    # Define relationship later

class BloodPressureReading(Base):
    __tablename__ = "blood_pressure_readings"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    systolic = Column(Integer, nullable=False)
    diastolic = Column(Integer, nullable=False)
    pulse = Column(Integer, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)
    
    # Define relationship later

class SpeechHearingAssessment(Base):
    __tablename__ = "speech_hearing_assessments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    audio_file = Column(String, nullable=True)
    transcription = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)
    
    # Define relationship later

class MovementAssessment(Base):
    __tablename__ = "movement_assessments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    video_file = Column(String, nullable=True)
    exercise_type = Column(String, nullable=True)
    analysis = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)
    
    # Define relationship later

class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String, nullable=False, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Define relationship later

# Now add the relationships
UserProfile.user = relationship("User", back_populates="profile")
PHQ9Assessment.user = relationship("User", back_populates="phq9_assessments")
NIHSSAssessment.user = relationship("User", back_populates="nihss_assessments")
BloodPressureReading.user = relationship("User", back_populates="blood_pressure_readings")
SpeechHearingAssessment.user = relationship("User", back_populates="speech_hearing_assessments")
MovementAssessment.user = relationship("User", back_populates="movement_assessments")
Assessment.user = relationship("User", back_populates="assessments")

# Add backref relationships to User
User.profile = relationship("UserProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")
User.phq9_assessments = relationship("PHQ9Assessment", back_populates="user", cascade="all, delete-orphan")
User.nihss_assessments = relationship("NIHSSAssessment", back_populates="user", cascade="all, delete-orphan")
User.blood_pressure_readings = relationship("BloodPressureReading", back_populates="user", cascade="all, delete-orphan")
User.speech_hearing_assessments = relationship("SpeechHearingAssessment", back_populates="user", cascade="all, delete-orphan")
User.movement_assessments = relationship("MovementAssessment", back_populates="user", cascade="all, delete-orphan")
User.assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")

# Create a FastAPI app to test the models
app = FastAPI(title="Fixed Auth Models Test")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/init-db")
def initialize_database():
    Base.metadata.create_all(bind=engine)
    return {"message": "Database initialized successfully"}

@app.get("/test-query")
def test_query(db: Session = Depends(get_db)):
    # Try to create a sample user
    try:
        # Check if test user exists
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if not test_user:
            # Create test user
            test_user = User(
                email="test@example.com",
                username="testuser",
                hashed_password="hashed_password",
                first_name="Test",
                last_name="User",
                role=UserRole.PATIENT,
                is_active=True,
                is_verified=True
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            
            # Create a profile for the user
            profile = UserProfile(
                user_id=test_user.id,
                gender="Other"
            )
            db.add(profile)
            db.commit()
            
        return {
            "status": "success",
            "message": "Database query successful",
            "user": {
                "id": test_user.id,
                "email": test_user.email,
                "username": test_user.username,
                "profile": {
                    "id": test_user.profile.id if test_user.profile else None,
                    "gender": test_user.profile.gender if test_user.profile else None
                } if test_user.profile else None
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database query failed: {str(e)}"
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)

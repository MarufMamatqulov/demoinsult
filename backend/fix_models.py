from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, Table, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.config import Base, engine
import enum

# Create tables
def initialize_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

# Fix models with fully qualified paths
class UserRole(enum.Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    CAREGIVER = "caregiver"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  # Add this line to avoid table already exists error

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True, index=True)  # Email verification token
    verification_token_expires = Column(DateTime(timezone=True), nullable=True)
    password_reset_token = Column(String, nullable=True, index=True)  # Password reset token
    password_reset_expires = Column(DateTime(timezone=True), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.PATIENT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    google_id = Column(String, unique=True, nullable=True)  # For Google OAuth
    
    # Relationships with patient data using fully qualified paths
    phq9_assessments = relationship("models.user.PHQ9Assessment", back_populates="user", cascade="all, delete-orphan")
    nihss_assessments = relationship("models.user.NIHSSAssessment", back_populates="user", cascade="all, delete-orphan")
    blood_pressure_readings = relationship("models.user.BloodPressureReading", back_populates="user", cascade="all, delete-orphan")
    speech_hearing_assessments = relationship("models.user.SpeechHearingAssessment", back_populates="user", cascade="all, delete-orphan")
    movement_assessments = relationship("models.user.MovementAssessment", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("models.user.UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    assessments = relationship("models.user.Assessment", back_populates="user", cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String, nullable=True)
    height = Column(Integer, nullable=True)  # in cm
    weight = Column(Integer, nullable=True)  # in kg
    medical_history = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    doctor_name = Column(String, nullable=True)
    doctor_phone = Column(String, nullable=True)
    stroke_date = Column(DateTime, nullable=True)
    stroke_type = Column(String, nullable=True)
    affected_side = Column(String, nullable=True)
    mobility_aid = Column(String, nullable=True)
    therapy_goals = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with user
    user = relationship("models.user.User", back_populates="profile")

# Models for assessments
class PHQ9Assessment(Base):
    __tablename__ = "phq9_assessments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    answers = Column(Text, nullable=True)  # JSON string of answers
    
    # Relationship with user
    user = relationship("models.user.User", back_populates="phq9_assessments")

class NIHSSAssessment(Base):
    __tablename__ = "nihss_assessments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    answers = Column(Text, nullable=True)  # JSON string of answers
    
    # Relationship with user
    user = relationship("models.user.User", back_populates="nihss_assessments")

class BloodPressureReading(Base):
    __tablename__ = "blood_pressure_readings"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    systolic = Column(Integer, nullable=False)
    diastolic = Column(Integer, nullable=False)
    pulse = Column(Integer, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)
    
    # Relationship with user
    user = relationship("models.user.User", back_populates="blood_pressure_readings")

class SpeechHearingAssessment(Base):
    __tablename__ = "speech_hearing_assessments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    audio_file = Column(String, nullable=True)
    transcription = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)  # JSON string of analysis
    score = Column(Integer, nullable=True)
    
    # Relationship with user
    user = relationship("models.user.User", back_populates="speech_hearing_assessments")

class MovementAssessment(Base):
    __tablename__ = "movement_assessments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    video_file = Column(String, nullable=True)
    exercise_type = Column(String, nullable=True)
    analysis = Column(Text, nullable=True)  # JSON string of analysis
    score = Column(Integer, nullable=True)
    
    # Relationship with user
    user = relationship("models.user.User", back_populates="movement_assessments")

class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    assessment_type = Column(String, nullable=False)
    assessment_id = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    score = Column(Integer, nullable=True)
    
    # Relationship with user
    user = relationship("models.user.User", back_populates="assessments")

if __name__ == "__main__":
    initialize_db()
    print("Models updated with fully qualified paths.")

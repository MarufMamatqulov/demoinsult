from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, Table, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.config import Base
import enum
import sys
import os

# Ensure module can be found in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    
    # Relationships will be defined at the end of the file to avoid circular references

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
    
    # Relationship will be defined later

# Models for assessments
class PHQ9Assessment(Base):
    __tablename__ = "phq9_assessments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    answers = Column(Text, nullable=True)  # JSON string of answers
    
    # Relationship will be defined later

class NIHSSAssessment(Base):
    __tablename__ = "nihss_assessments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    answers = Column(Text, nullable=True)  # JSON string of answers
    
    # Relationship will be defined later

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
    
    # Relationship will be defined later

class SpeechHearingAssessment(Base):
    __tablename__ = "speech_hearing_assessments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    speech_score = Column(Integer, nullable=True)
    hearing_score = Column(Integer, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)
    
    # Relationship will be defined later

class MovementAssessment(Base):
    __tablename__ = "movement_assessments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    upper_limb_score = Column(Integer, nullable=True)
    lower_limb_score = Column(Integer, nullable=True)
    balance_score = Column(Integer, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)
    
    # Relationship will be defined later

class Assessment(Base):
    __tablename__ = "assessments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String, nullable=False, index=True)  # blood_pressure, phq9, nihss, etc.
    data = Column(JSON, nullable=False)  # Store assessment data as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship will be defined later

# Define all relationships after all classes have been defined to avoid circular imports

# First add the relationships for the child tables using lambda to avoid circular imports
UserProfile.user = relationship(lambda: User, back_populates="profile")
PHQ9Assessment.user = relationship(lambda: User, back_populates="phq9_assessments")
NIHSSAssessment.user = relationship(lambda: User, back_populates="nihss_assessments")
BloodPressureReading.user = relationship(lambda: User, back_populates="blood_pressure_readings")
SpeechHearingAssessment.user = relationship(lambda: User, back_populates="speech_hearing_assessments")
MovementAssessment.user = relationship(lambda: User, back_populates="movement_assessments")
Assessment.user = relationship(lambda: User, back_populates="assessments")

# Then add all the backref relationships to User class using lambda to avoid circular imports
User.profile = relationship(lambda: UserProfile, back_populates="user", uselist=False, cascade="all, delete-orphan")
User.phq9_assessments = relationship(lambda: PHQ9Assessment, back_populates="user", cascade="all, delete-orphan")
User.nihss_assessments = relationship(lambda: NIHSSAssessment, back_populates="user", cascade="all, delete-orphan")
User.blood_pressure_readings = relationship(lambda: BloodPressureReading, back_populates="user", cascade="all, delete-orphan")
User.speech_hearing_assessments = relationship(lambda: SpeechHearingAssessment, back_populates="user", cascade="all, delete-orphan")
User.movement_assessments = relationship(lambda: MovementAssessment, back_populates="user", cascade="all, delete-orphan")
User.assessments = relationship(lambda: Assessment, back_populates="user", cascade="all, delete-orphan")

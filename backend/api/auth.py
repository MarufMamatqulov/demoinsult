from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, List
from google.oauth2 import id_token
from google.auth.transport import requests
from jose import jwt

import os
import logging
import json
from datetime import datetime, timedelta

# Fixed import paths
from backend.core.config import get_db
from backend.core.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    decode_access_token,
    create_verification_token,
    create_password_reset_token
)
from backend.models.user import User, UserProfile, UserRole
from backend.schemas.auth import (
    Token, 
    UserCreate, 
    UserLogin, 
    UserOut, 
    UserGoogleLogin,
    UserProfileCreate,
    UserProfileOut,    UserProfileUpdate,
    UserUpdateMe,
    VerifyEmail,
    RequestPasswordReset,
    ResetPassword
)
from backend.utils.email_utils import send_verification_email, send_password_reset_email

# Google OAuth2 client ID
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

router = APIRouter()

# OAuth2 password bearer for token-based auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Helper functions
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_google_id(db: Session, google_id: str) -> Optional[User]:
    return db.query(User).filter(User.google_id == google_id).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def create_user_profile(db: Session, user_id: int) -> UserProfile:
    """Create an empty user profile."""
    profile = UserProfile(user_id=user_id)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

# Auth endpoints
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Register a new user with email and password."""
    # Check if email already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Check if username already exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
        
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=UserRole.PATIENT,  # Default role is patient
        is_verified=False       # User needs to verify email
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create empty profile for the user
    create_user_profile(db, new_user.id)
    
    # Generate verification token
    verification_token = create_verification_token(new_user.id)
    expiry = datetime.utcnow() + timedelta(hours=24)
    
    # Save token in the database
    new_user.verification_token = verification_token
    new_user.verification_token_expires = expiry
    db.commit()
    
    # Send verification email in the background
    background_tasks.add_task(
        send_verification_email,
        to_email=new_user.email,
        token=verification_token
    )
    
    return new_user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login with username/email and password."""
    # Try to authenticate with email
    user = authenticate_user(db, form_data.username, form_data.password)
    # If not found, try with username
    if not user:
        # Check if the username field is actually a username, not an email
        potential_user = get_user_by_username(db, form_data.username)
        if potential_user:
            # Verify password
            if verify_password(form_data.password, potential_user.hashed_password):
                user = potential_user
                
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login/google", response_model=Token)
async def login_with_google(
    google_data: UserGoogleLogin,
    db: Session = Depends(get_db)
):
    """Login or register with Google OAuth."""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google authentication is not configured"
        )
        
    try:
        # Verify the Google token
        idinfo = id_token.verify_oauth2_token(
            google_data.token, requests.Request(), GOOGLE_CLIENT_ID
        )
        
        # Get user info from token
        google_id = idinfo["sub"]
        email = idinfo["email"]
        email_verified = idinfo.get("email_verified", False)
        name = idinfo.get("name", "")
        picture = idinfo.get("picture", "")
        
        # Try to find user by Google ID
        user = get_user_by_google_id(db, google_id)
        
        # If not found, try by email
        if not user and email:
            user = get_user_by_email(db, email)
            
            # If found by email but Google ID not set, update it
            if user:
                user.google_id = google_id
                user.is_verified = email_verified
                db.commit()
                
        # If still not found, create new user
        if not user:
            # Create username from email
            username_base = email.split("@")[0]
            username = username_base
            counter = 1
            
            # Make sure username is unique
            while get_user_by_username(db, username):
                username = f"{username_base}{counter}"
                counter += 1
                
            # Split name into first and last name
            name_parts = name.split(" ", 1)
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            last_name = name_parts[1] if len(name_parts) > 1 else ""
            
            # Create new user
            user = User(
                email=email,
                username=username,
                google_id=google_id,
                first_name=first_name,
                last_name=last_name,
                profile_picture=picture,
                is_verified=email_verified,
                role=UserRole.PATIENT  # Default role
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Create empty profile
            create_user_profile(db, user.id)
            
        # Generate token
        access_token = create_access_token(user.id)
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        logging.error(f"Google login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to authenticate with Google: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get information about the current logged in user."""
    return current_user

@router.put("/me", response_model=UserOut)
def update_user_me(
    user_data: UserUpdateMe,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's information."""
    # Check if trying to update email and if it's already taken
    if user_data.email and user_data.email != current_user.email:
        if get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = user_data.email
        
    # Update password if provided
    if user_data.new_password:
        if not user_data.current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is required to set a new password"
            )
            
        if not verify_password(user_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
            
        current_user.hashed_password = get_password_hash(user_data.new_password)
        
    # Update other fields
    if user_data.first_name is not None:
        current_user.first_name = user_data.first_name
        
    if user_data.last_name is not None:
        current_user.last_name = user_data.last_name
        
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me/profile", response_model=UserProfileOut)
def read_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user profile information."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        # Create profile if it doesn't exist
        profile = create_user_profile(db, current_user.id)
        
    return profile

@router.put("/me/profile", response_model=UserProfileOut)
def update_user_profile(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile information."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        # Create profile if it doesn't exist
        profile = create_user_profile(db, current_user.id)
        
    # Update profile fields from request data
    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)
        
    # Set updated timestamp
    profile.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(profile)
    return profile

@router.post("/verify-email", response_model=UserOut)
def verify_email(
    verification_data: VerifyEmail,
    db: Session = Depends(get_db)
):
    """Verify user email with token."""
    try:
        # Decode token to get user ID
        payload = decode_access_token(verification_data.token)
        user_id = int(payload["sub"])
        token_type = payload.get("type")
        
        if token_type != "email_verification":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )
            
        # Get user
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        if user.is_verified:
            return user  # Already verified
            
        # Verify user
        user.is_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        db.commit()
        db.refresh(user)
        
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error verifying email: {str(e)}"
        )

@router.post("/resend-verification")
def resend_verification(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Resend verification email."""
    user = get_user_by_email(db, email)
    if not user:
        # Don't reveal that email doesn't exist for security
        return {"message": "If the email exists, a verification link has been sent"}
        
    if user.is_verified:
        return {"message": "Email is already verified"}
        
    # Generate new verification token
    verification_token = create_verification_token(user.id)
    expiry = datetime.utcnow() + timedelta(hours=24)
    
    # Update token in database
    user.verification_token = verification_token
    user.verification_token_expires = expiry
    db.commit()
    
    # Send verification email in background
    background_tasks.add_task(
        send_verification_email,
        to_email=user.email,
        token=verification_token
    )
    
    return {"message": "Verification email has been sent"}

@router.post("/request-password-reset")
def request_password_reset(
    request_data: RequestPasswordReset,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Request password reset email."""
    user = get_user_by_email(db, request_data.email)
    if not user:
        # Don't reveal that email doesn't exist for security
        return {"message": "If the email exists, a password reset link has been sent"}
        
    # Generate password reset token
    reset_token = create_password_reset_token(user.id)
    expiry = datetime.utcnow() + timedelta(hours=1)
    
    # Update token in database
    user.password_reset_token = reset_token
    user.password_reset_expires = expiry
    db.commit()
    
    # Send password reset email in background
    background_tasks.add_task(
        send_password_reset_email,
        to_email=user.email,
        token=reset_token
    )
    
    return {"message": "Password reset email has been sent"}

@router.post("/reset-password")
def reset_password(
    reset_data: ResetPassword,
    db: Session = Depends(get_db)
):
    """Reset password with token."""
    try:
        # Decode token to get user ID
        payload = decode_access_token(reset_data.token)
        user_id = int(payload["sub"])
        token_type = payload.get("type")
        
        if token_type != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type"
            )
            
        # Get user
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        # Check if token matches stored token
        if user.password_reset_token != reset_data.token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token"
            )
            
        # Check if token is expired in database
        now = datetime.utcnow()
        if user.password_reset_expires and user.password_reset_expires < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password reset token has expired"
            )
            
        # Update password
        user.hashed_password = get_password_hash(reset_data.new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        db.commit()
        
        return {"message": "Password has been reset successfully"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password reset token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error resetting password: {str(e)}"
        )

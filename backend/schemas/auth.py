from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    user_id: Optional[int] = None
    
class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: Optional[bool] = True
    
class UserCreate(UserBase):
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class VerifyEmail(BaseModel):
    token: str
    
class RequestPasswordReset(BaseModel):
    email: EmailStr
    
class ResetPassword(BaseModel):
    token: str
    new_password: str
    
    @validator('new_password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserGoogleLogin(BaseModel):
    token: str  # Google ID token
    
class UserOut(UserBase):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_picture: Optional[str] = None
    is_verified: bool
    role: str
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class UserProfileBase(BaseModel):
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    doctor_name: Optional[str] = None
    doctor_phone: Optional[str] = None
    stroke_date: Optional[datetime] = None
    stroke_type: Optional[str] = None
    affected_side: Optional[str] = None
    mobility_aid: Optional[str] = None
    therapy_goals: Optional[str] = None
    
class UserProfileCreate(UserProfileBase):
    pass
    
class UserProfileUpdate(UserProfileBase):
    pass
    
class UserProfileOut(UserProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        
class UserUpdateMe(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    
    @validator('new_password')
    def password_strength(cls, v, values):
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if v is not None and 'current_password' not in values:
            raise ValueError('Current password is required to set a new password')
        return v

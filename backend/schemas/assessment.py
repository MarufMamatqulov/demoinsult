"""Assessment schemas for serialization and validation."""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class AssessmentBase(BaseModel):
    """Base schema for assessment data."""
    type: str = Field(..., description="Type of assessment (e.g., blood_pressure, phq9, nihss)")
    data: Dict[str, Any] = Field(..., description="Assessment data as JSON")

class AssessmentCreate(AssessmentBase):
    """Schema for creating a new assessment."""
    pass

class AssessmentOut(AssessmentBase):
    """Schema for assessment output with additional fields."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        """Pydantic config."""
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "type": "blood_pressure",
                "data": {
                    "systolic": 120,
                    "diastolic": 80,
                    "classification": "Normal"
                },
                "created_at": "2023-05-01T10:30:00Z",
                "updated_at": "2023-05-01T10:30:00Z"
            }
        }

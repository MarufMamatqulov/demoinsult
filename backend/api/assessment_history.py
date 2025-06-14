"""Assessment history API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
import logging

from backend.core.auth import get_current_user
from backend.core.config import get_db
from backend.models.user import User, Assessment
from backend.schemas.assessment import AssessmentOut, AssessmentCreate

router = APIRouter()

def convert_assessment_to_dict(assessment: Assessment) -> Dict[str, Any]:
    """
    Safely convert an Assessment ORM object to a dictionary.
    Handles JSON serialization issues with the data field.
    """
    try:
        # Handle the data field which might be causing issues
        data = assessment.data
        if data is None:
            data = {}
        elif isinstance(data, str):
            # If data is a string (maybe JSON string), try to parse it
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                # If parsing fails, keep it as is but as an empty dict to avoid errors
                logging.warning(f"Failed to parse JSON data for assessment {assessment.id}")
                data = {}
        elif isinstance(data, list):
            # If data is a list (which causes the 'list' object has no attribute 'get' error)
            # Convert it to a dictionary with a 'items' key
            logging.warning(f"Assessment {assessment.id} data is a list, converting to dict")
            data = {"items": data}
        
        # Format datetime objects to ISO format strings
        created_at = assessment.created_at.isoformat() if assessment.created_at else None
        updated_at = assessment.updated_at.isoformat() if assessment.updated_at else None
        
        # Create a dictionary with all the fields we need
        return {
            "id": assessment.id,
            "user_id": assessment.user_id,
            "type": assessment.type,
            "data": data,
            "created_at": created_at,
            "updated_at": updated_at
        }
    except Exception as e:
        logging.error(f"Error converting assessment to dict: {str(e)}")
        # Return a minimal valid dict to prevent errors        created_at = assessment.created_at.isoformat() if hasattr(assessment, 'created_at') and assessment.created_at else None
        updated_at = assessment.updated_at.isoformat() if hasattr(assessment, 'updated_at') and assessment.updated_at else None
        
        return {
            "id": getattr(assessment, 'id', 0),
            "user_id": getattr(assessment, 'user_id', 0),
            "type": getattr(assessment, 'type', "unknown"),
            "data": {},
            "created_at": created_at,
            "updated_at": updated_at
        }

@router.get("/history")
async def get_user_assessments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = None
):
    """Get all assessment records for the current user."""
    try:
        query = db.query(Assessment).filter(Assessment.user_id == current_user.id).order_by(Assessment.created_at.desc())
        
        if limit:
            query = query.limit(limit)
            
        assessments = query.all()
        
        # Convert each assessment to a dict
        result = []
        for assessment in assessments:
            try:
                assessment_dict = convert_assessment_to_dict(assessment)
                result.append(assessment_dict)
            except Exception as e:
                logging.error(f"Error converting assessment {assessment.id}: {str(e)}")
                # Include a minimal representation to avoid breaking the whole response
                result.append({
                    "id": getattr(assessment, 'id', 0),
                    "type": getattr(assessment, 'type', "unknown"),
                    "error": f"Failed to convert: {str(e)}"
                })
        
        # Log what we're returning for debugging
        logging.info(f"Returning {len(result)} assessment history items")
          # Use JSONResponse directly instead of relying on FastAPI's automatic serialization
        return JSONResponse(
            content=result,
            headers={"Content-Type": "application/json", "X-Content-Type-Options": "nosniff"}
        )
    except Exception as e:
        logging.error(f"Error processing assessment history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing assessment history: {str(e)}"
        )

@router.get("/{assessment_id}")
async def get_assessment_by_id(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific assessment record by ID."""
    try:
        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id,
            Assessment.user_id == current_user.id
        ).first()
        
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
        
        # Convert assessment to a dict with better error handling
        try:
            result = convert_assessment_to_dict(assessment)
        except Exception as e:
            logging.error(f"Error converting assessment {assessment_id} to dict: {str(e)}")
            # Provide a minimal valid response if conversion fails
            result = {
                "id": assessment.id,
                "type": assessment.type,
                "error": f"Could not properly format assessment data: {str(e)}"
            }
          # Use JSONResponse with explicit headers
        return JSONResponse(
            content=result,
            headers={"Content-Type": "application/json", "X-Content-Type-Options": "nosniff"}
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logging.error(f"Error retrieving assessment {assessment_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving assessment: {str(e)}"
        )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_assessment(
    assessment: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new assessment record."""
    try:
        # Ensure data is properly formatted
        assessment_data = assessment.data
        if isinstance(assessment_data, str):
            try:
                assessment_data = json.loads(assessment_data)
            except json.JSONDecodeError:
                logging.warning("Failed to parse JSON data in create_assessment")
                assessment_data = {}
        elif isinstance(assessment_data, list):
            # Handle list data by converting to a dictionary
            logging.warning("Assessment data is a list, converting to dict")
            assessment_data = {"items": assessment_data}
        
        # Create the assessment
        db_assessment = Assessment(
            user_id=current_user.id,
            type=assessment.type,
            data=assessment_data
        )
        
        db.add(db_assessment)
        db.commit()
        db.refresh(db_assessment)
        
        # Convert to dict for response
        try:
            result = convert_assessment_to_dict(db_assessment)
        except Exception as e:
            logging.error(f"Error converting new assessment to dict: {str(e)}")
            # Provide a minimal valid response
            result = {
                "id": db_assessment.id,
                "type": db_assessment.type,
                "message": "Assessment created successfully but could not format complete response"
            }
          # Return as JSONResponse with explicit headers
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=result,
            headers={"Content-Type": "application/json", "X-Content-Type-Options": "nosniff"}
        )
    except Exception as e:
        db.rollback()
        logging.error(f"Error creating assessment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating assessment: {str(e)}"
        )

@router.delete("/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a specific assessment record."""
    try:
        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id,
            Assessment.user_id == current_user.id
        ).first()
        
        if not assessment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assessment not found"
            )
        
        db.delete(assessment)
        db.commit()
        
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        logging.error(f"Error deleting assessment {assessment_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting assessment: {str(e)}"
        )

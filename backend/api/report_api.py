from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.utils.pdf_report import generate_patient_report
from backend.core.config import get_db
from backend.models.user import User, UserRole
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # Mock implementation for user retrieval
    user = db.query(User).filter(User.username == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

@router.get("/report/pdf/{patient_id}")
def get_patient_report(patient_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.DOCTOR:
        raise HTTPException(status_code=403, detail="Access forbidden: Only doctors can generate reports.")

    try:
        # Generate the PDF report
        pdf_path = generate_patient_report(db, patient_id)

        # Return the PDF as a downloadable response
        return FileResponse(pdf_path, media_type="application/pdf", filename=f"{patient_id}_report.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

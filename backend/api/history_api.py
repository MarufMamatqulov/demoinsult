from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.crud import (
    get_blood_pressure_history,
    get_nihss_history,
    get_barthel_index_history
)
from backend.core.config import get_db
from typing import Optional

router = APIRouter()

@router.get("/history/blood-pressure/{patient_id}")
def get_blood_pressure(patient_id: str, days: Optional[int] = 30, db: Session = Depends(get_db)):
    try:
        history = get_blood_pressure_history(db, patient_id, days)
        return sorted(history, key=lambda x: x.measurement_time, reverse=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/nihss/{patient_id}")
def get_nihss(patient_id: str, days: Optional[int] = 30, db: Session = Depends(get_db)):
    try:
        history = get_nihss_history(db, patient_id, days)
        return sorted(history, key=lambda x: x.measurement_time, reverse=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/barthel/{patient_id}")
def get_barthel(patient_id: str, days: Optional[int] = 30, db: Session = Depends(get_db)):
    try:
        history = get_barthel_index_history(db, patient_id, days)
        return sorted(history, key=lambda x: x.measurement_time, reverse=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

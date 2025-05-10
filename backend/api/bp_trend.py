from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ml_models.trend_analyzer import detect_bp_trend

router = APIRouter()

class BPMeasurement(BaseModel):
    systolic: float
    diastolic: float

class BPTrendRequest(BaseModel):
    measurements: List[BPMeasurement]

@router.post("/bp/trend")
async def analyze_bp_trend(request: BPTrendRequest):
    try:
        daily_measurements = [m.dict() for m in request.measurements]
        result = detect_bp_trend(daily_measurements)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

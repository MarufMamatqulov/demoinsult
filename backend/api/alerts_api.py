from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ml_models.trend_analyzer import detect_bp_trend
from ml_models.phq_trend_alert import detect_phq_trend

router = APIRouter()

class BPMeasurement(BaseModel):
    systolic: float
    diastolic: float

class PHQTrendInput(BaseModel):
    scores: List[int]

@router.post("/alerts/analyze-bp")
async def analyze_bp_trend(measurements: List[BPMeasurement]):
    try:
        # Convert Pydantic models to list of dictionaries
        daily_measurements = [measurement.dict() for measurement in measurements]

        # Analyze blood pressure trend
        result = detect_bp_trend(daily_measurements)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/alerts/phq-trend")
async def analyze_phq_trend(input_data: PHQTrendInput):
    try:
        # Analyze PHQ trend
        trend_status = detect_phq_trend(input_data.scores)
        return {"trend_status": trend_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

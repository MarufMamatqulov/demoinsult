from fastapi import APIRouter
from pydantic import BaseModel
from ml_models.blood_pressure_analysis import analyze_blood_pressure

router = APIRouter()

class BloodPressureRequest(BaseModel):
    systolic: int
    diastolic: int
    correct_position: bool

class BloodPressureResponse(BaseModel):
    category: str
    message: str

@router.post("/bp/analyze", response_model=BloodPressureResponse)
def analyze_bp(data: BloodPressureRequest):
    category = analyze_blood_pressure(data.systolic, data.diastolic, data.correct_position)
    if category == "Invalid reading: Position incorrect":
        return BloodPressureResponse(category=category, message="Please ensure correct position during measurement.")
    elif category == "Hypertension Stage 2":
        return BloodPressureResponse(category=category, message="Consult a healthcare provider immediately.")
    elif category == "Hypertension Stage 1":
        return BloodPressureResponse(category=category, message="Monitor your blood pressure regularly and consult a doctor.")
    elif category == "Elevated":
        return BloodPressureResponse(category=category, message="Adopt a healthy lifestyle to prevent hypertension.")
    else:
        return BloodPressureResponse(category=category, message="Your blood pressure is normal. Maintain a healthy lifestyle.")

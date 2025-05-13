from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ml_models.phq_model import predict_phq_level, analyze_phq9
from schemas.phq9 import PHQ9Request, PHQ9Response
router = APIRouter()

# Load the PHQ-9 model
import os

phq9_model_path = os.path.join(os.path.dirname(__file__), "../../ml_models/phq_model.pkl")
phq9_model = joblib.load(os.path.abspath(phq9_model_path))

class PHQ9Request(BaseModel):
    phq1: int
    phq2: int
    phq3: int
    phq4: int
    phq5: int
    phq6: int
    phq7: int
    phq8: int
    phq9: int

class PHQInput(BaseModel):
    q1: int
    q2: int
    q3: int
    q4: int
    q5: int
    q6: int
    q7: int
    q8: int
    q9: int

@router.post("/phq9/predict")
def predict_phq9(data: PHQ9Request):
    features = np.array([[
        data.phq1, data.phq2, data.phq3, data.phq4, data.phq5,
        data.phq6, data.phq7, data.phq8, data.phq9
    ]])
    prediction = phq9_model.predict(features)
    return {"prediction": prediction[0]}

@router.post("/phq/analyze", response_model=PHQ9Response)
def analyze_phq(data: PHQ9Request):
    prediction = predict_phq_level(data.dict())
    return PHQ9Response(prediction=prediction)

@router.post("/phq/analyze")
async def analyze_phq(input_data: PHQInput):
    try:
        # Convert input data to dictionary
        answers = input_data.dict()

        # Analyze PHQ-9 answers
        depression_level = analyze_phq9(answers)
        total_score = sum(answers.values())

        return {"depression_level": depression_level, "total_score": total_score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os
import logging

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
try:
    from ml_models.nihss_model import predict_nihss_severity
except ImportError:
    logging.warning("Could not import nihss_model, using direct severity calculation")

router = APIRouter()

class NIHSSInput(BaseModel):
    nihs_1: int
    nihs_2: int
    nihs_3: int
    nihs_4: int
    nihs_5: int
    nihs_6: int
    nihs_7: int
    nihs_8: int
    nihs_9: int
    nihs_10: int
    nihs_11: int

def calculate_nihss_severity(total_score: int) -> str:
    """
    Calculate NIHSS severity based on total score
    
    NIHSS Score interpretation:
    0: No stroke symptoms
    1-4: Minor stroke
    5-15: Moderate stroke
    16-20: Moderate to severe stroke
    21-42: Severe stroke
    """
    if total_score <= 0:
        return "No stroke symptoms"
    elif 1 <= total_score <= 4:
        return "Minor Stroke"
    elif 5 <= total_score <= 15:
        return "Moderate Stroke"
    elif 16 <= total_score <= 20:
        return "Moderate to Severe Stroke"
    elif 21 <= total_score <= 42:
        return "Severe Stroke"
    else:
        return "Invalid Score"

@router.post("/nihss/analyze")
async def analyze_nihss(input_data: NIHSSInput):
    try:
        # Convert input data to dictionary
        input_dict = input_data.dict()
        
        # Calculate total score
        total_score = sum(input_dict.values())
        
        try:
            # Try to get prediction from ML model first
            severity = predict_nihss_severity(input_dict)
        except Exception as model_error:
            # Fall back to direct calculation if model fails
            logging.warning(f"ML model error: {str(model_error)}. Using direct calculation.")
            severity = calculate_nihss_severity(total_score)

        # Create response with additional information
        response = {
            "severity": severity,
            "total_score": total_score,
            "interpretation": f"NIHSS Score: {total_score}. {severity}.",
            "recommendations": get_recommendations(severity)
        }

        # Log successful analysis
        logging.info(f"NIHSS analysis completed successfully: Score={total_score}, Severity={severity}")
        return response
    except Exception as e:
        logging.error(f"Error in NIHSS analysis: {str(e)}")
        # Return a user-friendly error but with a success status to avoid 500 errors
        return {
            "severity": "Unable to determine severity",
            "total_score": 0,
            "interpretation": "Error analyzing NIHSS data. Please consult with your healthcare provider.",
            "recommendations": ["Please consult with your healthcare provider for a proper assessment."]
        }

def get_recommendations(severity: str) -> list:
    """
    Get recommendations based on stroke severity
    """
    common_recommendations = [
        "Continue regular medical follow-ups with healthcare providers",
        "Monitor for any new or worsening symptoms",
        "Take medications as prescribed"
    ]
    
    if severity == "No stroke symptoms" or severity == "Minor Stroke":
        return common_recommendations + [
            "Maintain a healthy lifestyle to prevent future strokes",
            "Follow a balanced diet low in salt and saturated fats",
            "Exercise regularly as recommended by your healthcare provider"
        ]
    elif severity == "Moderate Stroke":
        return common_recommendations + [
            "Participate in a structured rehabilitation program",
            "Work with physical and occupational therapists as needed",
            "Consider speech therapy if communication difficulties are present",
            "Implement home modifications for safety if necessary"
        ]
    elif severity == "Moderate to Severe Stroke" or severity == "Severe Stroke":
        return common_recommendations + [
            "Intensive rehabilitation program recommended",
            "Multidisciplinary approach including physical, occupational, and speech therapy",
            "Regular assessment of progress and adjustment of treatment plans",
            "Home care support and potential home modifications",
            "Caregiver support and education"
        ]
    else:
        return common_recommendations

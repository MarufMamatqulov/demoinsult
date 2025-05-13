from fastapi import APIRouter
from pydantic import BaseModel
import openai
import logging
import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ml_models.blood_pressure_analysis import analyze_blood_pressure

router = APIRouter()

# Set OpenAI API key from environment variable
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.warning("OPENAI_API_KEY is not set in environment variables. API calls may fail.")
openai.api_key = openai_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)

class BloodPressureRequest(BaseModel):
    systolic: int
    diastolic: int
    correct_position: bool

class BloodPressureResponse(BaseModel):
    category: str
    message: str

@router.post("/bp/analyze", response_model=BloodPressureResponse)
def analyze_bp(data: BloodPressureRequest):
    try:
        category = analyze_blood_pressure(data.systolic, data.diastolic, data.correct_position)
        logging.info(f"Generated category: {category}")        message = ""
        if category == "Invalid reading: Position incorrect":
            message = "Please ensure correct position during measurement."
        elif category == "Hypertension Stage 2":
            message = "Consult a healthcare provider immediately."
        elif category == "Hypertension Stage 1":
            message = "Monitor your blood pressure regularly and consult a doctor."
        elif category == "Elevated":
            message = "Adopt a healthy lifestyle to prevent hypertension."
        else:
            message = "Your blood pressure is normal. Maintain a healthy lifestyle."
            
        # Generate AI recommendations
        prompt = f"Based on the blood pressure category '{category}', provide detailed recommendations for the patient including lifestyle changes, diet, exercise and monitoring advice."
        try:
            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a medical assistant providing concise, evidence-based recommendations for blood pressure management."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            ai_recommendations = openai_response.choices[0].message['content'].strip()
        except Exception as e:
            logging.error(f"Error generating AI recommendations: {e}")
            ai_recommendations = "Unable to generate AI recommendations at this time."        logging.info(f"Returning response: category={category}, message={message}, AI Recommendations={ai_recommendations}")
        formatted_message = f"""
Category: {category}
Basic Advice: {message}

AI RECOMMENDATIONS:
{ai_recommendations}
"""
        return BloodPressureResponse(category=category, message=formatted_message)

    except Exception as e:
        logging.error(f"Error in blood pressure analysis: {e}")
        return BloodPressureResponse(category="Error", message="An error occurred while analyzing blood pressure.")

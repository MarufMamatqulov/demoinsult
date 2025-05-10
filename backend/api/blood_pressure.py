from fastapi import APIRouter
from pydantic import BaseModel
from ml_models.blood_pressure_analysis import analyze_blood_pressure
import openai
import logging

router = APIRouter()

# Set OpenAI API key
openai.api_key = "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"

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
        logging.info(f"Generated category: {category}")
        message = ""
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
        prompt = f"Based on the blood pressure category '{category}', provide recommendations for the patient."
        try:
            openai_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150
            )
            ai_recommendations = openai_response.choices[0].text.strip()
        except Exception as e:
            logging.error(f"Error generating AI recommendations: {e}")
            ai_recommendations = "Unable to generate AI recommendations at this time."

        logging.info(f"Returning response: category={category}, message={message}, AI Recommendations={ai_recommendations}")
        return BloodPressureResponse(category=category, message=f"{message}\nAI Recommendations: {ai_recommendations}")

    except Exception as e:
        logging.error(f"Error in blood pressure analysis: {e}")
        return BloodPressureResponse(category="Error", message="An error occurred while analyzing blood pressure.")

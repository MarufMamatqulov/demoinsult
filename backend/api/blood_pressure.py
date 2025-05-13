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
    correct_position: bool = True  # Making this optional with a default value

@router.post("/bp/analyze")
def analyze_bp(data: BloodPressureRequest):
    try:
        category = analyze_blood_pressure(data.systolic, data.diastolic, data.correct_position)
        logging.info(f"Generated category: {category}")
        
        # Define appropriate message based on category
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
            
        # Try to get AI recommendations if possible
        ai_recommendations = ""
        try:
            prompt = f"Based on the blood pressure category '{category}' (systolic: {data.systolic}, diastolic: {data.diastolic}), provide concise recommendations."
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
            ai_recommendations = "Unable to generate AI recommendations at this time."
            
        # Format the complete message
        formatted_message = f"""Category: {category}\nBasic Advice: {message}"""
        if ai_recommendations:
            formatted_message += f"\n\nAI RECOMMENDATIONS:\n{ai_recommendations}"
        
        logging.info(f"Returning response for BP analysis: category={category}")
        
        # Return data in a consistent format for frontend
        return {
            "category": category,
            "message": formatted_message,
            "status": "success",
            "systolic": data.systolic,
            "diastolic": data.diastolic
        }

    except Exception as e:
        logging.error(f"Error in blood pressure analysis: {e}")
        return {
            "status": "error", 
            "message": f"Error analyzing blood pressure: {str(e)}"
        }

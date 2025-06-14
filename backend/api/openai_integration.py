from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel
import os
import logging
from typing import Dict, Any, List, Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize router
router = APIRouter()

# Get OpenAI API key from environment variables
try:
    from backend.utils.openai_helper import get_openai_key
    OPENAI_API_KEY = get_openai_key()
    logging.info("Using OpenAI API key from helper")
except (ImportError, ValueError) as e:
    logging.warning(f"OpenAI API key loading error: {str(e)}")
    
    # Try to load directly from .env file if the helper failed
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        # Try to read directly from .env files
        backend_env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        root_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        
        # Check backend/.env
        if os.path.exists(backend_env_path):
            with open(backend_env_path, 'r') as f:
                for line in f:
                    if line.strip().startswith('OPENAI_API_KEY='):
                        OPENAI_API_KEY = line.strip().split('=', 1)[1].strip()
                        if OPENAI_API_KEY.startswith('"') and OPENAI_API_KEY.endswith('"'):
                            OPENAI_API_KEY = OPENAI_API_KEY[1:-1]
                        logging.info(f"Loaded OpenAI API key from {backend_env_path}")
                        break
        
        # Check project root .env if still not found
        if not OPENAI_API_KEY and os.path.exists(root_env_path):
            with open(root_env_path, 'r') as f:
                for line in f:
                    if line.strip().startswith('OPENAI_API_KEY='):
                        OPENAI_API_KEY = line.strip().split('=', 1)[1].strip()
                        if OPENAI_API_KEY.startswith('"') and OPENAI_API_KEY.endswith('"'):
                            OPENAI_API_KEY = OPENAI_API_KEY[1:-1]
                        logging.info(f"Loaded OpenAI API key from {root_env_path}")
                        break
    
    if not OPENAI_API_KEY:
        logging.warning("OPENAI_API_KEY not found. Using placeholder for development.")
        OPENAI_API_KEY = "sk-placeholder-key-for-development"

# Debugging output - mask the key for security
if OPENAI_API_KEY:
    masked_key = f"{OPENAI_API_KEY[:8]}...{OPENAI_API_KEY[-4:]}" if len(OPENAI_API_KEY) > 12 else "***masked***"
    logging.info(f"OpenAI API key loaded: {masked_key}")

# Use the new OpenAI client consistently
try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    logging.info("Using new OpenAI client (>= 1.0.0)")
except ImportError:
    logging.warning("Failed to import new OpenAI client, falling back to legacy client")
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        logging.info("Using legacy OpenAI client (< 1.0.0)")
    except ImportError:
        logging.error("Could not import any OpenAI client. AI features will be disabled.")
        # Create a mock client for development that will return dummy responses
        class MockOpenAIClient:
            def chat_completions_create(self, *args, **kwargs):
                return {"choices": [{"message": {"content": "This is a development mock response."}}]}
        client = MockOpenAIClient()
    openai.api_key = OPENAI_API_KEY

# Models for request and response
class RehabilitationAnalysisRequest(BaseModel):
    assessment_data: Dict[str, Any]
    assessment_type: str
    language: str = "en"

class ChatCompletionRequest(BaseModel):
    messages: List[Dict[str, str]]
    language: str = "en"
    context: Optional[Dict[str, Any]] = None

class AIResponse(BaseModel):
    response: str
    recommendations: Optional[List[str]] = None

# Helper function to generate system prompts based on assessment type
def get_system_prompt(assessment_type: str, language: str) -> str:
    base_prompt = {
        "en": "You are an AI assistant specialized in stroke rehabilitation. Provide a compassionate, clear analysis based on the assessment data.",
        "ru": "Вы - ИИ-ассистент, специализирующийся на реабилитации после инсульта. Предоставьте сострадательный, понятный анализ на основе данных оценки.",
        "uz": "Siz insult reabilitatsiyasiga ixtisoslashgan AI yordamchisiz. Baholash ma'lumotlariga asoslangan hamdard, aniq tahlil taqdim eting."
    }
    
    # Assessment-specific additions to the prompt
    assessment_additions = {
        "nihss": {
            "en": " The NIHSS score measures stroke severity. Scores range from 0 (no stroke symptoms) to 42 (severe stroke). Interpret the score and suggest appropriate rehabilitation approaches.",
            "ru": " Шкала NIHSS измеряет тяжесть инсульта. Баллы варьируются от 0 (нет симптомов инсульта) до 42 (тяжелый инсульт). Интерпретируйте оценку и предложите соответствующие подходы к реабилитации.",
            "uz": " NIHSS ball insult og'irligini o'lchaydi. Ballar 0 (insult alomatlari yo'q) dan 42 (og'ir insult) gacha. Ballni talqin qiling va tegishli reabilitatsiya yondashuvlarini taklif qiling."
        },
        "phq9": {
            "en": " The PHQ-9 score measures depression severity. Scores range from 0-4 (minimal), 5-9 (mild), 10-14 (moderate), 15-19 (moderately severe), 20-27 (severe). Consider how depression may impact stroke recovery.",
            "ru": " Оценка PHQ-9 измеряет тяжесть депрессии. Баллы варьируются от 0-4 (минимальная), 5-9 (легкая), 10-14 (умеренная), 15-19 (умеренно-тяжелая), 20-27 (тяжелая). Рассмотрите, как депрессия может повлиять на восстановление после инсульта.",
            "uz": " PHQ-9 ball depressiya darajasini o'lchaydi. Ballar 0-4 (minimal), 5-9 (yengil), 10-14 (o'rtacha), 15-19 (o'rtacha og'ir), 20-27 (og'ir). Depressiya insultdan keyin tiklanishga qanday ta'sir qilishi mumkinligini ko'rib chiqing."
        },
        "movement": {
            "en": " Analyze the movement assessment data and provide recommendations for improving mobility and strength.",
            "ru": " Проанализируйте данные оценки движения и предоставьте рекомендации по улучшению подвижности и силы.",
            "uz": " Harakat baholash ma'lumotlarini tahlil qiling va harakatchanlik va kuchni yaxshilash bo'yicha tavsiyalar bering."
        },
        "speech": {
            "en": " Analyze the speech and hearing assessment data and provide recommendations for improving communication abilities.",
            "ru": " Проанализируйте данные оценки речи и слуха и предоставьте рекомендации по улучшению коммуникативных способностей.",
            "uz": " Nutq va eshitish baholash ma'lumotlarini tahlil qiling va muloqot qobiliyatlarini yaxshilash bo'yicha tavsiyalar bering."
        },
        "blood_pressure": {
            "en": " Analyze the blood pressure data and provide recommendations for managing blood pressure during stroke recovery.",
            "ru": " Проанализируйте данные артериального давления и предоставьте рекомендации по контролю артериального давления во время восстановления после инсульта.",
            "uz": " Qon bosimi ma'lumotlarini tahlil qiling va insultdan keyin tiklanish davrida qon bosimini boshqarish bo'yicha tavsiyalar bering."
        }
    }
    
    # Get base prompt for the requested language, default to English if not available
    prompt = base_prompt.get(language, base_prompt["en"])
    
    # Add assessment-specific prompt if available
    if assessment_type in assessment_additions:
        lang_specific_addition = assessment_additions[assessment_type].get(language, 
                                                                        assessment_additions[assessment_type]["en"])
        prompt += lang_specific_addition
    
    return prompt

@router.post("/rehabilitation/analysis", response_model=AIResponse)
async def analyze_rehabilitation_data(request: RehabilitationAnalysisRequest):
    """
    Analyze rehabilitation assessment data and provide recommendations
    """
    try:
        # Prepare the messages for OpenAI
        system_prompt = get_system_prompt(request.assessment_type, request.language)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Please analyze this {request.assessment_type} assessment data and provide recommendations: {json.dumps(request.assessment_data)}"}
        ]    # Call OpenAI API
        ai_text = ""  # Initialize ai_text to avoid UnboundLocalError
        try:
            # Use our helper module to handle API version differences
            from backend.utils.openai_helper import create_chat_completion
            ai_text = create_chat_completion(
                messages=messages,
                model="gpt-4o",
                temperature=0.7,
                max_tokens=1000
            )
        except Exception as api_error:
            logging.error(f"OpenAI API error: {str(api_error)}")
            ai_text = "Sorry, I couldn't process your request. Please try again later."
        
        # Extract recommendations (assuming the AI formats recommendations with bullet points)
        recommendations = []
        for line in ai_text.split('\n'):
            if line.strip().startswith('- ') or line.strip().startswith('• '):
                recommendations.append(line.strip()[2:])
        
        return AIResponse(
            response=ai_text,
            recommendations=recommendations if recommendations else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing rehabilitation data: {str(e)}")

@router.post("/chat/completion", response_model=AIResponse)
async def chat_completion(request: ChatCompletionRequest):
    """
    General purpose chat completion endpoint for the rehabilitation assistant
    """
    try:
        # Add system message if not present
        messages = request.messages
        if not any(msg.get("role") == "system" for msg in messages):
            system_content = {
                "en": "You are a helpful stroke rehabilitation assistant. Provide clear, compassionate guidance for stroke survivors and caregivers.",
                "ru": "Вы - полезный помощник по реабилитации после инсульта. Предоставляйте понятные, сострадательные рекомендации для людей, перенесших инсульт, и их опекунов.",
                "uz": "Siz insult reabilitatsiyasi bo'yicha foydali yordamchisiz. Insultdan keyin tirilgan bemorlar va ularning parvarishlovchilari uchun aniq, hamdard ko'rsatmalar bering."
            }
            messages.insert(0, {
                "role": "system", 
                "content": system_content.get(request.language, system_content["en"])
            })        # Add context if provided
        if request.context:
            context_msg = f"Context information: {json.dumps(request.context)}"
            messages.insert(1, {"role": "system", "content": context_msg})
          # Call OpenAI API
        try:
            # Use our helper module to handle API version differences
            from backend.utils.openai_helper import create_chat_completion
            
            response_text = create_chat_completion(
                messages=messages,
                model="gpt-4o",
                temperature=0.7,
                max_tokens=1000
            )
            
            # Return the response
            return AIResponse(
                response=response_text,
                recommendations=None
            )
        except Exception as api_error:
            logging.error(f"OpenAI API error in chat completion: {str(api_error)}")
            # Return a friendly error message instead of raising an exception
            return AIResponse(
                response="Sorry, I encountered an issue processing your request. Please try again later.",
                recommendations=None
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat completion: {str(e)}")

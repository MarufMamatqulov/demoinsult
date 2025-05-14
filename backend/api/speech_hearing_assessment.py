from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import openai
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)

class SpeechHearingQuestion(BaseModel):
    id: int
    score: int  # 0-3 score

class SpeechHearingRequest(BaseModel):
    questions: List[SpeechHearingQuestion]
    language: str  # 'en', 'es', 'ru'
    patient_name: str
    patient_age: int
    assessor_relationship: str  # relationship to patient

class SpeechHearingResponse(BaseModel):
    speech_score: int
    hearing_score: int
    total_score: int
    speech_level: str
    hearing_level: str
    overall_level: str
    recommendations: str
    
@router.post("/speech-hearing", response_model=SpeechHearingResponse)
def analyze_speech_hearing_alt(data: SpeechHearingRequest):
    """Alternative endpoint for speech hearing assessment that matches frontend path"""
    return analyze_speech_hearing(data)

@router.post("/assessment/speech-hearing", response_model=SpeechHearingResponse)
def analyze_speech_hearing(data: SpeechHearingRequest):
    try:
        # Calculate scores
        questions = data.questions
        
        # Questions 1-5 are for speech assessment
        speech_questions = [q for q in questions if q.id <= 5]
        speech_score = sum(q.score for q in speech_questions)
        
        # Questions 6-10 are for hearing assessment
        hearing_questions = [q for q in questions if q.id > 5]
        hearing_score = sum(q.score for q in hearing_questions)
        
        total_score = speech_score + hearing_score
        
        # Determine levels
        speech_level = get_level(speech_score, 15)
        hearing_level = get_level(hearing_score, 15)
        overall_level = get_level(total_score, 30)
        
        # Generate AI recommendations
        recommendations = generate_ai_recommendations(
            speech_score, hearing_score, total_score,
            speech_level, hearing_level, overall_level,
            data.language, data.patient_age
        )
        
        logging.info(f"Analyzed speech and hearing assessment: Speech={speech_score}, Hearing={hearing_score}, Total={total_score}")
        
        return SpeechHearingResponse(
            speech_score=speech_score,
            hearing_score=hearing_score,
            total_score=total_score,
            speech_level=speech_level,
            hearing_level=hearing_level,
            overall_level=overall_level,
            recommendations=recommendations
        )
        
    except Exception as e:
        logging.error(f"Error in speech and hearing assessment: {e}")
        return SpeechHearingResponse(
            speech_score=0,
            hearing_score=0,
            total_score=0,
            speech_level="Error",
            hearing_level="Error",
            overall_level="Error",
            recommendations="An error occurred while analyzing the assessment."
        )

def get_level(score: int, max_score: int) -> str:
    percentage = (score / max_score) * 100
    
    if percentage >= 85:
        return "Excellent"
    elif percentage >= 70:
        return "Good"
    elif percentage >= 50:
        return "Fair"
    else:
        return "Poor"

def generate_ai_recommendations(speech_score: int, hearing_score: int, total_score: int,
                              speech_level: str, hearing_level: str, overall_level: str,
                              language: str, patient_age: int) -> str:
    try:
        # Create a prompt for OpenAI
        if language == 'es':
            prompt = f"""
            Paciente de {patient_age} años con evaluación de habla y audición:
            - Puntuación del habla: {speech_score}/15 (Nivel: {speech_level})
            - Puntuación auditiva: {hearing_score}/15 (Nivel: {hearing_level})
            - Puntuación total: {total_score}/30 (Nivel: {overall_level})
            
            Por favor, proporcione recomendaciones profesionales médicas detalladas para mejorar las habilidades 
            de habla y audición de este paciente basadas en las puntuaciones anteriores. 
            Incluya ejercicios, terapias y recursos disponibles.
            """
        elif language == 'ru':
            prompt = f"""
            Пациент {patient_age} лет с оценкой речи и слуха:
            - Оценка речи: {speech_score}/15 (Уровень: {speech_level})
            - Оценка слуха: {hearing_score}/15 (Уровень: {hearing_level})
            - Общая оценка: {total_score}/30 (Уровень: {overall_level})
            
            Пожалуйста, предоставьте подробные профессиональные медицинские рекомендации для улучшения 
            речевых и слуховых навыков этого пациента на основе приведенных выше оценок. 
            Включите упражнения, терапию и доступные ресурсы.
            """
        else:  # default to English
            prompt = f"""
            {patient_age}-year-old patient with speech and hearing assessment:
            - Speech score: {speech_score}/15 (Level: {speech_level})
            - Hearing score: {hearing_score}/15 (Level: {hearing_level})
            - Total score: {total_score}/30 (Level: {overall_level})
            
            Please provide detailed professional medical recommendations to improve this patient's 
            speech and hearing abilities based on the above scores. Include exercises, 
            therapies, and available resources.
            """        # Call OpenAI API
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a speech and hearing specialist providing professional medical recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        recommendations = openai_response.choices[0].message['content'].strip()
        return recommendations
        
    except Exception as e:
        logging.error(f"Error generating AI recommendations: {e}")
        return "Unable to generate AI recommendations at this time."

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import openai
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)

class MovementQuestion(BaseModel):
    id: int
    score: int  # 0-3 score

class MovementRequest(BaseModel):
    questions: List[MovementQuestion]
    language: str  # 'en', 'es', 'ru'
    patient_name: str
    patient_age: int
    assessor_relationship: str  # relationship to patient

class MovementResponse(BaseModel):
    upper_limb_score: int
    lower_limb_score: int
    balance_score: int
    total_score: int
    upper_limb_level: str
    lower_limb_level: str
    balance_level: str
    overall_level: str
    recommendations: str
    
@router.post("/assessment/movement", response_model=MovementResponse)
def analyze_movement(data: MovementRequest):
    try:
        # Calculate scores
        questions = data.questions
        
        # Questions 1-5 are for upper limb assessment
        upper_limb_questions = [q for q in questions if q.id <= 5]
        upper_limb_score = sum(q.score for q in upper_limb_questions)
        
        # Questions 6-9 are for lower limb assessment
        lower_limb_questions = [q for q in questions if 6 <= q.id <= 9]
        lower_limb_score = sum(q.score for q in lower_limb_questions)
        
        # Questions 10-13 are for balance assessment
        balance_questions = [q for q in questions if q.id >= 10]
        balance_score = sum(q.score for q in balance_questions)
        
        total_score = upper_limb_score + lower_limb_score + balance_score
        
        # Determine levels
        upper_limb_level = get_level(upper_limb_score, 15)
        lower_limb_level = get_level(lower_limb_score, 12)
        balance_level = get_level(balance_score, 12)
        overall_level = get_level(total_score, 39)
        
        # Generate AI recommendations
        recommendations = generate_ai_recommendations(
            upper_limb_score, lower_limb_score, balance_score, total_score,
            upper_limb_level, lower_limb_level, balance_level, overall_level,
            data.language, data.patient_age
        )
        
        logging.info(f"Analyzed movement assessment: Upper Limb={upper_limb_score}, Lower Limb={lower_limb_score}, " +
                     f"Balance={balance_score}, Total={total_score}")
        
        return MovementResponse(
            upper_limb_score=upper_limb_score,
            lower_limb_score=lower_limb_score,
            balance_score=balance_score,
            total_score=total_score,
            upper_limb_level=upper_limb_level,
            lower_limb_level=lower_limb_level,
            balance_level=balance_level,
            overall_level=overall_level,
            recommendations=recommendations
        )
        
    except Exception as e:
        logging.error(f"Error in movement assessment: {e}")
        return MovementResponse(
            upper_limb_score=0,
            lower_limb_score=0,
            balance_score=0,
            total_score=0,
            upper_limb_level="Error",
            lower_limb_level="Error",
            balance_level="Error",
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

def generate_ai_recommendations(upper_limb_score: int, lower_limb_score: int, 
                              balance_score: int, total_score: int,
                              upper_limb_level: str, lower_limb_level: str, 
                              balance_level: str, overall_level: str,
                              language: str, patient_age: int) -> str:
    try:
        # Create a prompt for OpenAI
        if language == 'es':
            prompt = f"""
            Paciente de {patient_age} años con evaluación de movimiento:
            - Puntuación de extremidades superiores: {upper_limb_score}/15 (Nivel: {upper_limb_level})
            - Puntuación de extremidades inferiores: {lower_limb_score}/12 (Nivel: {lower_limb_level})
            - Puntuación de equilibrio: {balance_score}/12 (Nivel: {balance_level})
            - Puntuación total: {total_score}/39 (Nivel: {overall_level})
            
            Por favor, proporcione recomendaciones profesionales médicas detalladas para mejorar las habilidades 
            motoras de este paciente basadas en las puntuaciones anteriores. 
            Incluya ejercicios específicos, terapias físicas y recursos disponibles. Sea específico para cada área (extremidades superiores, extremidades inferiores y equilibrio).
            """
        elif language == 'ru':
            prompt = f"""
            Пациент {patient_age} лет с оценкой движения:
            - Оценка верхних конечностей: {upper_limb_score}/15 (Уровень: {upper_limb_level})
            - Оценка нижних конечностей: {lower_limb_score}/12 (Уровень: {lower_limb_level})
            - Оценка равновесия: {balance_score}/12 (Уровень: {balance_level})
            - Общая оценка: {total_score}/39 (Уровень: {overall_level})
            
            Пожалуйста, предоставьте подробные профессиональные медицинские рекомендации для улучшения 
            двигательных навыков этого пациента на основе приведенных выше оценок. 
            Включите конкретные упражнения, физическую терапию и доступные ресурсы. Будьте конкретны для каждой области (верхние конечности, нижние конечности и равновесие).
            """
        else:  # default to English
            prompt = f"""
            {patient_age}-year-old patient with movement assessment:
            - Upper limb score: {upper_limb_score}/15 (Level: {upper_limb_level})
            - Lower limb score: {lower_limb_score}/12 (Level: {lower_limb_level})
            - Balance score: {balance_score}/12 (Level: {balance_level})
            - Total score: {total_score}/39 (Level: {overall_level})
            
            Please provide detailed professional medical recommendations to improve this patient's 
            movement abilities based on the above scores. Include specific exercises, 
            physical therapies, and available resources. Be specific for each area (upper limbs, lower limbs, and balance).
            """        # Call OpenAI API
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a physical therapy and rehabilitation specialist providing professional medical recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        recommendations = openai_response.choices[0].message['content'].strip()
        return recommendations
        
    except Exception as e:
        logging.error(f"Error generating AI recommendations: {e}")
        return "Unable to generate AI recommendations at this time."

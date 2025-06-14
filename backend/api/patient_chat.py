from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import json

# Import our custom OpenAI helper for version compatibility
from backend.utils.openai_helper import create_chat_completion

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)

class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant' or 'system'
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    patient_context: Optional[Dict[str, Any]] = None
    language: str = "en"

class ChatResponse(BaseModel):
    response: str
    advice: Optional[str] = None

@router.post("/patient-chat", response_model=ChatResponse)
async def get_chat_response(request: ChatRequest):
    """
    Get AI response for patient chat interactions.
    This can be used either for:
    1. Questions about assessment results
    2. General medical questions related to stroke rehabilitation
    """
    try:
        # Convert messages to OpenAI format
        openai_messages = []
        
        # Add system message with medical context
        system_message = "You are a helpful medical assistant specializing in stroke rehabilitation. "
        system_message += "Provide accurate, clear, and compassionate responses to patients and their relatives. "
        system_message += "Focus on evidence-based advice but explain it in simple terms. "
        system_message += "Do not provide specific medical diagnoses or prescribe medication. "
        system_message += "For serious concerns, always recommend consulting with healthcare professionals."
        
        openai_messages.append({"role": "system", "content": system_message})
        
        # Add patient context if available
        if request.patient_context:
            context_message = "Patient information: "
            for key, value in request.patient_context.items():
                context_message += f"{key}: {value}, "
            openai_messages.append({"role": "system", "content": context_message})
            
        # Add conversation history
        for message in request.messages:
            openai_messages.append({"role": message.role, "content": message.content})
        
        # Select appropriate language instruction
        language_instruction = ""
        if request.language == "es":
            language_instruction = "Please respond in Spanish."
        elif request.language == "ru":
            language_instruction = "Please respond in Russian."
        elif request.language == "uz":
            language_instruction = "Please respond in Uzbek."
        
        # Auto-detect language from the last user message if no language specified
        if not language_instruction:
            last_user_message = ""
            for msg in reversed(openai_messages):
                if msg["role"] == "user":
                    last_user_message = msg["content"]
                    break
            
            # Simple language detection based on common words
            # This is a simplified approach - in production you might want to use a proper language detection library
            if any(word in last_user_message.lower() for word in ["qanday", "nima", "qachon", "qayerda", "nega"]):
                language_instruction = "Please respond in Uzbek."
            elif any(word in last_user_message.lower() for word in ["как", "что", "когда", "где", "почему"]):
                language_instruction = "Please respond in Russian."
            elif any(word in last_user_message.lower() for word in ["cómo", "qué", "cuándo", "dónde", "por qué"]):
                language_instruction = "Please respond in Spanish."
        
        if language_instruction:
            # Add language instruction to system message for better results
            openai_messages.insert(1, {"role": "system", "content": language_instruction})
        
        logging.info(f"Sending chat request to OpenAI with {len(openai_messages)} messages")
        
        # Call OpenAI API using our helper function
        chat_response = create_chat_completion(
            messages=openai_messages,
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0.7
        )
        
        # Generate additional health advice if this is a question about assessment results
        advice = None
        if any(keyword in str(request.messages[-1].content).lower() for keyword in 
               ["result", "score", "assessment", "test", "evaluation", "natija", "baho", "результат", "оценка"]):
            
            context_info = ""
            if request.patient_context:
                # Extract specific assessment context
                assessment_type = request.patient_context.get("assessmentType", "")
                assessment_data = request.patient_context.get("assessmentResults", {})
                
                if assessment_type and assessment_data:
                    context_info = f"Assessment type: {assessment_type}. Assessment data: {json.dumps(assessment_data)}. "
            
            advice_prompt = f"{context_info}Based on the patient's assessment results, provide 3-5 specific and personalized recommendations for stroke rehabilitation. Include specific exercises, lifestyle changes, and monitoring advice. {language_instruction}"
            
            # Use our helper for the advice response too
            advice = create_chat_completion(
                messages=[
                    {"role": "system", "content": system_message}, 
                    {"role": "user", "content": advice_prompt}
                ],
                model="gpt-3.5-turbo",
                max_tokens=400,
                temperature=0.7
            )
            
        logging.info(f"Chat response generated successfully")
        
        return ChatResponse(response=chat_response, advice=advice)
        
    except Exception as e:
        logging.error(f"Error in patient chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat service error: {str(e)}")

@router.post("/assessment-advice", response_model=ChatResponse)
async def get_assessment_advice(request: Request):
    """
    Generate specific advice based on assessment results
    """
    try:
        # Parse request body
        body = await request.json()
        assessment_type = body.get("assessment_type")
        results = body.get("results", {})
        language = body.get("language", "en")
        
        if not assessment_type or not results:
            raise HTTPException(status_code=400, detail="Missing assessment data")
            
        # Construct prompt based on assessment type
        if assessment_type == "speech_hearing":
            prompt = f"""
            Based on these speech and hearing assessment results:
            - Speech score: {results.get('speech_score', 'N/A')}/15 (Level: {results.get('speech_level', 'N/A')})
            - Hearing score: {results.get('hearing_score', 'N/A')}/15 (Level: {results.get('hearing_level', 'N/A')})
            - Total score: {results.get('total_score', 'N/A')}/30 (Level: {results.get('overall_level', 'N/A')})
            
            Provide comprehensive rehabilitation advice, including:
            1. Specific exercises the patient should practice daily
            2. Technology tools or apps that might help
            3. When they should see a specialist
            4. Signs of improvement to look for
            5. How family members can assist in the rehabilitation process
            """
            
        elif assessment_type == "movement":
            prompt = f"""
            Based on these movement assessment results:
            - Upper limb score: {results.get('upper_limb_score', 'N/A')}/15 (Level: {results.get('upper_limb_level', 'N/A')})
            - Lower limb score: {results.get('lower_limb_score', 'N/A')}/12 (Level: {results.get('lower_limb_level', 'N/A')})
            - Balance score: {results.get('balance_score', 'N/A')}/12 (Level: {results.get('balance_level', 'N/A')})
            - Total score: {results.get('total_score', 'N/A')}/39 (Level: {results.get('overall_level', 'N/A')})
            
            Provide comprehensive rehabilitation advice, including:
            1. Specific exercises for each area (upper limbs, lower limbs, balance)
            2. Safety precautions to prevent falls
            3. Adaptive equipment recommendations
            4. Goal setting for recovery milestones
            5. How to track progress effectively
            """
            
        elif assessment_type == "phq9":
            prompt = f"""
            Based on the PHQ-9 depression assessment with a score of {results.get('score', 'N/A')} 
            (Category: {results.get('category', 'N/A')}),
            
            Provide comprehensive psychological support advice, including:
            1. Self-care strategies for mental health
            2. When to seek professional help
            3. How family members can provide emotional support
            4. Daily activities to improve mood
            5. How mental health connects with overall recovery
            """
            
        elif assessment_type == "blood_pressure":
            prompt = f"""
            Based on the blood pressure reading in category '{results.get('category', 'N/A')}',
            
            Provide comprehensive health management advice, including:
            1. Diet recommendations specific to this blood pressure level
            2. Exercise guidelines appropriate for stroke rehabilitation patients
            3. Stress management techniques
            4. Monitoring schedule recommendations
            5. Warning signs that require immediate medical attention
            """
            
        else:
            prompt = f"Provide general rehabilitation advice for a stroke patient based on their assessment results."
        
        # Add language instruction
        if language == "es":
            prompt += "\nPlease respond in Spanish."
        elif language == "ru":
            prompt += "\nPlease respond in Russian."
            
        # Get response from OpenAI using our helper
        advice = create_chat_completion(
            messages=[
                {"role": "system", "content": "You are a medical specialist providing comprehensive rehabilitation advice for stroke patients."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=550,
            temperature=0.7
        )
        
        return ChatResponse(
            response="Assessment advice generated successfully.", 
            advice=advice
        )
        
    except Exception as e:
        logging.error(f"Error generating assessment advice: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Assessment advice error: {str(e)}")

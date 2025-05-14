from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import openai
import json
import os
import logging
from starlette.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

# Custom middleware to handle response content length issues
class ContentLengthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if hasattr(response, "body") and isinstance(response.body, bytes):
            # Update Content-Length header to match actual body size
            response.headers["Content-Length"] = str(len(response.body))
        return response

# Load environment variables
load_dotenv()

from api.phq9 import router as phq9_router, PHQInput
from api.alert_test_api import router as alert_test_router
from api.alerts_api import router as alerts_router
# Removing test routers but adding production routers
# from api.audio_test_api import router as audio_test_router
# from api.video_test_api import router as video_test_router
from api.audio_routes import router as audio_router
from api.video_routes import router as video_router
from api.report_api import router as report_router
from api.bp_trend import router as bp_trend_router
from api.speech_hearing_assessment import router as speech_hearing_router
from api.movement_assessment import router as movement_router
from api.export_assessment import router as export_router
from api.patient_chat import router as patient_chat_router
from api.nihss import router as nihss_router
from api.openai_integration import router as openai_router, RehabilitationAnalysisRequest

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Add project root to Python path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load the trained model
model = joblib.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "../ml_models/phq_model.pkl")))

# Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware to handle Content-Length issues
app.add_middleware(ContentLengthMiddleware)

# Set OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables. Please check your .env file.")
openai.api_key = openai_api_key

class PHQData(BaseModel):
    phq1: int
    phq2: int
    phq3: int
    phq4: int
    phq5: int
    phq6: int
    phq7: int
    phq8: int
    phq9: int

@app.post("/predict")
def predict(data: PHQData):
    features = np.array([[
        data.phq1, data.phq2, data.phq3, data.phq4, data.phq5,
        data.phq6, data.phq7, data.phq8, data.phq9
    ]])
    prediction = model.predict(features)
    return {"prediction": prediction[0]}

# Health-check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ai/rehabilitation/analysis")
async def global_rehabilitation_analysis(request: Request):
    """
    Endpoint that handles rehabilitation analysis requests
    This is needed because frontend is sending requests to /ai/rehabilitation/analysis
    but the actual implementation is at /ai/rehabilitation/analysis
    """
    try:
        # Get the request body
        data = await request.json()
        
        # Import the openai integration function
        from api.openai_integration import analyze_rehabilitation_data
        
        # Create the request model
        rehab_request = RehabilitationAnalysisRequest(
            assessment_type=data.get("assessment_type", "unknown"),
            assessment_data=data.get("assessment_data", {}),
            language=data.get("language", "en")
        )
        
        # Call the handler
        return await analyze_rehabilitation_data(rehab_request)
    except Exception as e:
        logging.error(f"Error in rehabilitation analysis: {str(e)}")
        return {
            "status": "error",
            "message": f"Error processing rehabilitation request: {str(e)}",
            "response": "An error occurred during analysis. Please try again later."
        }

@app.post("/analyze")
async def global_analyze(request: Request):
    """
    Global analyze endpoint to handle various analysis requests and forward them to the appropriate endpoint
    """
    try:
        # Get the request body
        data = await request.json()
        
        # Determine the type of analysis from the request body
        assessment_type = data.get("assessment_type", "unknown")
        
        if assessment_type == "phq9":
            # Forward to PHQ-9 endpoint
            from api.phq9 import analyze_phq
            return await analyze_phq(PHQInput(**data))
        elif assessment_type == "nihss":
            # Forward to NIHSS endpoint
            from api.nihss import analyze_nihss, NIHSSInput
            return await analyze_nihss(NIHSSInput(**data))
        elif assessment_type == "blood_pressure":
            # Forward to blood pressure endpoint
            from api.blood_pressure import analyze_bp, BloodPressureRequest
            return analyze_bp(BloodPressureRequest(**data))
        elif assessment_type == "speech_hearing":
            # Forward to speech-hearing assessment
            from api.speech_hearing_assessment import analyze_speech_hearing
            return analyze_speech_hearing(data)
        elif assessment_type == "movement":
            # Forward to movement assessment
            from api.movement_assessment import analyze_movement
            return analyze_movement(data)
        elif assessment_type == "audio":
            # Forward to audio analysis
            from api.audio_routes import analyze_audio
            return await analyze_audio(request)
        elif assessment_type == "video":
            # Forward to video analysis
            from api.video_routes import analyze_video
            return await analyze_video(request)
        else:
            return {
                "status": "error",
                "message": f"Unknown assessment type: {assessment_type}. Please specify a valid assessment_type."
            }
    except Exception as e:
        logging.error(f"Error in global analyze endpoint: {str(e)}")
        return {
            "status": "error",
            "message": f"Error processing request: {str(e)}"
        }

# Include routers
app.include_router(phq9_router, prefix="/phq")
app.include_router(alert_test_router, prefix="/alert-test")
app.include_router(alerts_router, prefix="/alerts")
# Include audio and video production routers
app.include_router(audio_router, prefix="/audio")
app.include_router(video_router, prefix="/video")
app.include_router(report_router, prefix="/report")
app.include_router(bp_trend_router, prefix="/bp-trend")
app.include_router(speech_hearing_router, prefix="/assessment")
app.include_router(movement_router, prefix="/assessment")
app.include_router(export_router, prefix="/export")
app.include_router(patient_chat_router, prefix="/chat")
app.include_router(nihss_router)  # No prefix, since router already has /nihss prefix
app.include_router(openai_router, prefix="/ai")

@app.middleware("http")
async def add_recommendations(request: Request, call_next):
    response = await call_next(request)

    # Only process JSON responses from specific assessment endpoints and skip streaming responses
    if (response.headers.get("content-type") == "application/json" and 
        not isinstance(response, StreamingResponse) and
        ("/assessment" in request.url.path or "/phq" in request.url.path)):
        try:
            # Collect the entire response body
            body_chunks = []
            async for chunk in response.body_iterator:
                body_chunks.append(chunk)
            body = b"".join(body_chunks)
            
            # Parse the JSON data
            data = json.loads(body)
            
            # Dont add recommendations if they already exist or if there is an error status
            if "recommendations" not in data and data.get("status") != "error":
                try:
                    # Use a simplified approach without calling OpenAI directly
                    # This ensures the API works even without OpenAI access
                    data["recommendations"] = "Please consult with a healthcare professional for personalized advice based on these results."
                except Exception as e:
                    print(f"Error in middleware: {str(e)}")
                    data["recommendations"] = "Recommendations unavailable."
            
            # Create a new response with the modified data
            # This ensures Content-Length is correctly calculated
            return JSONResponse(content=data, status_code=response.status_code, headers=dict(response.headers))
        except Exception as e:
            # If any error occurs processing the response, log and return the original
            print(f"Error processing response: {str(e)}")
            # We cannot return the original response as its body iterator has been consumed
            # Instead, create a new response with an error message
            return JSONResponse(
                content={"status": "error", "message": "Error processing response"},
                status_code=500
            )

    return response

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import logging
import random
from starlette.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv
from datetime import datetime
import time
from collections import defaultdict, deque

# Rate limiting utility
class RateLimiter:
    def __init__(self, max_requests=60, per_seconds=60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.request_timestamps = defaultdict(lambda: deque(maxlen=max_requests))
    
    def check_rate_limit(self, client_id):
        """
        Check if a client has exceeded their rate limit
        Returns (is_allowed, retry_after) tuple
        """
        now = time.time()
        client_timestamps = self.request_timestamps[client_id]
        
        # If client hasn't made max_requests yet, allow the request
        if len(client_timestamps) < self.max_requests:
            client_timestamps.append(now)
            return True, 0
        
        # Check if the oldest request is older than the window
        time_diff = now - client_timestamps[0]
        if time_diff > self.per_seconds:
            # Window has passed, allow the request
            client_timestamps.append(now)
            return True, 0
        
        # Client has exceeded rate limit
        retry_after = self.per_seconds - time_diff
        return False, round(retry_after, 1)
    
    def cleanup(self, max_age=300):
        """Remove clients that haven't made requests recently"""
        now = time.time()
        expired_clients = []
        
        for client_id, timestamps in self.request_timestamps.items():
            if not timestamps or now - timestamps[-1] > max_age:
                expired_clients.append(client_id)
                
        for client_id in expired_clients:
            del self.request_timestamps[client_id]

# Custom middleware to handle response content length issues
class ContentLengthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Initialize rate limiters for different endpoints
        self.profile_limiter = RateLimiter(max_requests=10, per_seconds=5)  # 10 requests per 5 seconds
    
    async def dispatch(self, request, call_next):
        # Handle profile endpoint with reasonable rate limiting
        if request.url.path == "/auth/me/profile":
            client_id = request.client.host if request.client else "unknown"
            allowed, retry_after = self.profile_limiter.check_rate_limit(client_id)
            
            if not allowed:
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": f"Too many profile requests. Please wait {retry_after} seconds before requesting again.",
                        "retry_after": retry_after
                    },
                    headers={"Retry-After": str(retry_after)}
                )
            
            # Periodically clean up old rate limit records
            if random.random() < 0.01:  # 1% chance on each request
                self.profile_limiter.cleanup()
        
        response = await call_next(request)
        
        # For API endpoints returning JSON arrays, return response without modifications
        if request.url.path.startswith("/assessments/history"):
            # Ensure content-length is correct for assessment history endpoints
            if hasattr(response, "body") and isinstance(response.body, bytes):
                response.headers["Content-Length"] = str(len(response.body))
            return response
            
        # Check if it's a regular response with a body
        if hasattr(response, "body") and isinstance(response.body, bytes):
            # Update Content-Length header to match actual body size
            response.headers["Content-Length"] = str(len(response.body))
        
        # For streaming responses, ensure proper handling
        if isinstance(response, StreamingResponse):
            # For streaming responses, we should avoid setting Content-Length
            # since the exact size may not be known in advance
            if "Content-Length" in response.headers:
                del response.headers["Content-Length"]
            return response
            
        # Special handling for certain response types that might cause content-length issues
        if response.status_code in (204, 304):  # No content or Not modified
            if "Content-Length" in response.headers:
                del response.headers["Content-Length"]
            return response
        
        # Handle JSON responses that might have encoding differences
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            if hasattr(response, "body") and isinstance(response.body, bytes):
                # Ensure Content-Length exactly matches the body size
                content_length = len(response.body)
                response.headers["Content-Length"] = str(content_length)
                
        # Ensure assessments endpoints have correct headers
        if request.url.path.startswith("/assessments"):
            if hasattr(response, "body") and isinstance(response.body, bytes):
                response.headers["Content-Length"] = str(len(response.body))
                response.headers["X-Content-Type-Options"] = "nosniff"
                
        return response

# Load environment variables
load_dotenv()

# Import OpenAI integration fix to ensure API key is properly loaded
try:
    import sys
    import os
    # Add the project root to the path so we can import the fix_openai_integration module
    project_root = os.path.dirname(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.append(project_root)
    
    from fix_openai_integration import fix_openai_integration
    openai_fix_success = fix_openai_integration()
    if openai_fix_success:
        logging.info("Successfully applied OpenAI integration fix")
    else:
        logging.warning("Failed to apply OpenAI integration fix - will try to continue anyway")
except Exception as e:
    logging.error(f"Error importing OpenAI integration fix: {str(e)}")

# Correctly import API routers with the package prefix
from backend.api.phq9 import router as phq9_router, PHQInput
from backend.api.alert_test_api import router as alert_test_router
from backend.api.alerts_api import router as alerts_router
# Removing test routers but adding production routers
# from backend.api.audio_test_api import router as audio_test_router
# from backend.api.video_test_api import router as video_test_router
from backend.api.audio_routes import router as audio_router
from backend.api.video_routes import router as video_router
from backend.api.report_api import router as report_router
from backend.api.bp_trend import router as bp_trend_router
from backend.api.speech_hearing_assessment import router as speech_hearing_router
from backend.api.movement_assessment import router as movement_router
from backend.api.export_assessment import router as export_router
from backend.api.patient_chat import router as patient_chat_router
from backend.api.nihss import router as nihss_router
from backend.api.openai_integration import router as openai_router, RehabilitationAnalysisRequest
from backend.api.auth import router as auth_router
from backend.api.assessment_history import router as assessment_history_router

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Add project root to Python path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Apply OpenAI helper patches to fix API compatibility issues
try:
    import fix_patient_chat
except ImportError:
    logging.warning("Could not import fix_patient_chat module")

# Load the trained model
model = joblib.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "../ml_models/phq_model.pkl")))

# Import deployment helpers for production environment
try:
    from deployment_helpers import configure_for_production
    # Check if running in production environment
    if os.getenv("RENDER") or os.getenv("PRODUCTION"):
        config = configure_for_production()
        is_production = config["is_production"]
        allowed_origins = config["allowed_origins"]
    else:
        is_production = False
        allowed_origins = [os.getenv("FRONTEND_URL", "http://localhost:3000")]
except ImportError:
    is_production = False
    allowed_origins = [os.getenv("FRONTEND_URL", "http://localhost:3000")]
    logging.warning("Deployment helpers not found, running in development mode")

# Configure CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware to handle Content-Length issues
app.add_middleware(ContentLengthMiddleware)

# Log startup configuration
logging.info(f"Starting application in {'production' if is_production else 'development'} mode")
logging.info(f"CORS allowed origins: {allowed_origins}")

# Set OpenAI API key from environment variable using our helper
try:
    from backend.utils.openai_helper import get_openai_key
    openai_api_key = get_openai_key()
    logging.info("Using OpenAI API key from helper")
except (ImportError, ValueError) as e:
    logging.warning(f"Could not use OpenAI helper: {str(e)}")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment variables. Please check your .env file.")
    # We don't need to set this globally anymore, as our helper will use it

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
        from backend.api.openai_integration import analyze_rehabilitation_data
        
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
            from backend.api.phq9 import analyze_phq
            return await analyze_phq(PHQInput(**data))
        elif assessment_type == "nihss":
            # Forward to NIHSS endpoint
            from backend.api.nihss import analyze_nihss, NIHSSInput
            return await analyze_nihss(NIHSSInput(**data))
        elif assessment_type == "blood_pressure":
            # Forward to blood pressure endpoint
            from backend.api.blood_pressure import analyze_bp, BloodPressureRequest
            return analyze_bp(BloodPressureRequest(**data))
        elif assessment_type == "speech_hearing":
            # Forward to speech-hearing assessment
            from backend.api.speech_hearing_assessment import analyze_speech_hearing
            return analyze_speech_hearing(data)
        elif assessment_type == "movement":
            # Forward to movement assessment
            from backend.api.movement_assessment import analyze_movement
            return analyze_movement(data)
        elif assessment_type == "audio":
            # Forward to audio analysis
            from backend.api.audio_routes import analyze_audio
            return await analyze_audio(request)
        elif assessment_type == "video":
            # Forward to video analysis
            from backend.api.video_routes import analyze_video
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
# Add blood pressure router
from backend.api.blood_pressure import router as bp_router
app.include_router(bp_router)  # No prefix as router already has /bp prefix
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
app.include_router(openai_router, prefix="/openai")  # Changed from /ai to /openai to match frontend
# Auth router
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(assessment_history_router, prefix="/assessments", tags=["Assessments"])

@app.middleware("http")
async def add_recommendations(request: Request, call_next):
    response = await call_next(request)

    # Skip assessment history endpoints - never modify these responses
    if request.url.path.startswith("/assessments"):
        # Just ensure content-length is correct and return unmodified
        if hasattr(response, "body") and isinstance(response.body, bytes):
            response.headers["Content-Length"] = str(len(response.body))
        return response

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
            
            # Check if data is a list (which would cause 'list' object has no attribute 'get' error)
            if isinstance(data, list):
                # For list responses (like from /assessments/history), don't modify
                pass
            # Dont add recommendations if they already exist or if there is an error status
            elif "recommendations" not in data and data.get("status") != "error":
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

# Start the server when this file is run directly
if __name__ == "__main__":
    import uvicorn
    import time
    print("Starting Stroke Rehabilitation AI Platform API Server...")
    
    try:
        # Add a small delay for any startup processes to complete
        time.sleep(1)
        
        # Better error handling for the server
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

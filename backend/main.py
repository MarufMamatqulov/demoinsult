from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import openai
import json
import os
from starlette.responses import JSONResponse, StreamingResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from api.phq9 import router as phq9_router
from api.alert_test_api import router as alert_test_router
from api.alerts_api import router as alerts_router
# Removing audio and video test routers as requested
# from api.audio_test_api import router as audio_router
# from api.video_test_api import router as video_router
from api.report_api import router as report_router
from api.bp_trend import router as bp_trend_router
from api.speech_hearing_assessment import router as speech_hearing_router
from api.movement_assessment import router as movement_router
from api.export_assessment import router as export_router
from api.patient_chat import router as patient_chat_router
from api.openai_integration import router as openai_router

app = FastAPI()

# Add project root to Python path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load the trained model
model = joblib.load(os.path.abspath(os.path.join(os.path.dirname(__file__), "../ml_models/phq_model.pkl")))

# Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Include routers
app.include_router(phq9_router, prefix="/phq")
app.include_router(alert_test_router, prefix="/alert-test")
app.include_router(alerts_router, prefix="/alerts")
# Removed audio and video routers
# app.include_router(audio_router, prefix="/audio")
# app.include_router(video_router, prefix="/video")
app.include_router(report_router, prefix="/report")
app.include_router(bp_trend_router, prefix="/bp-trend")
app.include_router(speech_hearing_router, prefix="/assessment")
app.include_router(movement_router, prefix="/assessment")
app.include_router(export_router, prefix="/export")
app.include_router(patient_chat_router, prefix="/chat")
app.include_router(openai_router, prefix="/ai")

@app.middleware("http")
async def add_recommendations(request: Request, call_next):
    response = await call_next(request)

    # Only process JSON responses and skip streaming responses
    if response.headers.get("content-type") == "application/json" and not isinstance(response, StreamingResponse):
        body = b"".join([chunk async for chunk in response.body_iterator])
        data = json.loads(body)

        # Generate recommendations using OpenAI API
        try:
            prompt = f"Based on the following data, provide recommendations: {data}"
            openai_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a medical specialist providing professional recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            recommendations = openai_response.choices[0].message['content'].strip()
            data["recommendations"] = recommendations
        except Exception as e:
            data["recommendations"] = f"Error generating recommendations: {str(e)}"

        # Update the response body
        response = JSONResponse(content=data)

    return response

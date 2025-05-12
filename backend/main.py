from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import openai
import json
from starlette.responses import JSONResponse, StreamingResponse

from backend.api.phq9 import router as phq9_router
from backend.api.alert_test_api import router as alert_test_router
from backend.api.alerts_api import router as alerts_router
# Removing audio and video test routers as requested
# from backend.api.audio_test_api import router as audio_router
# from backend.api.video_test_api import router as video_router
from backend.api.report_api import router as report_router
from backend.api.bp_trend import router as bp_trend_router
from backend.api.speech_hearing_assessment import router as speech_hearing_router
from backend.api.movement_assessment import router as movement_router
from backend.api.export_assessment import router as export_router
from backend.api.patient_chat import router as patient_chat_router

app = FastAPI()

# Load the trained model
model = joblib.load("ml_models/phq_model.pkl")

# Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set OpenAI API key
openai.api_key = "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"

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

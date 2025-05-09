from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

from backend.api.phq9 import router as phq9_router
from backend.api.alert_test_api import router as alert_test_router
from backend.api.alerts_api import router as alerts_router
from backend.api.audio_test_api import router as audio_router
from backend.api.video_test_api import router as video_router
from backend.api.report_api import router as report_router

app = FastAPI()

# Load the trained model
model = joblib.load("ml_models/phq_model.pkl")

# Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(audio_router, prefix="/audio")
app.include_router(video_router, prefix="/video")
app.include_router(report_router, prefix="/report")

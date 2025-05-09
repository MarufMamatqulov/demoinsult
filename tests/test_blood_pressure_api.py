import pytest
from fastapi.testclient import TestClient
from backend.api.blood_pressure import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_bp_analyze_normal():
    response = client.post("/bp/analyze", json={"systolic": 115, "diastolic": 75, "correct_position": True})
    assert response.status_code == 200
    assert response.json() == {
        "category": "Normal",
        "message": "Your blood pressure is normal. Maintain a healthy lifestyle."
    }

def test_bp_analyze_elevated():
    response = client.post("/bp/analyze", json={"systolic": 125, "diastolic": 75, "correct_position": True})
    assert response.status_code == 200
    assert response.json() == {
        "category": "Elevated",
        "message": "Adopt a healthy lifestyle to prevent hypertension."
    }

def test_bp_analyze_hypertension_stage_1():
    response = client.post("/bp/analyze", json={"systolic": 135, "diastolic": 85, "correct_position": True})
    assert response.status_code == 200
    assert response.json() == {
        "category": "Hypertension Stage 1",
        "message": "Monitor your blood pressure regularly and consult a doctor."
    }

def test_bp_analyze_hypertension_stage_2():
    response = client.post("/bp/analyze", json={"systolic": 145, "diastolic": 95, "correct_position": True})
    assert response.status_code == 200
    assert response.json() == {
        "category": "Hypertension Stage 2",
        "message": "Consult a healthcare provider immediately."
    }

def test_bp_analyze_invalid_position():
    response = client.post("/bp/analyze", json={"systolic": 115, "diastolic": 75, "correct_position": False})
    assert response.status_code == 200
    assert response.json() == {
        "category": "Invalid reading: Position incorrect",
        "message": "Please ensure correct position during measurement."
    }

def test_bp_analyze_invalid_payload():
    response = client.post("/bp/analyze", json={"systolic": "invalid", "diastolic": 75, "correct_position": True})
    assert response.status_code == 422

from fastapi.testclient import TestClient
from backend.api.nihss import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_analyze_nihss_normal():
    input_data = {
        "nihs_1": 0, "nihs_2": 0, "nihs_3": 0, "nihs_4": 0, "nihs_5": 0,
        "nihs_6": 0, "nihs_7": 0, "nihs_8": 0, "nihs_9": 0, "nihs_10": 0, "nihs_11": 0
    }
    response = client.post("/nihss/analyze", json=input_data)
    assert response.status_code == 200
    assert response.json()["severity"] == "mild"

def test_analyze_nihss_extreme():
    input_data = {
        "nihs_1": 4, "nihs_2": 4, "nihs_3": 4, "nihs_4": 4, "nihs_5": 4,
        "nihs_6": 4, "nihs_7": 4, "nihs_8": 4, "nihs_9": 4, "nihs_10": 4, "nihs_11": 4
    }
    response = client.post("/nihss/analyze", json=input_data)
    assert response.status_code == 200
    assert response.json()["severity"] == "severe"

def test_analyze_nihss_invalid():
    input_data = {
        "nihs_1": 0, "nihs_2": 0, "nihs_3": 0  # Missing keys
    }
    response = client.post("/nihss/analyze", json=input_data)
    assert response.status_code == 422

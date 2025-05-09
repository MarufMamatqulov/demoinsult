import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_post_phq_analyze_valid():
    payload = {f'q{i}': 1 for i in range(1, 10)}
    response = client.post("/phq/analyze", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_post_phq_analyze_extreme():
    payload = {f'q{i}': 3 for i in range(1, 10)}
    response = client.post("/phq/analyze", json=payload)
    assert response.status_code == 200
    assert response.json()["prediction"] == "Severe"

def test_post_phq_analyze_invalid():
    payload = {f'q{i}': 1 for i in range(1, 9)}  # Missing q9
    response = client.post("/phq/analyze", json=payload)
    assert response.status_code == 422

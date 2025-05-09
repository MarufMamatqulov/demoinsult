from fastapi.testclient import TestClient
from backend.api.exercise import router
from fastapi import FastAPI
import io

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_exercise_analyze_valid():
    # Replace 'valid_video.mp4' with the path to a valid video file for testing
    video_content = b"Fake video content for testing"  # Replace with actual video content
    response = client.post(
        "/exercise/analyze",
        files={"file": ("valid_video.mp4", io.BytesIO(video_content), "video/mp4")}
    )
    assert response.status_code == 200
    assert "accuracy" in response.json()
    assert "feedback" in response.json()

def test_exercise_analyze_invalid():
    # Replace 'invalid_video.txt' with the path to an invalid file for testing
    invalid_content = b"This is not a video file"
    response = client.post(
        "/exercise/analyze",
        files={"file": ("invalid_video.txt", io.BytesIO(invalid_content), "text/plain")}
    )
    assert response.status_code == 500

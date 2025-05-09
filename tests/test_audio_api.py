from fastapi.testclient import TestClient
from backend.api.audio import router
from fastapi import FastAPI
import io

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_audio_analyze_valid():
    # Replace 'valid_audio.mp3' with the path to a valid audio file for testing
    audio_content = b"Fake audio content for testing"  # Replace with actual audio content
    response = client.post(
        "/audio/analyze",
        files={"file": ("valid_audio.mp3", io.BytesIO(audio_content), "audio/mpeg")}
    )
    assert response.status_code == 200
    assert "transcription" in response.json()

def test_audio_analyze_invalid():
    # Replace 'invalid_audio.txt' with the path to an invalid file for testing
    invalid_content = b"This is not an audio file"
    response = client.post(
        "/audio/analyze",
        files={"file": ("invalid_audio.txt", io.BytesIO(invalid_content), "text/plain")}
    )
    assert response.status_code == 500

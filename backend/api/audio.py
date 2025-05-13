from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ml_models.audio_transcription import transcribe_audio

router = APIRouter()

@router.post("/audio/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Transcribe the audio file
        transcription = transcribe_audio(temp_file_path)

        # Remove the temporary file
        os.remove(temp_file_path)

        return {"transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

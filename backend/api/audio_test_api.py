from fastapi import APIRouter, UploadFile, HTTPException
from ml_models.audio_cognition import analyze_audio
import shutil

router = APIRouter()

@router.post("/audio/analyze")
async def analyze_audio_endpoint(file: UploadFile):
    """
    Analyze audio file for cognitive patterns.

    Args:
        file (UploadFile): The uploaded audio file (.wav or .mp3).

    Returns:
        dict: Analysis result including speech clarity, repetition score, and cognitive risk level.
    """
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Analyze the audio file
        result = analyze_audio(temp_file_path)

        # Clean up temporary file
        os.remove(temp_file_path)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

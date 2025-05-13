from fastapi import APIRouter, UploadFile, HTTPException
import shutil
import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from ml_models.video_exercise import analyze_exercise_video

router = APIRouter()

@router.post("/video/analyze")
async def analyze_video_endpoint(file: UploadFile):
    """
    Analyze exercise video for movement quality and range.

    Args:
        file (UploadFile): The uploaded video file (max 30 seconds).

    Returns:
        dict: Analysis result with quality score and improvement recommendation.
    """
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Analyze the video file
        result = analyze_exercise_video(temp_file_path)

        # Clean up temporary file
        os.remove(temp_file_path)

        # Add improvement recommendation
        if result['status'] == "Fail":
            result['recommendation'] = "Focus on improving range of motion and consistency."
        else:
            result['recommendation'] = "Keep up the good work!"

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, UploadFile, File, HTTPException
from ml_models.exercise_analysis import analyze_exercise_video
import os

router = APIRouter()

@router.post("/exercise/analyze")
async def analyze_exercise(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        # Analyze the exercise video
        accuracy = analyze_exercise_video(temp_file_path)

        # Remove the temporary file
        os.remove(temp_file_path)

        # Provide feedback based on accuracy
        feedback = "Great job! Keep it up." if accuracy == "Correct" else "Please improve your form."

        return {"accuracy": accuracy, "feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
import os
import logging
import sys
import shutil
from typing import Optional

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import ML model for video analysis if available
try:
    from ml_models.video_exercise import analyze_exercise_video
    ML_AVAILABLE = True
except ImportError:
    logging.warning("Video ML models not available. Video analysis will be limited.")
    ML_AVAILABLE = False

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure upload directory
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads/video"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

class VideoAnalysisResponse(BaseModel):
    filename: str
    file_size: int
    duration: Optional[float] = None
    analysis: Optional[dict] = None
    status: str = "success"
    message: str = ""

@router.post("/upload", response_model=VideoAnalysisResponse)
async def upload_video(file: UploadFile = File(...)):
    """
    Upload and analyze a video file for exercise analysis.
    Supports mp4, mov, avi formats.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
            
        # Check file extension
        allowed_extensions = [".mp4", ".mov", ".avi", ".webm"]
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}"
            )
        
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Initialize response
        response = VideoAnalysisResponse(
            filename=file.filename,
            file_size=file_size
        )
        
        # Perform video analysis if ML models are available
        if ML_AVAILABLE:
            try:
                # Video exercise analysis
                analysis_results = analyze_exercise_video(file_path)
                response.analysis = analysis_results
                
                response.message = "Video successfully uploaded and analyzed"
            except Exception as ml_error:
                logging.error(f"Error in video ML processing: {str(ml_error)}")
                response.message = "Video uploaded, but analysis failed. Basic information only."
        else:
            response.message = "Video uploaded successfully. Analysis not available."
        
        return response
        
    except Exception as e:
        logging.error(f"Error processing video upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing video upload: {str(e)}")

@router.post("/analyze")
async def analyze_video_data(request: Request):
    """
    Analyze previously uploaded video file
    """
    try:
        data = await request.json()
        filename = data.get("filename")
        
        if not filename:
            raise HTTPException(status_code=400, detail="Filename is required")
            
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File {filename} not found")
            
        if ML_AVAILABLE:
            # Video analysis
            analysis_results = analyze_exercise_video(file_path)
            
            return {
                "status": "success",
                "filename": filename,
                "analysis": analysis_results
            }
        else:
            return {
                "status": "error",
                "message": "Video analysis is not available"
            }
            
    except Exception as e:
        logging.error(f"Error in video analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in video analysis: {str(e)}")

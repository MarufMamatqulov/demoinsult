from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
import os
import logging
import sys
import shutil
from typing import Optional

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import ML model for audio processing if available
try:
    from ml_models.audio_cognition import analyze_audio
    from ml_models.audio_transcription import transcribe_audio
    ML_AVAILABLE = True
except ImportError:
    logging.warning("Audio ML models not available. Audio analysis will be limited.")
    ML_AVAILABLE = False

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure upload directory
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads/audio"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

class AudioAnalysisResponse(BaseModel):
    filename: str
    file_size: int
    duration: Optional[float] = None
    transcription: Optional[str] = None
    analysis: Optional[dict] = None
    status: str = "success"
    message: str = ""

@router.post("/upload", response_model=AudioAnalysisResponse)
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload and analyze an audio file.
    Supports wav, mp3, ogg, m4a formats.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
            
        # Check file extension
        allowed_extensions = [".wav", ".mp3", ".ogg", ".m4a"]
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed_extensions:
            extensions_str = ", ".join(allowed_extensions)
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Allowed formats: {extensions_str}"
            )
        
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Initialize response
        response = AudioAnalysisResponse(
            filename=file.filename,
            file_size=file_size
        )
        
        # Perform audio analysis if ML models are available
        if ML_AVAILABLE:
            try:
                # Audio transcription
                transcription = transcribe_audio(file_path)
                response.transcription = transcription
                
                # Audio analysis for speech characteristics and quality
                analysis_results = analyze_audio(file_path)
                response.analysis = analysis_results
                
                response.message = "Audio successfully uploaded and analyzed"
            except Exception as ml_error:
                logging.error(f"Error in audio ML processing: {str(ml_error)}")
                response.message = "Audio uploaded, but analysis failed. Basic information only."
        else:
            response.message = "Audio uploaded successfully. Analysis not available."
        
        return response
        
    except Exception as e:
        logging.error(f"Error processing audio upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing audio upload: {str(e)}")

@router.post("/analyze")
async def analyze_audio_data(request: Request):
    """
    Analyze previously uploaded audio file or audio data from request
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
            # Audio transcription
            transcription = transcribe_audio(file_path)
            
            # Audio analysis
            analysis_results = analyze_audio(file_path)
            
            return {
                "status": "success",
                "filename": filename,
                "transcription": transcription,
                "analysis": analysis_results
            }
        else:
            return {
                "status": "error",
                "message": "Audio analysis is not available"
            }
            
    except Exception as e:
        logging.error(f"Error in audio analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in audio analysis: {str(e)}")

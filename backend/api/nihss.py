from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ml_models.nihss_model import predict_nihss_severity

router = APIRouter()

class NIHSSInput(BaseModel):
    nihs_1: float
    nihs_2: float
    nihs_3: float
    nihs_4: float
    nihs_5: float
    nihs_6: float
    nihs_7: float
    nihs_8: float
    nihs_9: float
    nihs_10: float
    nihs_11: float

@router.post("/nihss/analyze")
async def analyze_nihss(input_data: NIHSSInput):
    try:
        # Convert input data to dictionary
        input_dict = input_data.dict()

        # Get prediction
        severity = predict_nihss_severity(input_dict)

        return {"severity": severity}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

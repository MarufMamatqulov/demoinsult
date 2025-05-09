from fastapi import APIRouter, HTTPException
from ml_models.recommendation_engine import get_recommendations

router = APIRouter()

@router.post("/recommendations/generate")
async def generate_recommendations(inputs: dict):
    """
    Generate recommendations based on the provided inputs.

    Args:
        inputs (dict): A dictionary containing the latest assessment values.

    Returns:
        List[str]: A list of recommendations.
    """
    try:
        return get_recommendations(inputs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

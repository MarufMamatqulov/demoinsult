from fastapi import APIRouter, HTTPException
from backend.utils.alert_sender import send_alert

router = APIRouter()

@router.post("/alert/test")
def test_alert(user_id: int, message: str, method: str):
    """
    Test endpoint to send an alert.

    Args:
        user_id (int): The ID of the user to send the alert to.
        message (str): The alert message to send.
        method (str): The method to use for sending the alert ('telegram' or 'email').

    Returns:
        dict: A success message.
    """
    try:
        send_alert(user_id, message, method)
        return {"detail": "Alert sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

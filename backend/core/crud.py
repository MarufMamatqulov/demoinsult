from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.models.history_models import BloodPressureHistory, NIHSSHistory, BarthelIndexHistory
from backend.models.user import User  # Import the User model

def save_blood_pressure(db: Session, patient_id: str, systolic: float, diastolic: float, time: datetime, comments: str = None):
    entry = BloodPressureHistory(
        patient_id=patient_id,
        systolic=systolic,
        diastolic=diastolic,
        measurement_time=time,
        comments=comments
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_blood_pressure_history(db: Session, patient_id: str, last_n_days: int):
    cutoff_date = datetime.now() - timedelta(days=last_n_days)
    return db.query(BloodPressureHistory).filter(
        BloodPressureHistory.patient_id == patient_id,
        BloodPressureHistory.measurement_time >= cutoff_date
    ).all()

def save_nihss_score(db: Session, patient_id: str, score: float, time: datetime, comments: str = None):
    entry = NIHSSHistory(
        patient_id=patient_id,
        score=score,
        measurement_time=time,
        comments=comments
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_nihss_history(db: Session, patient_id: str, last_n_days: int):
    cutoff_date = datetime.now() - timedelta(days=last_n_days)
    return db.query(NIHSSHistory).filter(
        NIHSSHistory.patient_id == patient_id,
        NIHSSHistory.measurement_time >= cutoff_date
    ).all()

def save_barthel_index(db: Session, patient_id: str, value: float, time: datetime, comments: str = None):
    entry = BarthelIndexHistory(
        patient_id=patient_id,
        value=value,
        measurement_time=time,
        comments=comments
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_barthel_index_history(db: Session, patient_id: str, last_n_days: int):
    cutoff_date = datetime.now() - timedelta(days=last_n_days)
    return db.query(BarthelIndexHistory).filter(
        BarthelIndexHistory.patient_id == patient_id,
        BarthelIndexHistory.measurement_time >= cutoff_date
    ).all()

def get_user_contact_info(db: Session, user_id: str):
    """
    Retrieve user contact information from the database.

    Args:
        db (Session): SQLAlchemy session.
        user_id (str): The ID of the user.

    Returns:
        dict: A dictionary containing user contact information (e.g., email, phone).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return {"email": user.email, "phone": user.phone}
    return None

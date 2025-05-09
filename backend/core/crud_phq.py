from sqlalchemy.orm import Session
from backend.models.phq_history import PHQHistory
from datetime import datetime

def save_phq_history(db: Session, patient_id: str, answers: dict, score: int, level: str):
    entry = PHQHistory(
        patient_id=patient_id,
        q1=answers['q1'],
        q2=answers['q2'],
        q3=answers['q3'],
        q4=answers['q4'],
        q5=answers['q5'],
        q6=answers['q6'],
        q7=answers['q7'],
        q8=answers['q8'],
        q9=answers['q9'],
        score=score,
        level=level,
        created_at=datetime.utcnow()
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_phq_history(db: Session, patient_id: str):
    return db.query(PHQHistory).filter(PHQHistory.patient_id == patient_id).order_by(PHQHistory.created_at.desc()).all()

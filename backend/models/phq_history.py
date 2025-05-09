from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class PHQHistory(Base):
    __tablename__ = 'phq_history'

    id = Column(String, primary_key=True, default=generate_uuid)
    patient_id = Column(String, nullable=False)
    q1 = Column(Integer, nullable=False)
    q2 = Column(Integer, nullable=False)
    q3 = Column(Integer, nullable=False)
    q4 = Column(Integer, nullable=False)
    q5 = Column(Integer, nullable=False)
    q6 = Column(Integer, nullable=False)
    q7 = Column(Integer, nullable=False)
    q8 = Column(Integer, nullable=False)
    q9 = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    level = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

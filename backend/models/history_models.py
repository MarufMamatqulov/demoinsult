from sqlalchemy import Column, String, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class BloodPressureHistory(Base):
    __tablename__ = 'blood_pressure_history'

    id = Column(String, primary_key=True, default=generate_uuid)
    patient_id = Column(String, nullable=False)
    measurement_time = Column(DateTime, nullable=False)
    systolic = Column(Float, nullable=False)
    diastolic = Column(Float, nullable=False)
    comments = Column(Text, nullable=True)

class NIHSSHistory(Base):
    __tablename__ = 'nihss_history'

    id = Column(String, primary_key=True, default=generate_uuid)
    patient_id = Column(String, nullable=False)
    measurement_time = Column(DateTime, nullable=False)
    score = Column(Float, nullable=False)
    comments = Column(Text, nullable=True)

class BarthelIndexHistory(Base):
    __tablename__ = 'barthel_index_history'

    id = Column(String, primary_key=True, default=generate_uuid)
    patient_id = Column(String, nullable=False)
    measurement_time = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    comments = Column(Text, nullable=True)

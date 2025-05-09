from pydantic import BaseModel

class PHQ9Request(BaseModel):
    phq1: int
    phq2: int
    phq3: int
    phq4: int
    phq5: int
    phq6: int
    phq7: int
    phq8: int
    phq9: int

class PHQ9Response(BaseModel):
    prediction: float

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from backend.core.crud import (
    get_blood_pressure_history,
    get_nihss_history,
    get_barthel_index_history
)
from backend.core.crud_phq import get_phq_history
from datetime import datetime, timedelta

def generate_patient_report(db: Session, patient_id: str) -> str:
    """
    Generate a PDF report for a patient.

    Args:
        db (Session): Database session.
        patient_id (str): Patient ID.

    Returns:
        str: Path to the generated PDF file.
    """
    # File path for the PDF
    pdf_path = f"{patient_id}_report.pdf"

    # Create a PDF canvas
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Title
    c.drawString(100, 750, f"Patient Report for {patient_id}")
    c.drawString(100, 735, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Fetch data
    last_30_days = datetime.now() - timedelta(days=30)
    bp_history = get_blood_pressure_history(db, patient_id, 30)
    nihss_history = get_nihss_history(db, patient_id, 30)
    barthel_history = get_barthel_index_history(db, patient_id, 30)
    phq_history = get_phq_history(db, patient_id)

    # Blood Pressure Section
    c.drawString(100, 700, "Blood Pressure History (Last 30 Days):")
    y = 685
    for record in bp_history:
        c.drawString(100, y, f"Date: {record.measurement_time}, Systolic: {record.systolic}, Diastolic: {record.diastolic}")
        y -= 15

    # NIHSS Section
    c.drawString(100, y, "NIHSS History (Last 30 Days):")
    y -= 15
    for record in nihss_history:
        c.drawString(100, y, f"Date: {record.measurement_time}, Score: {record.score}")
        y -= 15

    # Barthel Index Section
    c.drawString(100, y, "Barthel Index History (Last 30 Days):")
    y -= 15
    for record in barthel_history:
        c.drawString(100, y, f"Date: {record.measurement_time}, Value: {record.value}")
        y -= 15

    # PHQ-9 Section
    c.drawString(100, y, "PHQ-9 History:")
    y -= 15
    for record in phq_history:
        c.drawString(100, y, f"Date: {record.created_at}, Score: {record.score}, Level: {record.level}")
        y -= 15

    # Doctor's Recommendation Placeholder
    c.drawString(100, y, "Doctor's Recommendation:")
    y -= 15
    c.drawString(100, y, "[Add recommendation here]")

    # Save the PDF
    c.save()

    return pdf_path

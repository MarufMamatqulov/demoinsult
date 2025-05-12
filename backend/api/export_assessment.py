from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import logging
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)

class ExportRequest(BaseModel):
    patient_name: str
    assessment_type: str  # "speech_hearing" or "movement"
    assessment_data: Dict[str, Any]
    language: str

class ExportResponse(BaseModel):
    file_path: str
    success: bool
    message: str

def generate_pdf_for_speech_hearing(data, language, file_path):
    """Generate a PDF report for speech and hearing assessment"""
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    subtitle_style = styles["Heading2"]
    normal_style = styles["Normal"]
    
    # Get title based on language
    if language == "es":
        title = "Evaluación de Habla y Audición"
        patient_label = "Paciente"
        date_label = "Fecha"
        results_label = "Resultados"
        speech_label = "Puntuación de habla"
        hearing_label = "Puntuación de audición"
        total_label = "Puntuación total"
        recommendations_label = "Recomendaciones"
    elif language == "ru":
        title = "Оценка Речи и Слуха"
        patient_label = "Пациент"
        date_label = "Дата"
        results_label = "Результаты"
        speech_label = "Оценка речи"
        hearing_label = "Оценка слуха"
        total_label = "Общая оценка"
        recommendations_label = "Рекомендации"
    else:  # Default to English
        title = "Speech and Hearing Assessment"
        patient_label = "Patient"
        date_label = "Date"
        results_label = "Results"
        speech_label = "Speech score"
        hearing_label = "Hearing score"
        total_label = "Total score"
        recommendations_label = "Recommendations"
    
    # Add title
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add patient info
    patient_info = [
        [f"{patient_label}:", data["patient_name"]],
        [f"{date_label}:", datetime.now().strftime("%Y-%m-%d %H:%M")]
    ]
    
    patient_table = Table(patient_info, colWidths=[1.5*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (-1, -1), colors.white),
    ]))
    
    elements.append(patient_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Add results
    elements.append(Paragraph(results_label, subtitle_style))
    elements.append(Spacer(1, 0.15*inch))
    
    results_data = [
        [f"{speech_label}:", f"{data['speech_score']}/15 ({data['speech_level']})"],
        [f"{hearing_label}:", f"{data['hearing_score']}/15 ({data['hearing_level']})"],
        [f"{total_label}:", f"{data['total_score']}/30 ({data['overall_level']})"]
    ]
    
    results_table = Table(results_data, colWidths=[2*inch, 3.5*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (-1, -1), colors.white),
    ]))
    
    elements.append(results_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Add recommendations
    elements.append(Paragraph(recommendations_label, subtitle_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Split recommendations by line breaks and add as paragraphs
    recommendations = data['recommendations'].split('\n')
    for rec in recommendations:
        if rec.strip():  # Skip empty lines
            elements.append(Paragraph(rec, normal_style))
            elements.append(Spacer(1, 0.1*inch))
    
    # Build the PDF
    doc.build(elements)
    
def generate_pdf_for_movement(data, language, file_path):
    """Generate a PDF report for movement assessment"""
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    subtitle_style = styles["Heading2"]
    normal_style = styles["Normal"]
    
    # Get title based on language
    if language == "es":
        title = "Evaluación de Movimiento"
        patient_label = "Paciente"
        date_label = "Fecha"
        results_label = "Resultados"
        upper_limb_label = "Puntuación de extremidades superiores"
        lower_limb_label = "Puntuación de extremidades inferiores"
        balance_label = "Puntuación de equilibrio"
        total_label = "Puntuación total"
        recommendations_label = "Recomendaciones"
    elif language == "ru":
        title = "Оценка Движения"
        patient_label = "Пациент"
        date_label = "Дата"
        results_label = "Результаты"
        upper_limb_label = "Оценка верхних конечностей"
        lower_limb_label = "Оценка нижних конечностей"
        balance_label = "Оценка равновесия"
        total_label = "Общая оценка"
        recommendations_label = "Рекомендации"
    else:  # Default to English
        title = "Movement Assessment"
        patient_label = "Patient"
        date_label = "Date"
        results_label = "Results"
        upper_limb_label = "Upper limb score"
        lower_limb_label = "Lower limb score"
        balance_label = "Balance score"
        total_label = "Total score"
        recommendations_label = "Recommendations"
    
    # Add title
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add patient info
    patient_info = [
        [f"{patient_label}:", data["patient_name"]],
        [f"{date_label}:", datetime.now().strftime("%Y-%m-%d %H:%M")]
    ]
    
    patient_table = Table(patient_info, colWidths=[1.5*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (-1, -1), colors.white),
    ]))
    
    elements.append(patient_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Add results
    elements.append(Paragraph(results_label, subtitle_style))
    elements.append(Spacer(1, 0.15*inch))
    
    results_data = [
        [f"{upper_limb_label}:", f"{data['upper_limb_score']}/15 ({data['upper_limb_level']})"],
        [f"{lower_limb_label}:", f"{data['lower_limb_score']}/12 ({data['lower_limb_level']})"],
        [f"{balance_label}:", f"{data['balance_score']}/12 ({data['balance_level']})"],
        [f"{total_label}:", f"{data['total_score']}/39 ({data['overall_level']})"]
    ]
    
    results_table = Table(results_data, colWidths=[2*inch, 3.5*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.darkblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (-1, -1), colors.white),
    ]))
    
    elements.append(results_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Add recommendations
    elements.append(Paragraph(recommendations_label, subtitle_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Split recommendations by line breaks and add as paragraphs
    recommendations = data['recommendations'].split('\n')
    for rec in recommendations:
        if rec.strip():  # Skip empty lines
            elements.append(Paragraph(rec, normal_style))
            elements.append(Spacer(1, 0.1*inch))
    
    # Build the PDF
    doc.build(elements)

def generate_pdf_background(data: ExportRequest) -> str:
    """Generate PDF in background and return the file path"""
    # Create directory if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "exports")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_name = "".join(c if c.isalnum() else "_" for c in data.patient_name)
    file_name = f"{data.assessment_type}_{sanitized_name}_{timestamp}.pdf"
    file_path = os.path.join(output_dir, file_name)
    
    try:
        if data.assessment_type == "speech_hearing":
            generate_pdf_for_speech_hearing(data.assessment_data, data.language, file_path)
        elif data.assessment_type == "movement":
            generate_pdf_for_movement(data.assessment_data, data.language, file_path)
        else:
            logging.error(f"Unknown assessment type: {data.assessment_type}")
            return None
            
        logging.info(f"Generated PDF report: {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"Error generating PDF: {e}")
        return None

@router.post("/export", response_model=ExportResponse)
async def export_assessment(data: ExportRequest, background_tasks: BackgroundTasks):
    """Export assessment results as PDF"""
    try:
        file_path = generate_pdf_background(data)
        
        if file_path:
            return ExportResponse(
                file_path=file_path,
                success=True,
                message="PDF report generated successfully"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate PDF report")
    except Exception as e:
        logging.error(f"Error in export endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

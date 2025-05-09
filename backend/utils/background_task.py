import time
from threading import Thread
from backend.ml_models.trend_analyzer import detect_bp_trend
from backend.ml_models.phq_trend_alert import detect_phq_trend
from backend.core.crud import get_all_patients_data
from backend.api.alerts_api import trigger_alert

def monitor_patient_data():
    """
    Background task to monitor patient data every 6 hours.
    Detects worsening trends and triggers alerts if thresholds are crossed.
    """
    while True:
        patients_data = get_all_patients_data()

        for patient in patients_data:
            # Check BP trends
            bp_trend = detect_bp_trend(patient['bp_data'])
            if bp_trend == "danger":
                trigger_alert(patient['id'], "Blood pressure is in a dangerous range.")

            # Check PHQ trends
            phq_trend = detect_phq_trend(patient['phq_data'])
            if phq_trend == "worsening":
                trigger_alert(patient['id'], "PHQ-9 score indicates worsening mental health.")

            # Add checks for Barthel and NIHSS trends if needed

        # Sleep for 6 hours
        time.sleep(6 * 60 * 60)

def start_background_task():
    """
    Start the background task in a separate thread.
    """
    task_thread = Thread(target=monitor_patient_data, daemon=True)
    task_thread.start()

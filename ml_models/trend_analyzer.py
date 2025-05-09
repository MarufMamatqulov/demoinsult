from typing import List, Dict
from sklearn.linear_model import LinearRegression
import numpy as np

def detect_bp_trend(daily_measurements: List[Dict[str, float]]) -> Dict[str, str]:
    """
    Detect abnormal trends in blood pressure.

    Args:
        daily_measurements (List[Dict[str, float]]): List of daily measurements with 'systolic' and 'diastolic'.

    Returns:
        Dict[str, str]: Status (Stable, Fluctuating, Rising, Danger) and warning if applicable.
    """
    systolic_values = [entry['systolic'] for entry in daily_measurements]
    diastolic_values = [entry['diastolic'] for entry in daily_measurements]
    days = np.arange(len(daily_measurements)).reshape(-1, 1)

    # Linear regression for trend detection
    model = LinearRegression()
    model.fit(days, systolic_values)
    systolic_trend = model.coef_[0]

    model.fit(days, diastolic_values)
    diastolic_trend = model.coef_[0]

    # Determine status
    if all(s > 140 and d > 90 for s, d in zip(systolic_values[-3:], diastolic_values[-3:])):
        status = "Danger"
        warning = "Blood pressure dangerously high for 3+ days. Seek medical attention."
    elif systolic_trend > 0.5 or diastolic_trend > 0.5:
        status = "Rising"
        warning = "Blood pressure is rising. Monitor closely."
    elif max(systolic_values) - min(systolic_values) > 20 or max(diastolic_values) - min(diastolic_values) > 10:
        status = "Fluctuating"
        warning = "Blood pressure is fluctuating. Check for irregularities."
    else:
        status = "Stable"
        warning = "Blood pressure is stable."

    return {"status": status, "warning": warning}

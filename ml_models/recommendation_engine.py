from typing import List

def get_recommendations(inputs: dict) -> List[str]:
    """
    Generate recommendations based on the provided inputs.

    Args:
        inputs (dict): A dictionary containing the latest assessment values, including BP, NIHSS, Barthel, and PHQ-9 levels.

    Returns:
        List[str]: A list of recommendations.
    """
    recommendations = []

    # High BP recommendation
    if inputs.get("bp", 0) > 140:
        recommendations.append("Shifokorga murojaat qiling")

    # Barthel score recommendation
    if inputs.get("barthel", 100) < 60:
        recommendations.append("Jismoniy reabilitatsiyani kuchaytirish kerak")

    # PHQ-9 level recommendation
    phq9_level = inputs.get("phq9_level", "None")
    if phq9_level in ["Moderate", "Moderately Severe", "Severe"]:
        recommendations.append("Psixologik maslahat tavsiya etiladi")

    return recommendations

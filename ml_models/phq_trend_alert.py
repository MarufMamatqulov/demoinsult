from typing import List

def detect_phq_trend(phq_scores: List[int]) -> str:
    """
    Detect trend in PHQ-9 scores.

    Args:
        phq_scores (List[int]): List of PHQ-9 scores.

    Returns:
        str: "stable", "worsening", or "improving".
    """
    if len(phq_scores) < 3:
        return "stable"  # Not enough data to determine trend

    # Compare the last three scores
    if phq_scores[-1] > phq_scores[-2] > phq_scores[-3]:
        return "worsening"
    elif phq_scores[-1] < phq_scores[-2] < phq_scores[-3]:
        return "improving"
    else:
        return "stable"

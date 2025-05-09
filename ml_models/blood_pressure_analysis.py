def analyze_blood_pressure(systolic: int, diastolic: int, correct_position: bool) -> str:
    """
    Analyze blood pressure readings and return a category.

    Parameters:
        systolic (int): Systolic blood pressure value.
        diastolic (int): Diastolic blood pressure value.
        correct_position (bool): Whether the position during measurement was correct.

    Returns:
        str: Blood pressure category (Normal, Elevated, Hypertension Stage 1, Hypertension Stage 2).
    """
    if not correct_position:
        return "Invalid reading: Position incorrect"

    if systolic < 120 and diastolic < 80:
        return "Normal"
    elif 120 <= systolic < 130 and diastolic < 80:
        return "Elevated"
    elif 130 <= systolic < 140 or 80 <= diastolic < 90:
        return "Hypertension Stage 1"
    elif systolic >= 140 or diastolic >= 90:
        return "Hypertension Stage 2"
    else:
        return "Uncategorized"

# Example usage
if __name__ == "__main__":
    print(analyze_blood_pressure(125, 75, True))  # Output: Elevated
    print(analyze_blood_pressure(135, 85, True))  # Output: Hypertension Stage 1
    print(analyze_blood_pressure(145, 95, True))  # Output: Hypertension Stage 2
    print(analyze_blood_pressure(115, 75, False))  # Output: Invalid reading: Position incorrect

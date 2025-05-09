import pytest
from ml_models.blood_pressure_analysis import analyze_blood_pressure

def test_normal_blood_pressure():
    assert analyze_blood_pressure(115, 75, True) == "Normal"

def test_elevated_blood_pressure():
    assert analyze_blood_pressure(125, 75, True) == "Elevated"

def test_hypertension_stage_1():
    assert analyze_blood_pressure(135, 85, True) == "Hypertension Stage 1"

def test_hypertension_stage_2():
    assert analyze_blood_pressure(145, 95, True) == "Hypertension Stage 2"

def test_invalid_position():
    assert analyze_blood_pressure(115, 75, False) == "Invalid reading: Position incorrect"

def test_uncategorized_blood_pressure():
    assert analyze_blood_pressure(121, 79, True) == "Uncategorized"

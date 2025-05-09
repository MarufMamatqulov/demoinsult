import pytest
from ml_models.phq_model import predict_phq_level

def test_predict_phq_level_normal():
    input_data = {f'q{i}': 1 for i in range(1, 10)}
    result = predict_phq_level(input_data)
    assert result == "Mild", f"Expected 'Mild', got {result}"

def test_predict_phq_level_severe():
    input_data = {f'q{i}': 3 for i in range(1, 10)}
    result = predict_phq_level(input_data)
    assert result == "Severe", f"Expected 'Severe', got {result}"

def test_predict_phq_level_extreme():
    input_data = {f'q{i}': 3 for i in range(1, 10)}
    result = predict_phq_level(input_data)
    assert result == "Severe", f"Expected 'Severe', got {result}"

def test_predict_phq_level_missing_input():
    input_data = {f'q{i}': 1 for i in range(1, 9)}  # Missing q9
    with pytest.raises(KeyError):
        predict_phq_level(input_data)

def test_predict_phq_level_invalid():
    input_data = {f'q{i}': 1 for i in range(1, 9)}  # Missing q9
    with pytest.raises(KeyError):
        predict_phq_level(input_data)

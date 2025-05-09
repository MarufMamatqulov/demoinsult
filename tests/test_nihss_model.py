import pytest
from ml_models.nihss_model import predict_nihss_severity
import joblib
import pandas as pd

@pytest.fixture(scope="module")
def load_model():
    return joblib.load('nihss_model.joblib')

def test_predict_nihss_severity(load_model):
    # Example input
    input_dict = {
        'nihs_1': 1.0, 'nihs_2': 0.0, 'nihs_3': 2.0, 'nihs_4': 1.0, 'nihs_5': 0.0,
        'nihs_6': 1.0, 'nihs_7': 0.0, 'nihs_8': 1.0, 'nihs_9': 0.0, 'nihs_10': 1.0, 'nihs_11': 0.0
    }

    # Convert input_dict to DataFrame
    input_df = pd.DataFrame([input_dict])

    # Predict severity
    prediction = load_model.predict(input_df)

    assert prediction[0] in ['mild', 'moderate', 'severe']

@pytest.mark.parametrize("input_data,expected", [
    ({'nihs_1': 0, 'nihs_2': 0, 'nihs_3': 0, 'nihs_4': 0, 'nihs_5': 0, 'nihs_6': 0, 'nihs_7': 0, 'nihs_8': 0, 'nihs_9': 0, 'nihs_10': 0, 'nihs_11': 0}, 'mild'),
    ({'nihs_1': 4, 'nihs_2': 4, 'nihs_3': 4, 'nihs_4': 4, 'nihs_5': 4, 'nihs_6': 4, 'nihs_7': 4, 'nihs_8': 4, 'nihs_9': 4, 'nihs_10': 4, 'nihs_11': 4}, 'severe')
])
def test_predict_nihss_severity_normal(input_data, expected):
    result = predict_nihss_severity(input_data)
    assert result == expected, f"Expected {expected}, got {result}"

def test_predict_nihss_severity_invalid():
    input_data = {'nihs_1': 0, 'nihs_2': 0, 'nihs_3': 0}  # Missing keys
    with pytest.raises(KeyError):
        predict_nihss_severity(input_data)

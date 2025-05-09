# PHQ-9 Model for Depression Prediction

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
import joblib

# Load and preprocess dataset
def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    X = data[[f'q{i}' for i in range(1, 10)]]
    y = data[[f'q{i}' for i in range(1, 10)]].sum(axis=1).apply(categorize_depression)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, scaler

def categorize_depression(score):
    if score <= 4:
        return "None"
    elif score <= 9:
        return "Mild"
    elif score <= 14:
        return "Moderate"
    else:
        return "Severe"

# Train model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))
    return model

# Save model
def save_model(model, scaler, file_path):
    joblib.dump({"model": model, "scaler": scaler}, file_path)

# Predict depression level
def predict_phq_level(input_dict):
    model_data = joblib.load("ml_models/phq_model.joblib")
    model = model_data["model"]
    scaler = model_data["scaler"]
    input_array = np.array([list(input_dict.values())]).reshape(1, -1)
    input_scaled = scaler.transform(input_array)
    prediction = model.predict(input_scaled)
    return prediction[0]

def analyze_phq9(answers: dict) -> str:
    """
    Analyze PHQ-9 answers and return the depression level.

    Args:
        answers (dict): Dictionary with keys q1 to q9, each value between 0 and 3.

    Returns:
        str: Depression level (Minimal, Mild, Moderate, Moderately severe, Severe).
    """
    # Calculate the total score
    total_score = sum(answers[f'q{i}'] for i in range(1, 10))

    # Determine the depression level based on the score
    if 0 <= total_score <= 4:
        return "Minimal"
    elif 5 <= total_score <= 9:
        return "Mild"
    elif 10 <= total_score <= 14:
        return "Moderate"
    elif 15 <= total_score <= 19:
        return "Moderately severe"
    elif 20 <= total_score <= 27:
        return "Severe"
    else:
        raise ValueError("Invalid PHQ-9 score")

if __name__ == "__main__":
    # Example CSV file path
    file_path = "data/Dataset_14-day_AA_depression_symptoms_mood_and_PHQ-9.csv/Dataset_14-day_AA_depression_symptoms_mood_and_PHQ-9.csv"
    X, y, scaler = load_and_preprocess_data(file_path)
    model = train_model(X, y)
    save_model(model, scaler, "ml_models/phq_model.joblib")

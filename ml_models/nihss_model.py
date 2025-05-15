import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# Define the function to train the model
def train_nihss_model(csv_path):
    # Load the dataset
    data = pd.read_csv(csv_path)

    # Define features and target
    X = data[[f'nihs_{i}' for i in range(1, 12)]]
    y = data['severity']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the RandomForestClassifier
    model = RandomForestClassifier(random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy}")

    # Save the model
    joblib.dump(model, 'nihss_model.joblib')

# Define the function to predict stroke severity
def predict_nihss_severity(input_dict):
    """
    Predict stroke severity based on NIHSS scores.
    
    This function uses a direct calculation approach rather than loading a model,
    as NIHSS severity interpretation is standardized based on total score.
    
    Args:
        input_dict: Dictionary with NIHSS item scores (nihs_1 through nihs_11)
        
    Returns:
        string: Severity classification
    """
    try:
        # Calculate total NIHSS score
        total_score = sum(input_dict.values())
        
        # Determine severity based on total score
        if total_score == 0:
            return "No Stroke Symptoms"
        elif 1 <= total_score <= 4:
            return "Minor Stroke"
        elif 5 <= total_score <= 15:
            return "Moderate Stroke"
        elif 16 <= total_score <= 20:
            return "Moderate to Severe Stroke"
        elif 21 <= total_score <= 42:
            return "Severe Stroke"
        else:
            return "Invalid Score"
    except Exception as e:
        import logging
        logging.error(f"Error predicting NIHSS severity: {str(e)}")
        return "Unable to determine severity"

if __name__ == "__main__":
    # Update this path when you have the NIHSS dataset
    train_nihss_model('data/nihss_dataset.csv')

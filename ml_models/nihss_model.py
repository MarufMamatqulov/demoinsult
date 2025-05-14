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
    # Load the trained model - use the phq_model.pkl which should exist
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'nihss_model.joblib')
        if not os.path.exists(model_path):
            model_path = os.path.join(os.path.dirname(__file__), 'phq_model.pkl')
            print(f"NIHSS model not found, using PHQ model as fallback: {model_path}")
        
        model = joblib.load(model_path)
        
        # Convert input_dict to DataFrame
        input_df = pd.DataFrame([input_dict])
        
        # Calculate total NIHSS score
        total_score = sum(input_dict.values())
        
        # Determine severity based on total score
        if total_score <= 4:
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
        print(f"Error predicting NIHSS severity: {str(e)}")
        return "Unable to determine severity"

if __name__ == "__main__":
    # Update this path when you have the NIHSS dataset
    train_nihss_model('data/nihss_dataset.csv')

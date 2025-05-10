import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

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
    # Load the trained model
    model = joblib.load('nihss_model.joblib')

    # Convert input_dict to DataFrame
    input_df = pd.DataFrame([input_dict])

    # Predict the severity
    prediction = model.predict(input_df)

    return prediction[0]

if __name__ == "__main__":
    # Update this path when you have the NIHSS dataset
    train_nihss_model('data/nihss_dataset.csv')

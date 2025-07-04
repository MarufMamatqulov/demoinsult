import joblib
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv("C:\\Users\\Marufjon\\Desktop\\InsultML\\data\\Dataset_14-day_AA_depression_symptoms_mood_and_PHQ-9.csv\\Dataset_14-day_AA_depression_symptoms_mood_and_PHQ-9.csv")

# Derive the target column as the sum of PHQ-9 scores
data['target'] = data[['phq1', 'phq2', 'phq3', 'phq4', 'phq5', 'phq6', 'phq7', 'phq8', 'phq9']].sum(axis=1)

# Prepare features and labels
X = data[['phq1', 'phq2', 'phq3', 'phq4', 'phq5', 'phq6', 'phq7', 'phq8', 'phq9']]
y = data['target']

# Handle missing values by filling with the mean of each column
X = X.fillna(X.mean())

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Update the save path to the ml_models directory
model_save_path = os.path.join(os.path.dirname(__file__), 'phq_model.pkl')

# Save the trained model
print("Attempting to save the model...")
try:
    joblib.dump(model, model_save_path)
    print(f"Model saved successfully as {model_save_path}")
except Exception as e:
    print(f"Error saving model: {e}")

# Explicitly confirm the file save operation
if os.path.exists(model_save_path):
    print(f"Model file saved successfully as {model_save_path}")
else:
    print("Error: Model file not saved correctly.")

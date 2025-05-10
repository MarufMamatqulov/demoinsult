import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load features and labels
angles = pd.read_csv('data/Physical Exercise Recognition Dataset/angles.csv')
labels = pd.read_csv('data/Physical Exercise Recognition Dataset/labels.csv')

# Merge on pose_id
merged = pd.merge(angles, labels, on='pose_id')

# Use all angle features for training
X = merged.drop(['pose_id', 'pose'], axis=1)
y = merged['pose']

# Train a simple classifier
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save the model
joblib.dump(model, 'ml_models/exercise_model.joblib')
print('Exercise model trained and saved as ml_models/exercise_model.joblib')

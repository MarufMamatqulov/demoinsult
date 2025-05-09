# Stroke Rehabilitation AI Platform

## Purpose
The Stroke Rehabilitation AI Platform is designed to assist healthcare professionals in monitoring and improving patient recovery. It integrates advanced machine learning models and user-friendly interfaces to analyze patient data, detect trends, and provide actionable insights.

## Technologies Used
- **Backend**: Python, FastAPI, SQLAlchemy
- **Frontend**: React, Tailwind CSS
- **Machine Learning**: OpenAI Whisper, MediaPipe, Scikit-learn
- **Database**: PostgreSQL (optional)
- **Containerization**: Docker, Docker Compose

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd InsultML
   ```
2. Install dependencies:
   - Backend:
     ```bash
     pip install -r requirements.txt
     ```
   - Frontend:
     ```bash
     cd frontend
     npm install
     ```
3. Run the application:
   - Backend:
     ```bash
     uvicorn backend.main:app --reload
     ```
   - Frontend:
     ```bash
     cd frontend
     npm start
     ```
4. Alternatively, use Docker:
   ```bash
   docker-compose up --build
   ```

## API Endpoints Overview
- **PHQ-9 Analysis**: `/phq/analyze`
- **Blood Pressure Analysis**: `/alerts/analyze-bp`
- **Stroke Severity Prediction**: `/nihss/predict`
- **Exercise Video Analysis**: `/video/analyze`
- **Audio Analysis**: `/audio/analyze`
- **PDF Report Generation**: `/report/pdf/{patient_id}`
- **Recommendations**: `/recommendations/generate`

## How to Run with Docker
1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
2. Access the frontend at `http://localhost:3000` and the backend at `http://localhost:8000`.

## Contribution
Feel free to contribute by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.
# Stroke Rehabilitation AI Platform

## Purpose
The Stroke Rehabilitation AI Platform is designed to assist healthcare professionals in monitoring and improving patient recovery. It integrates advanced machine learning models and user-friendly interfaces to analyze patient data, detect trends, and provide actionable insights.

## Technologies Used
- **Backend**: Python, FastAPI, SQLAlchemy
- **Frontend**: React, Tailwind CSS
- **Machine Learning**: OpenAI (GPT-4o, Whisper), MediaPipe, Scikit-learn
- **Database**: PostgreSQL (optional)
- **Containerization**: Docker, Docker Compose

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd InsultML
   ```
2. Set up environment variables:
   - Copy the `.env.template` file to `.env` and update with your configuration:
     ```bash
     cp .env.template .env
     # Edit .env with your settings
     ```

3. Install dependencies:
   - Backend:
     ```bash
     pip install -r requirements.txt
     ```
   - Frontend:
     ```bash
     cd frontend
     npm install
     ```
4. Run the application:
   - Backend:
     ```bash
     uvicorn backend.main:app --reload
     ```
   - Frontend:
     ```bash
     cd frontend
     npm start
     ```
5. Alternatively, use Docker:
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
- **AI Rehabilitation Analysis**: `/ai/rehabilitation/analysis`
- **AI Chat Completion**: `/ai/chat/completion`

## How to Run with Docker
1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
2. Access the frontend at `http://localhost:3000` and the backend at `http://localhost:8000`.

## Features

### AI-Powered Rehabilitation Analysis
- **Assessment Analysis**: Get AI-driven insights from assessment forms
- **Multilingual Support**: Available in English, Russian, and Uzbek
- **Smart Recommendations**: Personalized rehabilitation advice based on assessment results

### Rehabilitation Exercises
- **Video Exercises**: Curated collection of stroke rehabilitation exercise videos
- **Articles**: Informative articles about stroke recovery in multiple languages
- **Cognitive Exercises**: Memory and speech improvement resources

### Quick Start
For an easier start, use our startup scripts:
- Windows: `.\start.ps1`
- Linux/macOS: `./start.sh`

## Documentation
Additional documentation can be found in the `docs` directory:
- [Architecture Overview](docs/architecture.md)
- [OpenAI Integration](docs/openai_integration.md)

## Contribution
Feel free to contribute by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Verification Scripts

The following scripts are available to verify the platform's functionality:

1. **Assessment History Verification**:
   ```bash
   .\verify-assessment-history.ps1
   ```
   Verifies that the assessment history endpoints are working correctly.

2. **Email Configuration Verification**:
   ```bash
   .\verify-email-configuration.ps1
   ```
   Tests the email configuration and sends a test email.

3. **OpenAI Integration Verification**:
   ```bash
   .\verify-openai-integration.ps1
   ```
   Verifies that the OpenAI integration is working correctly.

4. **Comprehensive Verification**:
   ```bash
   .\verify-all-fixes.ps1
   ```
   Runs all verification scripts and generates a comprehensive report.

## Documentation

Detailed documentation is available in the following files:

- `FIXES_DOCUMENTATION.md` - Detailed documentation of all fixes implemented
- `FINAL_VERIFICATION_SUMMARY.md` - Summary of verification results
- `EMAIL_CONFIGURATION_GUIDE.md` - Guide for configuring email settings
- `ASSESSMENT_HISTORY_VERIFICATION_RESULTS.md` - Results of assessment history endpoint testing
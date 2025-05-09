# Stroke Rehabilitation AI Platform Documentation

## Architecture Overview
The Stroke Rehabilitation AI Platform is designed to assist in post-stroke rehabilitation using AI-driven analysis and monitoring. The system is divided into the following components:

1. **Frontend**: A React-based user interface for interacting with the platform.
   - Location: `frontend/`
   - Key Components: `PhqForm.tsx`, `Results.tsx`

2. **Backend**: A FastAPI-based server for handling API requests and running machine learning models.
   - Location: `backend/`
   - Key Modules:
     - `api/`: Contains API endpoints (e.g., `phq9.py` for PHQ-9 analysis).
     - `core/`: Configuration and database connection.
     - `schemas/`: Pydantic models for request/response validation.

3. **Machine Learning Models**: Pre-trained models for analyzing PHQ-9 responses and other health metrics.
   - Location: `ml_models/`
   - Key File: `phq_model.py`

4. **Data**: Contains CSV datasets used for training and analysis.
   - Location: `data/`

5. **Tests**: Unit and integration tests for the backend and ML models.
   - Location: `tests/`

6. **Deployment**: Docker and GitHub Actions for containerization and CI/CD.
   - Files: `Dockerfile.backend`, `Dockerfile.frontend`, `docker-compose.yml`, `.github/workflows/ci-cd.yml`

---

## API Usage

### Health Check
- **Endpoint**: `/health`
- **Method**: GET
- **Response**: `{ "status": "ok" }`

### PHQ-9 Analysis
- **Endpoint**: `/phq/analyze`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "q1": 1,
    "q2": 2,
    "q3": 3,
    "q4": 1,
    "q5": 2,
    "q6": 3,
    "q7": 1,
    "q8": 2,
    "q9": 3
  }
  ```
- **Response**:
  ```json
  {
    "prediction": "Moderate"
  }
  ```
- **Error Response**:
  ```json
  {
    "error": "Invalid input"
  }
  ```

---

## ML Model Behavior

### PHQ-9 Model
- **Purpose**: Classifies depression levels based on PHQ-9 responses.
- **Input**: 9 integer values (0–3) representing PHQ-9 question responses.
- **Output**: Depression level (`None`, `Mild`, `Moderate`, `Severe`).
- **Implementation**:
  - Preprocessing: Standard scaling of inputs.
  - Model: RandomForestClassifier.
  - Location: `ml_models/phq_model.py`

### Example Usage
```python
from ml_models.phq_model import predict_phq_level

input_data = {"q1": 1, "q2": 2, "q3": 3, "q4": 1, "q5": 2, "q6": 3, "q7": 1, "q8": 2, "q9": 3}
result = predict_phq_level(input_data)
print(result)  # Output: "Moderate"
```

---

## User Guide

### Running the System
1. **Backend**:
   - Build and run using Docker:
     ```bash
     docker-compose up --build backend
     ```
   - Access the API at `http://localhost:8000`.

2. **Frontend**:
   - Build and run using Docker:
     ```bash
     docker-compose up --build frontend
     ```
   - Access the UI at `http://localhost:3000`.

### Using the PHQ-9 Form
1. Open the frontend in your browser.
2. Fill in the PHQ-9 form by adjusting the sliders for each question.
3. Click the **Submit** button.
4. View the predicted depression level in the result box.

### Running Tests
- Run backend and ML model tests using Pytest:
  ```bash
  pytest tests/
  ```

---

For further details, refer to the individual module documentation or contact the development team.

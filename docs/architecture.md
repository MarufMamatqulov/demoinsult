# System Architecture

## Overview
The Stroke Rehabilitation AI Platform is designed with a modular architecture to ensure scalability, maintainability, and ease of integration. Below is the system diagram and a detailed description of its components.

## System Diagram
```
+-------------------+       +-------------------+       +-------------------+
|   Frontend (UI)   | <-->  |   API Gateway     | <-->  |   Database (DB)   |
+-------------------+       +-------------------+       +-------------------+
         |                          |                          |
         v                          v                          v
+-------------------+       +-------------------+       +-------------------+
| Audio Analysis    |       | Video Analysis    |       | ML Models         |
| (Whisper)         |       | (MediaPipe)       |       | (PHQ, NIHSS, etc.)|
+-------------------+       +-------------------+       +-------------------+
```

## Modular Structure
1. **Frontend**:
   - Built with React and Tailwind CSS.
   - Provides user-friendly interfaces for doctors and caregivers.
   - Role-based access control for different user types.

2. **API Gateway**:
   - Built with FastAPI.
   - Handles requests from the frontend and routes them to appropriate services.
   - Includes endpoints for PHQ-9 analysis, BP trend detection, audio/video analysis, and more.

3. **Database**:
   - Stores patient data, assessment histories, and user information.
   - Optional: PostgreSQL for production environments.

4. **Machine Learning Services**:
   - **Audio Analysis**: Uses OpenAI Whisper to transcribe and analyze speech patterns.
   - **Video Analysis**: Uses MediaPipe to evaluate exercise movements.
   - **PHQ-9 and NIHSS Models**: Predicts mental health and stroke severity.

## User Roles
- **Doctor**:
  - Access to all patient data and reports.
  - Can generate PDF reports and view trends.
- **Caregiver**:
  - Limited access to patient data.
  - Can view alerts and recommendations.

## Machine Learning Usage
- **Whisper**: For audio transcription and cognitive analysis.
- **MediaPipe**: For video-based exercise evaluation.
- **Custom Models**: For PHQ-9 trend detection, BP analysis, and NIHSS predictions.

## Future Enhancements
- Integration with wearable devices for real-time data.
- Advanced analytics dashboards.
- Support for additional languages and regions.
# InsultMedAI Quick Start Guide

This guide provides step-by-step instructions for getting started with InsultMedAI, a stroke rehabilitation platform with AI-powered assessment tools.

## Local Development Setup

### Prerequisites

- Node.js (v16+)
- Python 3.8+
- OpenAI API key

### Step 1: Set Up the Backend

1. Clone the repository (if you haven't already):
   ```bash
   git clone https://github.com/yourusername/InsultMedAI.git
   cd InsultMedAI
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. Start the backend server:
   ```bash
   # Windows (PowerShell)
   .\start.ps1

   # Linux/Mac
   ./start.sh
   ```

   Alternatively, you can run:
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```

6. The API should now be running at http://localhost:8000

### Step 2: Set Up the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.development` file:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm start
   ```

5. The frontend application should now be running at http://localhost:3000

## Using the Application

### PHQ-9 Assessment

1. Navigate to the PHQ-9 page
2. Fill out the questionnaire
3. Submit for analysis
4. View the results and recommendations

### Blood Pressure Analysis

1. Navigate to the Blood Pressure page
2. Enter blood pressure readings
3. Submit for analysis
4. View the categorization and recommendations

### NIHSS Assessment

1. Navigate to the NIHSS page
2. Complete the assessment form
3. Submit for analysis
4. View the results and recommendations

### Audio Analysis

1. Navigate to the Audio Assessment page
2. Upload an audio recording or record directly
3. Submit for analysis
4. View the speech assessment results

### Video Analysis

1. Navigate to the Video Assessment page
2. Upload a video recording
3. Submit for analysis
4. View the movement assessment results

## Troubleshooting

### Backend Issues

- **API not responding**: Check if the backend server is running
- **Import errors**: Make sure all dependencies are installed
- **OpenAI API errors**: Verify your API key is correct

### Frontend Issues

- **API connection errors**: Check if the backend server is running and CORS is configured correctly
- **Component errors**: Check browser console for specific errors
- **Styling issues**: Make sure all CSS dependencies are loaded

## Getting Help

For additional help:
- Check the documentation in the `docs` folder
- Refer to the `DEPLOYMENT_GUIDE.md` for deployment instructions
- Use the `api_test.js` script to test the API functionality

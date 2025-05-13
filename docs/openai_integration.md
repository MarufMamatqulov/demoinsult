# OpenAI Integration for Stroke Rehabilitation AI Platform

This document describes how the OpenAI API is integrated into our Stroke Rehabilitation AI Platform to provide personalized rehabilitation recommendations and AI-powered assistance.

## Overview

The integration uses OpenAI's GPT-4o model to analyze assessment data and provide:

1. **Rehabilitation Analysis**: Assessment-specific analysis and recommendations based on form data
2. **Chat Functionality**: Interactive conversation to answer patient questions about their rehabilitation
3. **Personalized Recommendations**: Tailored suggestions based on assessment results

## Setup

### Prerequisites

- OpenAI API key (set in `.env` file)
- Python 3.8+ with FastAPI
- Required Python packages (see `requirements.txt`)

### Environment Configuration

1. Copy the `.env.example` file to `.env`
2. Add your OpenAI API key in the `.env` file:
   ```
   OPENAI_API_KEY="your-api-key-goes-here"
   ```

## API Endpoints

The application exposes two main API endpoints for AI assistance:

### 1. Rehabilitation Analysis

**Endpoint:** `/ai/rehabilitation/analysis`  
**Method:** POST  
**Purpose:** Analyze assessment data and provide recommendations

**Request Example:**

```json
{
  "assessment_data": {
    "q1": 2,
    "q2": 1,
    "q3": 3,
    "q4": 2
  },
  "assessment_type": "phq9",
  "language": "en"
}
```

**Response Example:**

```json
{
  "response": "Based on the PHQ-9 assessment data provided, the patient shows signs of moderate depression with a score of 8...",
  "recommendations": [
    "Consider regular physical activity, which has been shown to reduce depression symptoms",
    "Maintain a consistent sleep schedule to improve mood regulation",
    "Consider consultation with a mental health professional for further evaluation"
  ]
}
```

### 2. Chat Completion

**Endpoint:** `/ai/chat/completion`  
**Method:** POST  
**Purpose:** Enable conversations with the AI assistant about rehabilitation

**Request Example:**

```json
{
  "messages": [
    {"role": "user", "content": "What exercises can help improve my hand mobility after stroke?"}
  ],
  "language": "en",
  "context": {
    "assessment_type": "movement",
    "assessment_data": {"upper_limb_score": 3}
  }
}
```

**Response Example:**

```json
{
  "response": "Based on your limited hand mobility, here are some gentle exercises that might help: 1. Finger tapping - tap each finger to your thumb slowly and with control. 2. Wrist rotation - gently rotate your wrist in circles, both clockwise and counterclockwise..."
}
```

## Supported Languages

The AI integration supports the following languages:
- English (en)
- Russian (ru)
- Uzbek (uz)

## Assessment Types

The system is optimized for the following assessment types:
- `nihss`: Stroke severity assessment
- `phq9`: Depression assessment
- `movement`: Physical movement capability assessment
- `speech`: Speech and communication assessment
- `blood_pressure`: Blood pressure monitoring

## Frontend Integration

The frontend uses the `AIRecommendations` React component to display AI-powered analysis and recommendations. This component:

1. Connects to the backend API endpoints
2. Displays loading states during API calls
3. Renders recommendations in a user-friendly format
4. Allows users to ask follow-up questions
5. Supports multilingual content

## Best Practices

1. **Keep sensitive data secure** - Never log or expose the OpenAI API key
2. **Handle API rate limits** - Implement proper error handling for API limits
3. **Monitor usage** - Track API usage to manage costs
4. **Validate responses** - Ensure AI responses are appropriate before displaying

## Troubleshooting

Common issues and solutions:

1. **API key errors**
   - Check that the API key is correctly set in the `.env` file
   - Verify that the dotenv package is properly loading the environment variables

2. **Connection errors**
   - Check network connectivity
   - Verify that the backend server is running

3. **Response errors**
   - Check that the assessment data is properly formatted
   - Verify that the assessment type is one of the supported types

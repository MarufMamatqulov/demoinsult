# API Endpoint Fixes

## Issues Fixed

### 1. Assessment History Endpoint (500 Error)

The issue with the assessments/history endpoint that was returning 500 errors with "'list' object has no attribute 'get'" has been fixed. The problem was that the endpoint was directly returning SQLAlchemy ORM objects, which were being converted to a list when being serialized. This caused issues when the Pydantic model tried to access attributes.

**Fix:** The endpoints now explicitly convert the SQLAlchemy ORM objects to dictionaries that match the Pydantic schema structure, ensuring proper serialization.

Files modified:
- `backend/api/assessment_history.py`

Changes:
- Updated the `/history` endpoint to properly convert Assessment objects to dictionaries
- Updated the `/{assessment_id}` endpoint to properly convert Assessment objects to dictionaries
- Updated the POST endpoint to properly convert the created Assessment object to a dictionary

### 2. OpenAI API Version Compatibility Issue

The OpenAI API integration was using the older API format (`openai.ChatCompletion.create`) which is no longer supported in OpenAI Python library versions >= 1.0.0.

**Fix:** Created a compatibility layer that supports both the old and new OpenAI API formats.

Files created/modified:
- Created `backend/utils/openai_helper.py` - A helper module that handles the OpenAI API version differences
- Updated `backend/api/openai_integration.py` to use the helper module

Changes:
- Added version detection to automatically use the appropriate API format
- Simplified the code in the API endpoints by using a common helper function
- Improved error handling for API calls

## Testing

To test these fixes:

1. Assessment History Endpoint:
   - Make a GET request to `/assessments/history`
   - Make a GET request to `/assessments/{id}` for a specific assessment
   - Create a new assessment with a POST request to `/assessments/`

2. OpenAI Integration:
   - Test the chat functionality in the application
   - Make a POST request to `/openai/chat/completion` with appropriate message format
   - Make a POST request to `/openai/rehabilitation/analysis` with assessment data

## Notes

- The fixes maintain backward compatibility with existing code
- Error handling has been improved to provide more meaningful error messages
- These changes should resolve the 500 errors reported in the logs

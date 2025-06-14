# Assessment History Verification Guide

This guide outlines the steps to verify and fix the assessment history endpoints in the Stroke Rehabilitation AI Platform.

## Background

The assessment history endpoints were returning 500 errors with the message "'list' object has no attribute 'get'". This was likely caused by improper serialization of SQLAlchemy ORM objects.

## Verification Results

Our verification process identified several issues:

1. **Authentication Issues**:
   - The `/auth/login` endpoint returns a 500 internal server error
   - Even manually generated JWT tokens resulted in 401 Unauthorized errors on assessment endpoints
   - The same token works for the `/health` endpoint but not for assessment history

2. **Connection Issues**:
   - Python tests experience "Connection broken: IncompleteRead" errors
   - This suggests response handling problems

## Recommended Fixes

### 1. Fix Authentication

The authentication system needs to be fixed to properly validate JWT tokens:

```python
# In backend/core/auth.py

def decode_access_token(token):
    """
    Decode and validate a JWT access token with better error handling.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            logging.error("Token missing 'sub' claim")
            raise JWTError("Missing subject claim")
        return payload
    except JWTError as e:
        logging.error(f"JWT Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logging.error(f"Unexpected error decoding token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication error",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

### 2. Fix Assessment History Endpoints

Update the assessment history endpoints to properly handle serialization:

```python
# In backend/api/assessment_history.py

@router.get("/history")
async def get_user_assessments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = None
):
    """Get all assessment records for the current user."""
    try:
        query = db.query(Assessment).filter(Assessment.user_id == current_user.id).order_by(Assessment.created_at.desc())
        
        if limit:
            query = query.limit(limit)
            
        assessments = query.all()
        
        # Convert each assessment to a dict explicitly
        result = []
        for assessment in assessments:
            try:
                assessment_dict = convert_assessment_to_dict(assessment)
                result.append(assessment_dict)
            except Exception as e:
                logging.error(f"Error converting assessment {assessment.id}: {str(e)}")
                # Include a minimal valid version of the assessment
                result.append({
                    "id": assessment.id,
                    "user_id": assessment.user_id,
                    "type": assessment.type,
                    "data": {},
                    "created_at": str(assessment.created_at) if assessment.created_at else None,
                    "updated_at": str(assessment.updated_at) if assessment.updated_at else None
                })
        
        # Use JSONResponse directly
        return JSONResponse(content=result)
    except Exception as e:
        logging.error(f"Error processing assessment history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing assessment history: {str(e)}"
        )
```

### 3. Improve Connection Handling

Add middleware to properly handle Content-Length headers:

```python
# In backend/main.py

class ContentLengthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # Check if it's a regular response with a body
        if hasattr(response, "body") and isinstance(response.body, bytes):
            # Update Content-Length header to match actual body size
            response.headers["Content-Length"] = str(len(response.body))
        
        # Special handling for StreamingResponse
        if isinstance(response, StreamingResponse):
            # For streaming responses, we should avoid setting Content-Length
            # since the exact size may not be known in advance
            if "Content-Length" in response.headers:
                del response.headers["Content-Length"]
        
        return response

# Add middleware to FastAPI app
app.add_middleware(ContentLengthMiddleware)
```

## Verification Steps

1. **Create a test user**:
   ```bash
   python tests/create_test_user_direct.py
   ```

2. **Generate a JWT token for testing**:
   ```bash
   python tests/generate_test_token.py
   ```

3. **Test the health endpoint with the token**:
   ```bash
   $token = Get-Content test_token.txt
   Invoke-WebRequest -Uri "http://localhost:8000/health" -Headers @{Authorization = "Bearer $token"} -Method GET
   ```

4. **Test the assessment history endpoint**:
   ```bash
   $token = Get-Content test_token.txt
   Invoke-WebRequest -Uri "http://localhost:8000/assessments/history" -Headers @{Authorization = "Bearer $token"} -Method GET
   ```

5. **Run the verification script**:
   ```bash
   python tests/direct_token_verification.py
   ```

## Troubleshooting

If you're still encountering issues:

1. Check for authentication errors in the server logs
2. Verify the JWT secret key is consistent throughout the application
3. Test creating a new assessment to see if the endpoint works correctly
4. Consider resetting the database and creating a fresh test user

## Conclusion

Once these fixes are implemented, the assessment history endpoints should work correctly, providing users with their assessment history and allowing the creation and management of assessments.

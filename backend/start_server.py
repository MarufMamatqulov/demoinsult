import os
import uvicorn
from dotenv import load_dotenv
from sqlalchemy import inspect
from backend.core.config import engine, Base

# Load environment variables
load_dotenv()

# Create database tables if they don't exist
inspector = inspect(engine)
if not inspector.has_table("users"):
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
else:
    print("Database tables already exist")

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8001"))  # Use port 8001 instead
    print(f"Starting server on {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=False)

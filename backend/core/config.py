from pydantic_settings import BaseSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"

settings = Settings()

# Database configuration
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL  # Update this URL for your database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

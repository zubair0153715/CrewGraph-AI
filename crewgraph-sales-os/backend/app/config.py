"""
Configuration settings for CrewGraph Sales OS
"""
import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "CrewGraph Sales OS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/crewgraph.db"  # Default to SQLite for dev
    # For production: postgresql://user:pass@host:5432/dbname
    
    # Vector DB (Qdrant)
    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None
    QDRANT_COLLECTION: str = "sales_memory"
    
    # AI/LLM
    GROQ_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    LLM_MODEL: str = "llama3-70b-8192"  # Groq's Llama3 70B (free)
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Email Configuration
    GMAIL_CLIENT_ID: Optional[str] = None
    GMAIL_CLIENT_SECRET: Optional[str] = None
    GMAIL_REDIRECT_URI: str = "http://localhost:8000/auth/gmail/callback"
    SMTP_HOST: Optional[str] = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Sending Limits
    DAILY_EMAIL_LIMIT: int = 100  # Start conservative
    EMAIL_BATCH_SIZE: int = 10
    
    # Scraping
    PLAYWRIGHT_HEADLESS: bool = True
    REQUEST_TIMEOUT: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://yourdomain.com",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

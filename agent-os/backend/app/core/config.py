from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://agentos:agentos_password@localhost:5432/agentos"
    
    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None
    
    # AI Providers
    OPENROUTER_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    DEFAULT_MODEL: str = "openai/gpt-4-turbo-preview"
    
    # JWT
    JWT_SECRET_KEY: str = "change-this-secret-key-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Browser Automation
    BROWSER_USE_API_KEY: Optional[str] = None
    PLAYWRIGHT_BROWSERS_PATH: str = "/tmp/browsers"
    
    # Docker Sandbox
    DOCKER_SANDBOX_ENABLED: bool = True
    SANDBOX_TIMEOUT: int = 300
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Feature Flags
    ENABLE_YOUTUBE_AUTOMATION: bool = False
    ENABLE_CODE_EXECUTION: bool = True
    ENABLE_BROWSER_AUTOMATION: bool = True
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def llm_provider(self) -> str:
        """Determine which LLM provider to use based on available keys"""
        if self.OPENROUTER_API_KEY:
            return "openrouter"
        elif self.OPENAI_API_KEY:
            return "openai"
        elif self.GROQ_API_KEY:
            return "groq"
        else:
            raise ValueError("No LLM API key configured")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, validator

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Microservice"
    PROJECT_DESCRIPTION: str = "A FastAPI microservice with proper configuration"
    VERSION: str = "0.2.0"
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:8000", "http://localhost:3000"]
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Admin User Settings
    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"  # Change in production
    
    # Use SettingsConfigDict for proper .env file configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

# Create global settings object
settings = Settings() 
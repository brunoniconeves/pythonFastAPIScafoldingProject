from typing import Dict

from pydantic import BaseModel, ConfigDict


class HealthCheck(BaseModel):
    """Response model for health check endpoint"""

    status: str
    version: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"status": "ok", "version": "0.1.0"}}
    )


class ConfigSettings(BaseModel):
    """Model for current settings in the config response"""

    version: str
    project_name: str
    database_url: str


class ConfigResponse(BaseModel):
    """Response model for config endpoint"""

    env_file_exists: bool
    env_file_contents: Dict[str, str]
    current_settings: ConfigSettings

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "env_file_exists": True,
                "env_file_contents": {
                    "PROJECT_NAME": "FastAPI Microservice",
                    "DATABASE_URL": "sqlite:///./test.db",
                },
                "current_settings": {
                    "version": "0.1.0",
                    "project_name": "FastAPI Microservice",
                    "database_url": "sqlite:///./test.db",
                },
            }
        }
    )

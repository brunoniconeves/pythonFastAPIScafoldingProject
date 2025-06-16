import os

from dotenv import dotenv_values
from fastapi import APIRouter, status

from app.core.config import settings
from app.schemas.system import ConfigResponse, HealthCheck

router = APIRouter(
    prefix="/system",
    tags=["system"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)


@router.get(
    "/health",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
    summary="System Health Check",
    description="Returns the current health status of the system and its version.",
)
def healthcheck():
    """
    Perform a health check of the system.

    Returns:
        - status: Current status of the system ("ok" if running)
        - version: Current version of the application
    """
    return {"status": "ok", "version": settings.VERSION}


@router.get(
    "/config",
    response_model=ConfigResponse,
    status_code=status.HTTP_200_OK,
    summary="System Configuration",
    description=(
        "Returns the current system configuration including environment "
        "variables and settings."
    ),
    response_description="Current system configuration and environment settings.",
)
def get_config():
    """
    Retrieve the current system configuration.

    This endpoint provides:
    - Environment file status
    - Current environment variables (from .env file)
    - Active system settings

    Note: Sensitive values may be redacted in production.

    Returns:
        - env_file_exists: Whether a .env file is present
        - env_file_contents: Contents of the .env file if it exists
        - current_settings: Active configuration settings
    """
    # Read .env file directly
    env_values = dotenv_values(".env") if os.path.exists(".env") else {}

    return {
        "env_file_exists": os.path.exists(".env"),
        "env_file_contents": env_values,
        "current_settings": {
            "version": settings.VERSION,
            "project_name": settings.PROJECT_NAME,
            "database_url": settings.DATABASE_URL,
        },
    }

from fastapi import status

from app.core.config import Settings, settings


def test_get_config(client):
    """
    Test the config endpoint returns:
    - 200 status code
    - Correct response structure
    - Valid settings values
    """
    response = client.get(f"{settings.API_V1_STR}/system/config")

    # Check status code
    assert response.status_code == status.HTTP_200_OK

    # Check response structure
    data = response.json()
    assert isinstance(data, dict)
    assert "env_file_exists" in data
    assert "env_file_contents" in data
    assert "current_settings" in data

    # Check current_settings structure and values
    current_settings = data["current_settings"]
    assert isinstance(current_settings, dict)
    assert current_settings["version"] == settings.VERSION
    assert current_settings["project_name"] == settings.PROJECT_NAME
    assert current_settings["database_url"] == settings.DATABASE_URL


def test_config_response_headers(client):
    """
    Test that the config endpoint returns proper headers:
    - Content-Type: application/json
    """
    response = client.get(f"{settings.API_V1_STR}/system/config")
    assert response.headers["content-type"] == "application/json"


def test_config_env_file_contents(client, tmp_path):
    """
    Test that the config endpoint correctly reports .env file status
    and contents when no .env file exists
    """
    response = client.get(f"{settings.API_V1_STR}/system/config")
    data = response.json()

    # Since we're in a test environment, there might not be a .env file
    if not data["env_file_exists"]:
        assert data["env_file_contents"] == {}


def test_config_with_env_file(client, test_env_file):
    """
    Test that the config endpoint correctly reads and reports
    the contents of a .env file when one exists
    """
    response = client.get(f"{settings.API_V1_STR}/system/config")
    data = response.json()

    # Check that the .env file was detected
    assert data["env_file_exists"] is True

    # Check that env file contents were read
    env_contents = data["env_file_contents"]
    assert isinstance(env_contents, dict)
    assert "PROJECT_NAME" in env_contents
    assert "DATABASE_URL" in env_contents
    assert "VERSION" in env_contents

    # Check specific values
    assert env_contents["PROJECT_NAME"] == "FastAPI Microservice"
    assert env_contents["DATABASE_URL"] == "sqlite:///./test.db"
    assert env_contents["VERSION"] == "0.2.0"


def test_cors_settings():
    """Test that CORS settings are properly configured."""
    settings = Settings()
    assert isinstance(settings.BACKEND_CORS_ORIGINS, list)
    assert "http://localhost:8000" in settings.BACKEND_CORS_ORIGINS
    assert "http://localhost:3000" in settings.BACKEND_CORS_ORIGINS
    # Check for value equality, not object identity
    settings2 = Settings()
    assert settings.BACKEND_CORS_ORIGINS == settings2.BACKEND_CORS_ORIGINS

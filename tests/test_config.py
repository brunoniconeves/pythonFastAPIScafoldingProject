from fastapi import status
from app.core.config import settings

def test_get_config(test_app):
    """
    Test the config endpoint returns:
    - 200 status code
    - Correct response structure
    - Valid settings values
    """
    response = test_app.get(f"{settings.API_V1_STR}/system/config")
    
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

def test_config_response_headers(test_app):
    """
    Test that the config endpoint returns proper headers:
    - Content-Type: application/json
    """
    response = test_app.get(f"{settings.API_V1_STR}/system/config")
    assert response.headers["content-type"] == "application/json"

def test_config_env_file_contents(test_app, tmp_path):
    """
    Test that the config endpoint correctly reports .env file status
    and contents when no .env file exists
    """
    response = test_app.get(f"{settings.API_V1_STR}/system/config")
    data = response.json()
    
    # Since we're in a test environment, there might not be a .env file
    if not data["env_file_exists"]:
        assert data["env_file_contents"] == {}

def test_config_with_env_file(test_app, test_env_file):
    """
    Test that the config endpoint correctly reads and reports
    the contents of a .env file when one exists
    """
    response = test_app.get(f"{settings.API_V1_STR}/system/config")
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
    assert env_contents["PROJECT_NAME"] == "Test FastAPI Project"
    assert env_contents["DATABASE_URL"] == "sqlite:///./test_db.db"
    assert env_contents["VERSION"] == "0.1.0-test" 
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.models.user import User

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture
def test_db():
    """
    Create a fresh test database for each test.
    """
    # Create test database engine
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create test database session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    try:
        yield engine
    finally:
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_app(test_db):
    """
    Create a fresh test client for each test.
    This gives us an isolated test environment.
    """
    client = TestClient(app)
    return client

@pytest.fixture
def app_settings():
    """
    Provide access to application settings in tests
    """
    return settings

@pytest.fixture
def test_env_file(tmp_path):
    """
    Create a temporary .env file for testing.
    The file will be automatically cleaned up after the test.
    """
    # Save current working directory
    original_cwd = os.getcwd()
    
    # Create a temporary .env file
    env_content = """
    PROJECT_NAME="Test FastAPI Project"
    DATABASE_URL="sqlite:///./test_db.db"
    VERSION="0.1.0-test"
    """
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    
    # Change to temp directory
    os.chdir(tmp_path)
    
    yield env_file
    
    # Clean up: restore original working directory
    os.chdir(original_cwd)

@pytest.fixture
def sample_user():
    """
    Return sample user data for testing
    """
    return {
        "name": "Test User",
        "email": "test@example.com"
    } 
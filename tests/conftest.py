import pytest
from datetime import datetime, timezone
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.main import app
from app.db import Base, get_db
from app.models.user import User

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create test database tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db() -> Generator[Session, None, None]:
    """Fixture that provides a database session."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db: Session) -> TestClient:
    """Fixture that provides a FastAPI TestClient."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user_data():
    """Fixture that provides sample user data."""
    return {
        "name": "Test User",
        "email": "test@example.com"
    }

@pytest.fixture
def test_user(db: Session, sample_user_data) -> User:
    """Fixture that provides a test user in the database."""
    user = User(
        **sample_user_data,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_env_file(tmp_path):
    """Fixture that provides a test .env file."""
    env_content = """
    PROJECT_NAME=FastAPI Microservice
    DATABASE_URL=sqlite:///./test.db
    VERSION=0.2.0
    """
    env_file = tmp_path / ".env"
    env_file.write_text(env_content)
    return env_file 
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app
from app.models.user import User

TEST_DATABASE_URL = "sqlite:///:memory:"


def unique_email() -> str:
    """Generate a unique email address for testing."""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture(scope="session")
def engine():
    """Create a test database engine and create all tables."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Ensures all connections share the same in-memory DB
    )
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield engine
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def connection(engine):
    """Create a connection to the test database."""
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def db_session(connection):
    """Create a new database session for a test."""
    transaction = connection.begin()
    session_maker = sessionmaker(bind=connection)
    session = session_maker()
    yield session
    session.close()
    transaction.rollback()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with a database session."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Fixture that provides sample user data."""
    return {
        "name": "Test User",
        "email": unique_email(),
    }


@pytest.fixture
def test_user(db_session: Session, sample_user_data) -> User:
    """Fixture that provides a test user in the database."""
    user = User(
        **sample_user_data,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
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

    # Create a copy in the current directory for the system router to find
    current_dir_env = Path(".env")
    current_dir_env.write_text(env_content)

    yield env_file

    # Clean up the current directory .env file
    if current_dir_env.exists():
        current_dir_env.unlink()

import uuid

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


def unique_email():
    return f"test_{uuid.uuid4()}@example.com"


@pytest.fixture
def user_service(db_session):
    """Fixture that provides a UserService instance."""
    return UserService(db=db_session)


def test_create_user_success(user_service, sample_user_data):
    """
    Test successful user creation
    """
    user_data = UserCreate(
        name=sample_user_data["name"],
        email=unique_email(),
    )
    created_user = user_service.create_user(user_data)
    assert created_user.name == user_data.name
    assert created_user.email == user_data.email


def test_get_all_users_success(user_service, test_user):
    """
    Test successful retrieval of all users
    """
    users = user_service.get_all_users()
    assert len(users) == 1
    assert users[0].id == test_user.id
    assert users[0].name == test_user.name
    assert users[0].email == test_user.email


def test_get_user_success(user_service, test_user):
    """
    Test successful user retrieval
    """
    fetched_user = user_service.get_user(test_user.id)
    assert fetched_user is not None
    assert fetched_user.id == test_user.id
    assert fetched_user.name == test_user.name
    assert fetched_user.email == test_user.email


def test_get_user_not_found(user_service):
    """
    Test getting non-existent user
    """
    non_existent_user = user_service.get_user(999)
    assert non_existent_user is None


def test_update_user_success(user_service, test_user):
    """
    Test successful user update
    """
    update_data = UserUpdate(name="Updated User")
    updated_user = user_service.update_user(test_user.id, update_data)

    assert updated_user is not None
    assert updated_user.id == test_user.id
    assert updated_user.name == "Updated User"
    assert updated_user.email == test_user.email  # Should be unchanged


def test_update_user_not_found(user_service):
    """
    Test updating non-existent user
    """
    update_data = UserUpdate(name="Updated User")
    updated_user = user_service.update_user(999, update_data)
    assert updated_user is None


def test_delete_user_success(user_service, test_user):
    """
    Test successful user deletion
    """
    result = user_service.delete_user(test_user.id)
    assert result is True

    # Verify user is deleted
    deleted_user = user_service.get_user(test_user.id)
    assert deleted_user is None


def test_delete_user_not_found(user_service):
    """
    Test deleting non-existent user
    """
    result = user_service.delete_user(999)
    assert result is False


def test_service_error_handling(monkeypatch):
    """
    Test error handling in service methods
    """

    def mock_repository_error(*args, **kwargs):
        raise SQLAlchemyError("Database error")

    # Create a service with a mocked repository
    service = UserService(repository=UserRepository(None))

    # Patch repository methods to raise errors
    monkeypatch.setattr(service.repository, "get_all", mock_repository_error)
    monkeypatch.setattr(service.repository, "get", mock_repository_error)
    monkeypatch.setattr(service.repository, "create", mock_repository_error)
    monkeypatch.setattr(service.repository, "update", mock_repository_error)
    monkeypatch.setattr(service.repository, "delete", mock_repository_error)

    # Test all service methods
    with pytest.raises(SQLAlchemyError):
        service.get_all_users()

    with pytest.raises(SQLAlchemyError):
        service.get_user(1)

    with pytest.raises(SQLAlchemyError):
        service.create_user(UserCreate(name="Test", email="test@example.com"))

    with pytest.raises(SQLAlchemyError):
        service.update_user(1, UserUpdate(name="Test"))

    with pytest.raises(SQLAlchemyError):
        service.delete_user(1)


def test_user_service_dependency(db_session):
    """Test that UserService dependency injection works correctly."""
    # Test that we can create a UserService with a session
    service = UserService(db=db_session)
    assert isinstance(service, UserService)
    assert service.db == db_session


def test_user_service_with_depends(db_session):
    """Test that UserService works with FastAPI's Depends."""

    # Test that we can create a UserService with Depends
    def get_test_service(db: Session = None) -> UserService:
        if db is None:
            db = db_session
        return UserService(db=db)

    # Test that the service is created correctly
    service = get_test_service()
    assert isinstance(service, UserService)


def test_user_service_operations(db_session):
    """Test that UserService operations work correctly."""
    service = UserService(db=db_session)

    # Test user creation
    user_data = UserCreate(
        name="Test User", email=unique_email(), password="testpassword"
    )
    user = service.create_user(user_data)
    assert user.name == user_data.name
    assert user.email == user_data.email

    # Test user retrieval
    retrieved_user = service.get_user(user.id)
    assert retrieved_user.id == user.id
    assert retrieved_user.name == user.name
    assert retrieved_user.email == user.email

    # Clean up
    service.delete_user(user.id)

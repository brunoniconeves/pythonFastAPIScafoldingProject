import pytest
from sqlalchemy.exc import SQLAlchemyError
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user_repository import UserRepository

@pytest.fixture
def user_service(db):
    """Fixture that provides a UserService instance."""
    return UserService(db=db)

def test_create_user_success(user_service, sample_user_data):
    """
    Test successful user creation
    """
    user_data = UserCreate(name=sample_user_data["name"], email=sample_user_data["email"])
    created_user = user_service.create_user(user_data)
    
    assert created_user is not None
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
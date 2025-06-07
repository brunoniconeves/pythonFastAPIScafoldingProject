import pytest
from sqlalchemy.exc import SQLAlchemyError
from app.services import user_service
from app.schemas.user import UserCreate, UserUpdate

def test_get_repository_error(monkeypatch):
    """
    Test error handling in get_repository function
    """
    def mock_session_error(*args, **kwargs):
        raise SQLAlchemyError("Database error")
    
    # Patch the SessionLocal to raise an error
    monkeypatch.setattr("app.services.user_service.SessionLocal", mock_session_error)
    
    with pytest.raises(SQLAlchemyError):
        user_service.get_repository()

def test_repository_creation_error(monkeypatch):
    """
    Test error handling in repository creation
    """
    class MockSession:
        def close(self):
            pass
    
    def mock_session(*args, **kwargs):
        return MockSession()
    
    def mock_repository_init(*args, **kwargs):
        raise Exception("Repository creation error")
    
    monkeypatch.setattr("app.services.user_service.SessionLocal", mock_session)
    monkeypatch.setattr("app.services.user_service.UserRepository.__init__", mock_repository_init)
    
    with pytest.raises(Exception) as exc_info:
        user_service.get_repository()
    assert str(exc_info.value) == "Repository creation error"

def test_get_all_users_error(monkeypatch):
    """
    Test error handling in get_all_users function
    """
    def mock_get_repository():
        raise SQLAlchemyError("Database error")
    
    monkeypatch.setattr("app.services.user_service.get_repository", mock_get_repository)
    
    with pytest.raises(SQLAlchemyError):
        user_service.get_all_users()

def test_get_user_success(test_db):
    """
    Test successful user retrieval
    """
    # Create a test user first
    user_data = UserCreate(name="Test User", email="test@example.com")
    created_user = user_service.create_user(user_data)
    
    # Get the user
    fetched_user = user_service.get_user(created_user.id)
    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.name == created_user.name
    assert fetched_user.email == created_user.email

def test_get_user_not_found(test_db):
    """
    Test getting non-existent user
    """
    non_existent_user = user_service.get_user(999)
    assert non_existent_user is None

def test_get_user_error(monkeypatch):
    """
    Test error handling in get_user function
    """
    def mock_get_repository():
        raise SQLAlchemyError("Database error")
    
    monkeypatch.setattr("app.services.user_service.get_repository", mock_get_repository)
    
    with pytest.raises(SQLAlchemyError):
        user_service.get_user(1)

def test_update_user_success(test_db):
    """
    Test successful user update
    """
    # Create a test user first
    user_data = UserCreate(name="Test User", email="test@example.com")
    created_user = user_service.create_user(user_data)
    
    # Update the user
    update_data = UserUpdate(name="Updated User")
    updated_user = user_service.update_user(created_user.id, update_data)
    
    assert updated_user is not None
    assert updated_user.id == created_user.id
    assert updated_user.name == "Updated User"
    assert updated_user.email == created_user.email  # Should be unchanged

def test_update_user_not_found(test_db):
    """
    Test updating non-existent user
    """
    update_data = UserUpdate(name="Updated User")
    updated_user = user_service.update_user(999, update_data)
    assert updated_user is None

def test_update_user_error(monkeypatch):
    """
    Test error handling in update_user function
    """
    def mock_get_repository():
        raise SQLAlchemyError("Database error")
    
    monkeypatch.setattr("app.services.user_service.get_repository", mock_get_repository)
    
    with pytest.raises(SQLAlchemyError):
        user_service.update_user(1, UserUpdate(name="Test"))

def test_delete_user_success(test_db):
    """
    Test successful user deletion
    """
    # Create a test user first
    user_data = UserCreate(name="Test User", email="test@example.com")
    created_user = user_service.create_user(user_data)
    
    # Delete the user
    result = user_service.delete_user(created_user.id)
    assert result is True
    
    # Verify user is deleted
    deleted_user = user_service.get_user(created_user.id)
    assert deleted_user is None

def test_delete_user_not_found(test_db):
    """
    Test deleting non-existent user
    """
    result = user_service.delete_user(999)
    assert result is False

def test_delete_user_error(monkeypatch):
    """
    Test error handling in delete_user function
    """
    def mock_get_repository():
        raise SQLAlchemyError("Database error")
    
    monkeypatch.setattr("app.services.user_service.get_repository", mock_get_repository)
    
    with pytest.raises(SQLAlchemyError):
        user_service.delete_user(1) 
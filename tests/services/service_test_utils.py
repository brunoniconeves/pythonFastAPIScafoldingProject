from typing import Any, Dict, Optional, Type
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from app.db import Base
from app.repositories.base import BaseRepository

def create_mock_repository(model_class: Type[Base]) -> MagicMock:
    """Create a mock repository with common methods.
    
    Args:
        model_class: The model class the repository handles
        
    Returns:
        MagicMock configured with common repository methods
    """
    mock_repo = MagicMock(spec=BaseRepository)
    mock_repo.model = model_class
    return mock_repo

def setup_mock_db_session() -> MagicMock:
    """Create a mock database session.
    
    Returns:
        MagicMock configured as a database session
    """
    mock_session = MagicMock(spec=Session)
    mock_session.commit = MagicMock()
    mock_session.rollback = MagicMock()
    mock_session.close = MagicMock()
    return mock_session

def assert_service_error(
    error,
    expected_error_type: Type[Exception],
    expected_message: Optional[str] = None
):
    """Assert that a service error matches expectations.
    
    Args:
        error: The caught exception
        expected_error_type: Expected exception type
        expected_message: Expected error message (optional)
    """
    assert isinstance(error, expected_error_type)
    if expected_message:
        assert str(error) == expected_message

def create_mock_model_instance(model_class: Type[Base], data: Dict[str, Any]) -> MagicMock:
    """Create a mock model instance.
    
    Args:
        model_class: The model class to mock
        data: Attribute values for the mock instance
        
    Returns:
        MagicMock configured as a model instance
    """
    mock_instance = MagicMock(spec=model_class)
    for key, value in data.items():
        setattr(mock_instance, key, value)
    return mock_instance 
import pytest

from app.models.user import User
from app.services.user_service import UserService

from .service_test_utils import create_mock_repository, setup_mock_db_session


@pytest.fixture
def mock_user_repository():
    """Fixture that provides a mock UserRepository."""
    return create_mock_repository(User)


@pytest.fixture
def mock_db_session():
    """Fixture that provides a mock database session."""
    return setup_mock_db_session()


@pytest.fixture
def user_service(mock_user_repository, mock_db_session):
    """Fixture that provides a UserService instance with mocked dependencies."""
    return UserService(repository=mock_user_repository, db=mock_db_session)

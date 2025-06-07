import pytest
from typing import List
from app.models.user import User
from app.repositories.user_repository import UserRepository
from .repository_test_utils import create_test_models

@pytest.fixture
def user_repository(db):
    """Fixture that provides a UserRepository instance."""
    return UserRepository(db)

@pytest.fixture
def multiple_users(db, sample_user_data) -> List[User]:
    """Fixture that provides multiple test users."""
    return create_test_models(db, User, 3, sample_user_data) 
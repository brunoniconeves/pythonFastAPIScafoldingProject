import uuid
from datetime import datetime, timezone

from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate


def unique_email():
    return f"test_{uuid.uuid4()}@example.com"


def test_base_repository_create(db_session):
    """
    Test base repository create operation:
    - Creates entity successfully
    - Returns created entity
    - Entity has correct data
    """
    repo = BaseRepository(User, db_session)
    user_data = UserCreate(name="Test User", email=unique_email())

    created_user = repo.create(user_data)
    assert created_user.id is not None
    assert created_user.name == user_data.name
    assert created_user.email == user_data.email
    assert isinstance(created_user.created_at, datetime)

    # Verify in database
    db_user = db_session.query(User).filter(User.id == created_user.id).first()
    assert db_user is not None
    assert db_user.name == user_data.name


def test_base_repository_get(db_session):
    """
    Test base repository get operation:
    - Returns correct entity by ID
    - Returns None for non-existent ID
    """
    # Create a test user first
    repo = BaseRepository(User, db_session)
    user_data = UserCreate(name="Test User", email=unique_email())
    created_user = repo.create(user_data)

    # Test getting existing user
    fetched_user = repo.get(created_user.id)
    assert fetched_user is not None
    assert fetched_user.id == created_user.id
    assert fetched_user.name == created_user.name

    # Test getting non-existent user
    non_existent = repo.get(999)
    assert non_existent is None


def test_base_repository_get_all(db_session):
    """
    Test base repository get_all operation:
    - Returns empty list when no entities
    - Returns all created entities
    """
    repo = BaseRepository(User, db_session)

    # Test empty database
    users = repo.get_all()
    assert len(users) == 0

    # Create some test users
    test_users = [
        UserCreate(name="User 1", email=unique_email()),
        UserCreate(name="User 2", email=unique_email()),
        UserCreate(name="User 3", email=unique_email()),
    ]

    for user_data in test_users:
        repo.create(user_data)

    # Test getting all users
    users = repo.get_all()
    assert len(users) == len(test_users)


def test_base_repository_update(db_session):
    """
    Test base repository update operation:
    - Updates entity successfully
    - Returns updated entity
    - Returns None for non-existent ID
    """
    # Create a test user first
    repo = BaseRepository(User, db_session)
    user_data = UserCreate(name="Test User", email=unique_email())
    created_user = repo.create(user_data)

    # Update user
    update_data = UserUpdate(name="Updated User")
    updated_user = repo.update(created_user.id, update_data)
    assert updated_user is not None
    assert updated_user.id == created_user.id
    assert updated_user.name == "Updated User"
    assert updated_user.email == created_user.email  # Unchanged

    # Verify in database
    db_user = db_session.query(User).filter(User.id == created_user.id).first()
    assert db_user.name == "Updated User"

    # Test updating non-existent user
    non_existent = repo.update(999, update_data)
    assert non_existent is None


def test_base_repository_delete(db_session):
    """
    Test base repository delete operation:
    - Deletes entity successfully
    - Returns True for successful deletion
    - Returns False for non-existent ID
    """
    # Create a test user first
    repo = BaseRepository(User, db_session)
    user_data = UserCreate(name="Test User", email=unique_email())
    created_user = repo.create(user_data)

    # Delete user
    result = repo.delete(created_user.id)
    assert result is True

    # Verify user is deleted
    db_user = db_session.query(User).filter(User.id == created_user.id).first()
    assert db_user is None

    # Test deleting non-existent user
    result = repo.delete(999)
    assert result is False


def test_create_user(db_session):
    user = User(
        name="Test User",
        email=unique_email(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.name == "Test User"
    assert user.email.startswith("test_")
    assert user.created_at is not None
    assert user.updated_at is not None

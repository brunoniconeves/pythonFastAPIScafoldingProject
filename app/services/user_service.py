from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserCreate, UserUpdate, User
from app.repositories.user_repository import UserRepository

class UserService:
    """Service for handling user-related operations."""

    def __init__(self, repository: UserRepository = None, db: Session = None):
        """Initialize the service with a repository instance."""
        if repository:
            self.repository = repository
        else:
            self.repository = UserRepository(db)
        self.db = db

    def get_all_users(self) -> List[User]:
        """Get all users from the database."""
        return self.repository.get_all()

    def get_user(self, user_id: int) -> User:
        """Get a specific user by ID."""
        return self.repository.get(user_id)

    def create_user(self, user: UserCreate) -> User:
        """Create a new user."""
        return self.repository.create(user)

    def update_user(self, user_id: int, user: UserUpdate) -> User:
        """Update an existing user."""
        return self.repository.update(user_id, user)

    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        return self.repository.delete(user_id)

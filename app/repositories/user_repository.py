from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email address"""
        return self.db.query(self.model).filter(self.model.email == email).first()

    def create(self, schema: UserCreate) -> User:
        """Create a new user, with email uniqueness check"""
        if self.get_by_email(schema.email):
            raise ValueError(f"Email {schema.email} already registered")
        return super().create(schema) 
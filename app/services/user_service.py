from app.db import SessionLocal
from app.schemas.user import UserCreate, UserUpdate, User
from app.repositories.user_repository import UserRepository
from typing import List

def get_repository():
    """Get a new repository instance with its own database session"""
    db = SessionLocal()
    try:
        return UserRepository(db)
    except Exception:
        db.close()
        raise

def get_all_users() -> List[User]:
    """Get all users from the database"""
    repo = get_repository()
    try:
        return repo.get_all()
    finally:
        repo.db.close()

def get_user(user_id: int) -> User:
    """Get a specific user by ID"""
    repo = get_repository()
    try:
        return repo.get(user_id)
    finally:
        repo.db.close()

def create_user(user: UserCreate) -> User:
    """Create a new user"""
    repo = get_repository()
    try:
        return repo.create(user)
    finally:
        repo.db.close()

def update_user(user_id: int, user: UserUpdate) -> User:
    """Update an existing user"""
    repo = get_repository()
    try:
        return repo.update(user_id, user)
    finally:
        repo.db.close()

def delete_user(user_id: int) -> bool:
    """Delete a user"""
    repo = get_repository()
    try:
        return repo.delete(user_id)
    finally:
        repo.db.close()

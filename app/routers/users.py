from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas import User, UserCreate
from app.services.user_service import UserService
from app.db import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found"
        },
        status.HTTP_409_CONFLICT: {
            "description": "Email already registered"
        }
    }
)

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Dependency to get UserService instance."""
    return UserService(db=db)

@router.get(
    "/",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Get All Users",
    description="Retrieve a list of all registered users in the system.",
    response_description="List of users with their details."
)
def get_users(service: UserService = Depends(get_user_service)):
    """
    Retrieve all users from the database.
    
    Returns a list of users with their:
    - ID
    - Name
    - Email
    - Creation timestamp
    
    The list will be empty if no users are registered.
    """
    return service.get_all_users()

@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create New User",
    description="Create a new user in the system.",
    response_description="The created user's details."
)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """
    Create a new user.
    
    Parameters:
    - name: User's full name
    - email: User's email address (must be unique)
    
    Returns the created user including:
    - Assigned ID
    - Name
    - Email
    - Creation timestamp
    
    Raises:
    - HTTP 409: If the email is already registered
    """
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

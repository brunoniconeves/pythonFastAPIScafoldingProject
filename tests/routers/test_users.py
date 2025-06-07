from fastapi import status
from app.core.config import settings

def test_create_user(client, sample_user_data):
    """
    Test creating a new user:
    - Returns 201 status code
    - Returns created user data
    - User data matches input
    """
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json=sample_user_data
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == sample_user_data["name"]
    assert data["email"] == sample_user_data["email"]
    assert "id" in data
    assert "created_at" in data

def test_create_user_duplicate_email(client, sample_user_data):
    """
    Test that creating a user with duplicate email:
    - Returns 409 status code
    - Returns appropriate error message
    """
    # Create first user
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json=sample_user_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    # Try to create user with same email
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json=sample_user_data
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already registered" in response.json()["detail"].lower()

def test_get_users_empty(client):
    """
    Test getting users when database is empty:
    - Returns 200 status code
    - Returns empty list
    """
    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_users(client, sample_user_data):
    """
    Test getting users after creating one:
    - Returns 200 status code
    - Returns list with created user
    """
    # Create a user first
    create_response = client.post(
        f"{settings.API_V1_STR}/users/",
        json=sample_user_data
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Get users list
    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == status.HTTP_200_OK
    
    users = response.json()
    assert len(users) == 1
    assert users[0]["name"] == sample_user_data["name"]
    assert users[0]["email"] == sample_user_data["email"]

def test_create_user_invalid_email(client):
    """
    Test that creating a user with invalid email:
    - Returns 422 status code
    - Returns validation error
    """
    invalid_user = {
        "name": "Test User",
        "email": "not-an-email"
    }
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json=invalid_user
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
def test_create_user_missing_fields(client):
    """
    Test that creating a user with missing required fields:
    - Returns 422 status code
    - Returns validation error
    """
    incomplete_user = {"name": "Test User"}
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json=incomplete_user
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY 
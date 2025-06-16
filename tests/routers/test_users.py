import uuid

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.config import settings
from app.db import get_db
from app.main import app


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def unique_email():
    return f"test_{uuid.uuid4()}@example.com"


def test_create_user(client, sample_user_data):
    """
    Test creating a new user:
    - Returns 201 status code
    - Returns created user data
    - User data matches input
    """
    response = client.post(f"{settings.API_V1_STR}/users/", json=sample_user_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == sample_user_data["name"]
    assert data["email"] == sample_user_data["email"]
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_email(client: TestClient):
    """Test that creating a user with a duplicate email raises the correct exception."""
    email = unique_email()
    user_data = {"name": "Test User", "email": email, "password": "testpassword"}
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Try to create second user with same email
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "detail" in response.json()
    assert "already registered" in response.json()["detail"].lower()


def test_get_users_empty(client):
    """
    Test getting users when database is empty:
    - Returns 200 status code
    - Returns empty list
    """
    # Ensure the database is empty
    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert users == []


def test_get_users(client):
    """
    Test getting users after creating one:
    - Returns 200 status code
    - Returns list with created user
    """
    # Create a user first
    email = unique_email()
    user_data = {"name": "Test User", "email": email, "password": "testpassword"}
    create_response = client.post(f"{settings.API_V1_STR}/users/", json=user_data)
    assert create_response.status_code == status.HTTP_201_CREATED

    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert any(u["email"] == email for u in users)


def test_create_user_invalid_email(client):
    """
    Test that creating a user with invalid email:
    - Returns 422 status code
    - Returns validation error
    """
    invalid_user = {"name": "Test User", "email": "not-an-email"}
    response = client.post(f"{settings.API_V1_STR}/users/", json=invalid_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_missing_fields(client):
    """
    Test that creating a user with missing required fields:
    - Returns 422 status code
    - Returns validation error
    """
    incomplete_user = {"name": "Test User"}
    response = client.post(f"{settings.API_V1_STR}/users/", json=incomplete_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_invalid_data(client: TestClient):
    """Test that creating a user with invalid data raises the correct exception."""
    # Test with missing required field
    user_data = {
        "name": "Test User",
        # Missing email
        "password": "testpassword",
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Test with invalid email format
    user_data = {
        "name": "Test User",
        "email": "invalid-email",
        "password": "testpassword",
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

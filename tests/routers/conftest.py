from typing import Dict

import pytest
from fastapi import FastAPI

from app.routers import system, users


@pytest.fixture
def test_app(client) -> FastAPI:
    """Fixture that provides a test FastAPI application."""
    app = FastAPI()
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    app.include_router(system.router, prefix="/api/v1/system", tags=["system"])
    return app


@pytest.fixture
def api_headers() -> Dict[str, str]:
    """Fixture that provides common API headers."""
    return {"Content-Type": "application/json", "Accept": "application/json"}


@pytest.fixture
def user_endpoints() -> Dict[str, str]:
    """Fixture that provides user endpoint URLs."""
    return {
        "list": "/api/v1/users/",
        "create": "/api/v1/users/",
        "get": lambda user_id: f"/api/v1/users/{user_id}",
        "update": lambda user_id: f"/api/v1/users/{user_id}",
        "delete": lambda user_id: f"/api/v1/users/{user_id}",
    }

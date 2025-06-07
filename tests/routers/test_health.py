from fastapi import status
from app.core.config import settings

def test_health_check(client):
    """
    Test the health check endpoint returns:
    - 200 status code
    - JSON response with status: "ok"
    """
    response = client.get(f"{settings.API_V1_STR}/system/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok", "version": settings.VERSION}

def test_health_check_headers(client):
    """
    Test that the health check endpoint returns proper headers:
    - Content-Type: application/json
    """
    response = client.get(f"{settings.API_V1_STR}/system/health")
    assert response.headers["content-type"] == "application/json" 
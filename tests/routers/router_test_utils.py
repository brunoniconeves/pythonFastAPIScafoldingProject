from typing import Any, Dict, List, Optional

from fastapi.testclient import TestClient


def assert_response(
    response,
    expected_status_code: int,
    expected_data: Optional[Dict[str, Any]] = None,
    exclude_keys: Optional[List[str]] = None,
):
    """Assert that a response matches expected status and data.

    Args:
        response: FastAPI TestClient response
        expected_status_code: Expected HTTP status code
        expected_data: Expected response data (optional)
        exclude_keys: List of keys to exclude from data comparison
    """
    assert (
        response.status_code == expected_status_code
    ), f"Expected status code {expected_status_code}, got {response.status_code}"

    if expected_data:
        response_data = response.json()
        exclude_keys = exclude_keys or []
        for key, value in expected_data.items():
            if key not in exclude_keys:
                assert (
                    response_data[key] == value
                ), f"Expected {key}={value}, got {response_data.get(key)}"


def make_paginated_request(
    client: TestClient,
    endpoint: str,
    page: int = 1,
    per_page: int = 10,
    filters: Optional[Dict[str, Any]] = None,
):
    """Make a paginated request to an endpoint.

    Args:
        client: FastAPI TestClient
        endpoint: API endpoint
        page: Page number
        per_page: Items per page
        filters: Additional query parameters

    Returns:
        TestClient response
    """
    params = {"page": page, "per_page": per_page}
    if filters:
        params.update(filters)
    return client.get(endpoint, params=params)


def assert_error_response(
    response, expected_status_code: int, expected_error_type: Optional[str] = None
):
    """Assert that an error response is correct.

    Args:
        response: FastAPI TestClient response
        expected_status_code: Expected HTTP status code
        expected_error_type: Expected error type (optional)
    """
    assert response.status_code == expected_status_code
    error_data = response.json()
    assert "detail" in error_data
    if expected_error_type:
        assert error_data.get("type") == expected_error_type

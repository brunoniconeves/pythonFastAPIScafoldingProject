from typing import Any, Dict, List, Optional, Type

from sqlalchemy.orm import Session

from app.db import Base


def assert_model_equals(
    model_instance: Base,
    expected_data: Dict[str, Any],
    exclude_keys: Optional[List[str]] = None,
):
    """Assert that a model instance matches expected data.

    Args:
        model_instance: The model instance to check
        expected_data: Dictionary of expected values
        exclude_keys: List of keys to exclude from comparison (e.g., id, created_at)
    """
    exclude_keys = exclude_keys or []
    for key, value in expected_data.items():
        if key not in exclude_keys:
            assert (
                getattr(model_instance, key) == value
            ), f"Expected {key}={value}, got {getattr(model_instance, key)}"


def create_test_models(
    db: Session, model: Type[Base], count: int, base_data: Dict[str, Any]
) -> List[Base]:
    """Create multiple test models with sequential data.

    Args:
        db: Database session
        model: Model class to create
        count: Number of instances to create
        base_data: Base data for all instances

    Returns:
        List of created model instances
    """
    instances = []
    for i in range(count):
        data = base_data.copy()
        # Modify unique fields to make them sequential
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = f"{value}_{i}"
        instance = model(**data)
        db.add(instance)
        instances.append(instance)
    db.commit()
    for instance in instances:
        db.refresh(instance)
    return instances

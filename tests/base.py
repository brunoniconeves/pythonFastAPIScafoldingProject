from typing import Any, Dict, Optional

from fastapi.testclient import TestClient

from app.db import Base, get_db
from app.main import app


class BaseTest:
    """Base test class with common functionality for all tests."""

    @classmethod
    def setup_class(cls):
        """Setup that runs once for the test class."""
        cls.client = TestClient(app)

    def setup_method(self):
        """Setup that runs before each test method."""
        # Override database dependency
        self.test_db = next(get_db())
        app.dependency_overrides[get_db] = lambda: self.test_db

    def teardown_method(self):
        """Cleanup that runs after each test method."""
        # Clear dependency overrides
        app.dependency_overrides.clear()
        # Clean up database
        for table in reversed(Base.metadata.sorted_tables):
            self.test_db.execute(table.delete())
        self.test_db.commit()

    def create_test_data(self, model: Base, data: Dict[str, Any]) -> Base:
        """Helper method to create test data in the database.

        Args:
            model: The SQLAlchemy model class
            data: Dictionary of data to create the instance

        Returns:
            The created model instance
        """
        instance = model(**data)
        self.test_db.add(instance)
        self.test_db.commit()
        self.test_db.refresh(instance)
        return instance

    def assert_db_state(
        self, model: Base, expected_count: int, filters: Optional[Dict[str, Any]] = None
    ):
        """Helper method to assert database state.

        Args:
            model: The SQLAlchemy model class to query
            expected_count: Expected number of records
            filters: Optional filters to apply to the query
        """
        query = self.test_db.query(model)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(model, key) == value)
        assert query.count() == expected_count

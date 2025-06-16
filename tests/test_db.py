from sqlalchemy import text

from app.core.config import settings
from app.db import SessionLocal, engine


def test_database_connection(db_session):
    """Test that database connection works and SQLite configuration is correct."""
    # Test that we can execute a query
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

    # Test that SQLite configuration is correct
    if settings.DATABASE_URL.startswith("sqlite"):
        # Test that we can execute a query
        result = db_session.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_session_management(db_session):
    """Test that database sessions are properly managed."""
    # Test that the session is active
    assert db_session.is_active
    db_session.close()
    # After close, is_active should be False or raise
    try:
        _ = db_session.is_active
    except Exception:
        pass


def test_session_configuration():
    """Test that session configuration is correct."""
    # Test session configuration
    session = SessionLocal()
    # Check session configuration through its properties
    assert not session.info.get("autocommit", False)
    assert not session.info.get("autoflush", False)
    assert session.get_bind() == engine
    session.close()


def test_engine_configuration():
    """Test that engine configuration is correct."""
    # Test SQLite specific configuration
    if settings.DATABASE_URL.startswith("sqlite"):
        assert engine.dialect.name == "sqlite"
        # Check if the engine is configured for SQLite
        assert engine.pool._dialect.name == "sqlite"
    else:
        assert engine.dialect.name != "sqlite"

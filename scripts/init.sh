#!/bin/sh

# Wait for a moment to ensure database is ready
sleep 2

# Run database migrations
python -m alembic upgrade head

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 
#!/bin/sh

# Exit on error
set -e

echo "Starting initialization..."

# Wait for a moment to ensure database is ready
echo "Waiting for database..."
sleep 2

# Run database migrations
echo "Running database migrations..."
python -m alembic upgrade head || {
    echo "Failed to run migrations. Checking alembic directory..."
    ls -la /app/alembic
    echo "Checking alembic.ini..."
    ls -la /app/alembic.ini
    exit 1
}

echo "Migrations completed successfully"

# Start the application
echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 
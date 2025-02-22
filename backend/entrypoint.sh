#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI application..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

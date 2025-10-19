#!/bin/bash
# startup.sh - Docker entrypoint script

set -e

echo "Starting Telco Churn API service..."

# Wait for MLflow service to be ready (if running in docker-compose)
if [ -n "$MLFLOW_TRACKING_URI" ]; then
    echo "Waiting for MLflow service to be ready..."
    until curl -f "$MLFLOW_TRACKING_URI/health" > /dev/null 2>&1; do
        echo "MLflow not ready yet, waiting..."
        sleep 5
    done
    echo "MLflow service is ready!"
fi

# Set environment-specific config
export CONFIG_ENV=${CONFIG_ENV:-docker}
echo "Using configuration: $CONFIG_ENV"

# Start the FastAPI application
exec uvicorn deployment.api.v1.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 1 \
    --log-level info
#!/bin/bash
# Airflow Quick Start Script

set -e

echo "🚀 Telco Churn MLOps Pipeline - Airflow Setup"
echo "=============================================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
AIRFLOW_DIR="$SCRIPT_DIR"
PROJECT_ROOT="$(dirname "$AIRFLOW_DIR")"

echo "📁 Project root: $PROJECT_ROOT"
echo "📁 Airflow directory: $AIRFLOW_DIR"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Create required directories
echo "📂 Creating required directories..."
mkdir -p "$AIRFLOW_DIR/logs"
mkdir -p "$AIRFLOW_DIR/plugins"
mkdir -p "$AIRFLOW_DIR/config"
mkdir -p "$PROJECT_ROOT/data/raw"
mkdir -p "$PROJECT_ROOT/data/processed"
mkdir -p "$PROJECT_ROOT/mlruns"
mkdir -p "$PROJECT_ROOT/mlartifacts"

echo "✅ Directories created"

# Create .env file if it doesn't exist
if [ ! -f "$AIRFLOW_DIR/.env" ]; then
    echo "📝 Creating .env file..."
    cat > "$AIRFLOW_DIR/.env" << EOF
# Airflow User ID
AIRFLOW_UID=$(id -u)

# Airflow Configuration
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__CORE__LOAD_EXAMPLES=false
AIRFLOW__CORE__FERNET_KEY=

# Database Configuration
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
EOF
    echo "✅ .env file created with UID: $(id -u)"
else
    echo "ℹ️  .env file already exists"
fi

# Change to airflow directory
cd "$AIRFLOW_DIR"

# Initialize Airflow
echo "🔧 Initializing Airflow database..."
docker-compose up airflow-init

if [ $? -eq 0 ]; then
    echo "✅ Airflow initialized successfully"
else
    echo "❌ Airflow initialization failed"
    exit 1
fi

# Start Airflow services
echo "🚀 Starting Airflow services..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✨ Airflow is ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Airflow UI: http://localhost:8080"
echo "👤 Username: admin"
echo "🔑 Password: admin"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Next steps:"
echo "  1. Open http://localhost:8080 in your browser"
echo "  2. Login with admin/admin"
echo "  3. Enable the 'telco_churn_training_pipeline' DAG"
echo "  4. Trigger the DAG to run the pipeline"
echo ""
echo "📝 View logs:"
echo "  docker-compose logs -f"
echo ""
echo "🛑 Stop Airflow:"
echo "  docker-compose down"
echo ""

# Airflow Setup and Usage Guide

## Prerequisites

- Docker and Docker Compose installed
- Sufficient disk space for Airflow and PostgreSQL data

## Initial Setup

### 1. Set Environment Variables

```bash
cd airflow
cp .env.example .env
# Edit .env and set AIRFLOW_UID to your user ID
# Run: id -u
# Update AIRFLOW_UID in .env
```

### 2. Create Required Directories

```bash
# From project root
mkdir -p airflow/logs airflow/plugins airflow/config
```

### 3. Initialize Airflow

```bash
cd airflow
docker-compose up airflow-init
```

This will:

- Initialize the Airflow database
- Create an admin user (username: admin, password: admin)
- Set up required directories with proper permissions

### 4. Start Airflow Services

```bash
docker-compose up -d
```

This starts:

- PostgreSQL database
- Airflow webserver (http://localhost:8080)
- Airflow scheduler

## Accessing Airflow

1. Open your browser and navigate to: http://localhost:8080
2. Login with:
   - Username: `admin`
   - Password: `admin`

## Using the ML Pipeline DAG

### 1. Enable the DAG

In the Airflow UI:

1. Navigate to the DAGs page
2. Find `telco_churn_training_pipeline`
3. Toggle the switch to enable it

### 2. Trigger the DAG

- Click on the DAG name
- Click the "Play" button (▶) in the top right
- Select "Trigger DAG"

### 3. Monitor Execution

- View the Graph view to see task dependencies
- Click on individual tasks to see logs
- Check the Grid view for run history

## Pipeline Tasks

The pipeline consists of 4 tasks:

1. **ingest_data**: Load raw data from source
2. **preprocess_data**: Clean and transform data
3. **train_model**: Train ML model with MLflow tracking
4. **evaluate_model**: Evaluate and register best model

## Accessing Pipeline Logs

### From Airflow UI:

- Click on a task in the Graph/Grid view
- Click "Log" to view execution logs

### From Host Machine:

```bash
# View logs directory
ls -la airflow/logs/dag_id=telco_churn_training_pipeline/

# View specific task logs
tail -f airflow/logs/dag_id=telco_churn_training_pipeline/run_id=*/task_id=train_model/attempt=1.log
```

## Accessing MLflow Artifacts

MLflow artifacts are stored in `mlruns/` and `mlartifacts/` in the project root.

To view MLflow UI:

```bash
# From project root
mlflow ui --backend-store-uri file:///path/to/mlruns
```

## Volume Mounts

The Airflow containers have access to:

- `/opt/airflow/project/pipeline/` - Pipeline scripts
- `/opt/airflow/project/data/` - Data directory
- `/opt/airflow/project/mlruns/` - MLflow tracking
- `/opt/airflow/project/mlartifacts/` - MLflow artifacts
- `/opt/airflow/project/configs/` - Configuration files
- `/opt/airflow/project/utils/` - Utility modules

## Stopping Airflow

```bash
cd airflow
docker-compose down
```

To remove all data (including database):

```bash
docker-compose down -v
```

## Troubleshooting

### Permission Issues

If you encounter permission errors:

```bash
# Set proper ownership
sudo chown -R ${AIRFLOW_UID}:0 airflow/logs airflow/dags airflow/plugins

# Or use your current user
sudo chown -R $(id -u):$(id -g) airflow/logs airflow/dags airflow/plugins
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps

# View PostgreSQL logs
docker-compose logs postgres
```

### Task Execution Issues

1. Check task logs in Airflow UI
2. Verify volume mounts are correct
3. Ensure Python dependencies are installed
4. Check file paths in environment variables

### Installing Additional Python Packages

Create a custom Dockerfile:

```dockerfile
FROM apache/airflow:2.10.2
USER root
RUN apt-get update && apt-get install -y <system-packages>
USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
```

Then update docker-compose.yaml to build from this Dockerfile.

## Configuration

### Changing DAG Schedule

Edit `airflow/dags/ml_pipeline.py`:

```python
schedule_interval='@daily',  # Run daily
# or
schedule_interval='0 0 * * 0',  # Run weekly (Sunday midnight)
```

### Modifying Environment Variables

Edit task definitions in the DAG file to change paths or add new environment variables.

### Scaling Workers

To add more workers, update `docker-compose.yaml`:

```yaml
  airflow-worker:
    <<: *airflow-common
    command: celery worker
    # Add more worker services as needed
```

And change executor to CeleryExecutor in environment variables.

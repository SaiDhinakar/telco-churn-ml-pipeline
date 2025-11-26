# Pipeline Module

This directory contains the ML training pipeline scripts that are orchestrated by Airflow.

## Structure

```
pipeline/
├── __init__.py           # Package initialization
├── ingest.py            # Data ingestion from Kaggle
├── preprocess.py        # Data preprocessing and feature engineering
├── train.py             # Multi-model training with MLflow tracking
└── update_config.py     # Model selection and config update
```

## Pipeline Steps

### 1. Data Ingestion (`ingest.py`)

Downloads Telco Customer Churn dataset from Kaggle and saves to raw data directory.

**Features:**

- Downloads dataset using kagglehub
- Checks if data already exists to avoid re-downloading
- Handles file organization and cleanup
- Logs all operations

**Run standalone:**

```bash
uv run pipeline/ingest.py
# or
python pipeline/ingest.py
```

**Environment Variables:**

- `RAW_DATA_PATH`: Custom output path (optional)

### 2. Data Preprocessing (`preprocess.py`)

Cleans and transforms raw data into ML-ready format.

**Features:**

- Handles missing values (TotalCharges)
- Encodes categorical variables (gender, contract type, etc.)
- Converts target variable (Churn) to binary
- Removes non-feature columns (customerID)
- Validates data quality

**Run standalone:**

```bash
uv run pipeline/preprocess.py
# or
python pipeline/preprocess.py
```

**Environment Variables:**

- `RAW_DATA_PATH`: Input data path (optional)
- `PROCESSED_DATA_PATH`: Output data path (optional)

### 3. Model Training (`train.py`)

Trains multiple ML models with GridSearchCV and tracks everything in MLflow.

**Features:**

- Trains 4 models: Logistic Regression, Random Forest, XGBoost, LightGBM
- Hyperparameter tuning with GridSearchCV (5-fold CV)
- Tracks all metrics: accuracy, precision, recall, f1_score
- Logs models to MLflow with appropriate flavors
- Returns results for all trained models

**Models & Hyperparameters:**

- **Logistic Regression**: C values, solvers (with StandardScaler)
- **Random Forest**: n_estimators, max_depth
- **XGBoost**: learning_rate, n_estimators, max_depth
- **LightGBM**: learning_rate, n_estimators, num_leaves

**Run standalone:**

```bash
uv run pipeline/train.py
# or
python pipeline/train.py
```

**Environment Variables:**

- `PROCESSED_DATA_PATH`: Input processed data path
- `MLFLOW_TRACKING_URI`: MLflow tracking server (default: http://localhost:5000)

### 4. Update Configuration (`update_config.py`)

Selects the best model based on accuracy and updates production config.

**Features:**

- Queries MLflow to find top 2 models by accuracy
- Registers champion (best) and challenger (2nd best) models
- Sets model aliases in MLflow Model Registry
- Updates `configs/prod.yml` with model URIs
- Preserves other config settings

**Run standalone:**

```bash
uv run pipeline/update_config.py
# or
python pipeline/update_config.py
```

**Environment Variables:**

- `MLFLOW_TRACKING_URI`: MLflow tracking server (default: http://localhost:5000)

**Output:**
Updates `configs/prod.yml`:

```yaml
model_uri: "models:/LightGBM@champion"
fallback_model_uri: "models:/XGBoost@challenger"
```

## Complete Pipeline Execution

Run the entire pipeline in sequence:

```bash
# 1. Ingest data from Kaggle
uv run pipeline/ingest.py

# 2. Preprocess and clean data
uv run pipeline/preprocess.py

# 3. Train all models with MLflow tracking
uv run pipeline/train.py

# 4. Select best model and update config
uv run pipeline/update_config.py
```

## Configuration

### Environment Variables

Each script uses environment variables for configuration:

- `RAW_DATA_PATH`: Path to raw data directory
- `PROCESSED_DATA_PATH`: Path to processed data
- `MLFLOW_TRACKING_URI`: MLflow tracking server URL

### Default Paths

When running standalone (outside Airflow):

- Raw data: `data/raw/telco-customer-churn.csv`
- Processed data: `data/processed/cleaned_telco_customer_churn.csv`
- MLflow: `http://localhost:5000`

When running in Airflow:

- Raw data: `/opt/airflow/project/data/raw/telco-customer-churn.csv`
- Processed data: `/opt/airflow/project/data/processed/cleaned_telco_customer_churn.csv`
- MLflow: `/opt/airflow/project/mlruns`

## Development Workflow

1. **Develop and test each script independently:**

   ```bash
   uv run pipeline/ingest.py
   uv run pipeline/preprocess.py
   uv run pipeline/train.py
   uv run pipeline/update_config.py
   ```
2. **Start MLflow UI (for local testing):**

   ```bash
   mlflow ui --port 5000
   # Access at http://localhost:5000
   ```
3. **Test with Airflow:**

   ```bash
   cd airflow
   ./start-airflow.sh
   # Access Airflow UI at http://localhost:8080
   # Trigger ml_training_pipeline DAG
   ```
4. **Monitor execution:**

   - View logs in Airflow UI (task logs)
   - Check MLflow experiments at http://localhost:5000
   - Verify output data files in `data/` directories
   - Check updated config in `configs/prod.yml`

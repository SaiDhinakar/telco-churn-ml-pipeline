# 🚀 Telco Customer Churn ML Pipeline

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.10.2-orange.svg)](https://airflow.apache.org/)
[![MLflow](https://img.shields.io/badge/MLflow-Latest-blue.svg)](https://mlflow.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)

A production-ready ML pipeline for predicting customer churn in telecommunications companies. This project demonstrates end-to-end machine learning workflow automation using **Apache Airflow** for orchestration, **MLflow** for experiment tracking, and **FastAPI** for model serving - all containerized with **Docker**.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Dataset](#-dataset)
- [Machine Learning Models](#-machine-learning-models)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Documentation](#-documentation)

---

## 🎯 Project Overview

This project implements a **complete ML pipeline** that automates the entire machine learning lifecycle for predicting customer churn in the telecommunications industry. The pipeline handles everything from data ingestion to model deployment, with orchestration, monitoring, and serving capabilities.

### What Does This Pipeline Do?

1. **📥 Data Ingestion**: Automatically fetches the Telco Customer Churn dataset from Kaggle
2. **🔧 Data Preprocessing**: Cleans, transforms, and engineers features from raw data
3. **🤖 Model Training**: Trains multiple ML models (Logistic Regression, Random Forest, XGBoost, LightGBM)
4. **📊 Model Selection**: Automatically selects the best-performing model based on accuracy metrics
5. **💾 Model Registry**: Registers models in MLflow with versioning and metadata
6. **🚀 Model Deployment**: Serves the best model through a REST API for real-time predictions
7. **🔄 Pipeline Orchestration**: Manages the entire workflow using Apache Airflow

### Key Highlights

- **Fully Automated**: End-to-end automation from data ingestion to model deployment
- **Containerized**: Both Airflow orchestration and API services run in separate Docker containers
- **Production Ready**: Includes logging, error handling, model versioning, and API documentation
- **Scalable**: Designed with distributed architecture principles for easy scaling

---

## 🏗️ Architecture

The project follows a **microservices architecture** with two main containerized components:

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│    (API Clients, Airflow UI, MLflow UI, Swagger Docs)           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐    ┌─────────────┐
│   FastAPI    │    │  Apache Airflow  │    │   MLflow    │
│  Container   │    │    Container     │    │  Tracking   │
│   (Port      │    │   (Port 8080)    │    │   Server    │
│    8000)     │    │                  │    │ (Port 5000) │
└──────────────┘    └──────────────────┘    └─────────────┘
       │                     │                      │
       │                     │                      │
       └─────────────────────┴──────────────────────┘
                             │
                             ▼
                  ┌───────────────────┐
                  │  Shared Storage   │
                  │  - mlruns/        │
                  │  - mlartifacts/   │
                  │  - data/          │
                  │  - config/        │
                  └───────────────────┘
```

### Components

1. **Airflow Container** (Port 8080)

   - Orchestrates the ML pipeline
   - Manages task dependencies and scheduling
   - Includes PostgreSQL for metadata storage
   - Runs data ingestion, preprocessing, training, and config update tasks
2. **FastAPI Container** (Port 8000)

   - Serves trained models via REST API
   - Provides prediction endpoints
   - Triggers Airflow pipeline executions
   - Monitors training status
   - Auto-reloads models based on configuration
3. **MLflow Tracking**

   - Tracks experiments and metrics
   - Manages model registry
   - Stores model artifacts
   - Provides model versioning

---

## ✨ Features

### Pipeline Orchestration

- 🔄 **Automated Workflow**: Apache Airflow DAG manages end-to-end ML pipeline
- 📅 **Scheduled Execution**: Support for periodic retraining
- 🔗 **Task Dependencies**: Proper task sequencing (ingest → preprocess → train → update config)
- 🔁 **Retry Logic**: Automatic retry on task failures
- 📊 **Monitoring Dashboard**: Airflow UI for pipeline visualization and monitoring

### Machine Learning

- 🤖 **Multiple Models**: Trains and compares 4 different ML algorithms
- 📈 **Hyperparameter Tuning**: Grid search for optimal model parameters
- 🎯 **Automatic Model Selection**: Selects best model based on accuracy metrics
- 💾 **Experiment Tracking**: Complete MLflow integration for reproducibility
- 🏷️ **Model Registry**: Version control and model lifecycle management

### Deployment & Serving

- 🚀 **REST API**: FastAPI-based model serving
- 🐳 **Containerized**: Docker containers for easy deployment
- 📝 **API Documentation**: Auto-generated Swagger/OpenAPI docs
- 🔄 **Dynamic Model Loading**: Updates model without container restart
- 🔐 **Data Validation**: Pydantic models for request validation

### Monitoring & Operations

- 📊 **Pipeline Status**: Check Airflow DAG run status via API
- 🎯 **Training Triggers**: Trigger retraining on-demand via API
- 📝 **Logging**: Comprehensive logging across all components
- ✅ **Testing**: Unit tests for API and model predictions

---

## 💻 Technology Stack

### Orchestration & Workflow

- **Apache Airflow 2.10.2**: Pipeline orchestration and scheduling
- **PostgreSQL 13**: Airflow metadata database

### Machine Learning & Tracking

- **MLflow**: Experiment tracking and model registry
- **Scikit-learn**: ML algorithms and preprocessing
- **XGBoost**: Gradient boosting framework
- **LightGBM**: Gradient boosting framework
- **Pandas & NumPy**: Data manipulation

### API & Web Services

- **FastAPI**: High-performance API framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation and settings management

### Infrastructure & DevOps

- **Docker & Docker Compose**: Containerization
- **Python 3.12**: Programming language
- **UV**: Fast Python package manager
- **Pytest**: Testing framework

### Data Source

- **Kaggle API**: Dataset ingestion
- **KaggleHub**: Dataset management

---

## 📊 Dataset

**Source**: [Telco Customer Churn Dataset on Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

The dataset contains **7,043 customers** with **21 features** including:

- **Demographics**: Gender, SeniorCitizen, Partner, Dependents
- **Services**: PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies
- **Account Information**: Contract, PaperlessBilling, PaymentMethod, tenure, MonthlyCharges, TotalCharges
- **Target Variable**: Churn (Yes/No)

The pipeline automatically downloads this dataset from Kaggle during the ingestion phase.

---

## 🤖 Machine Learning Models

The pipeline trains and evaluates **four different algorithms**:

| Model                         | Type               | Hyperparameter Tuning                      |
| ----------------------------- | ------------------ | ------------------------------------------ |
| **Logistic Regression** | Linear Model       | Regularization (C)                         |
| **Random Forest**       | Ensemble (Bagging) | n_estimators, max_depth, min_samples_split |
| **XGBoost**             | Gradient Boosting  | n_estimators, learning_rate, max_depth     |
| **LightGBM**            | Gradient Boosting  | n_estimators, learning_rate, num_leaves    |

### Evaluation Metrics

Models are evaluated using comprehensive metrics:

- ✅ **Accuracy**: Overall prediction correctness
- 🎯 **Precision**: Positive prediction accuracy
- 📊 **Recall**: True positive detection rate
- 🔄 **F1-Score**: Harmonic mean of precision and recall
- 📈 **AUC**: Area under ROC curve

The model with the **highest accuracy** is automatically selected as the production model.

---

## 🚀 Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+**
- **Docker & Docker Compose**
- **UV Package Manager** (optional, for local development)
- **Kaggle API Credentials** (for data ingestion)

### Step 1: Clone the Repository

```bash
git clone https://github.com/SaiDhinakar/telco-churn-ML-pipeline.git
cd telco-churn-ML-pipeline
```

### Step 2: Configure Environment Variables

Create a `.env` file in the `airflow/` directory:

```bash
cd airflow
cat > .env << EOF
MLFLOW_TRACKING_URI=http://host.docker.internal:5000
AIRFLOW_PUBLIC_URL=http://localhost:8080
API_SERVER_URL=http://host.docker.internal:8000
AIRFLOW_UID=50000
EOF
cd ..
```

### Step 3: Install Dependencies (Local Development)

For local development without Docker:

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### Step 4: Start Services

#### Option A: Full Stack with Docker (Recommended)

```bash
# Start Airflow (orchestration)
cd airflow
docker-compose up -d
cd ..

# Start API service
docker-compose up -d
```

#### Option B: Local Development

```bash
# Terminal 1: Start MLflow
mlflow ui --port 5000

# Terminal 2: Start Airflow (if needed locally)
airflow standalone

# Terminal 3: Start API
uvicorn deployment.api.v1.main:app --reload --port 8000
```

### Step 5: Verify Installation

- **Airflow UI**: http://localhost:8080 (username: `airflow`, password: `airflow`)
- **API Documentation**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5000

---

## 📖 Usage

### 1️⃣ Trigger the ML Pipeline

You can trigger the pipeline in two ways:

**Via Airflow UI:**

1. Navigate to http://localhost:8080
2. Find the `telco_churn_training_pipeline` DAG
3. Click the "Play" button to trigger

**Via API:**

```bash
curl -X POST "http://localhost:8000/api/v1/trigger-training"
```

### 2️⃣ Monitor Pipeline Execution

**Check pipeline status:**

```bash
# Get the dag_run_id from the trigger response
curl "http://localhost:8000/api/v1/training-status/{dag_run_id}"
```

**View in Airflow UI:**

- Navigate to http://localhost:8080/dags/telco_churn_training_pipeline/grid

### 3️⃣ Make Predictions

Once the pipeline completes and model is deployed:

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.35,
    "TotalCharges": 844.2
  }'
```

### 4️⃣ Reload Model (After Retraining)

```bash
curl "http://localhost:8000/api/v1/restart"
```

---

## 🔌 API Endpoints

The FastAPI service provides the following endpoints:

| Endpoint                                 | Method | Description                                |
| ---------------------------------------- | ------ | ------------------------------------------ |
| `/`                                    | GET    | Welcome message and API info               |
| `/docs`                                | GET    | Interactive API documentation (Swagger UI) |
| `/api/v1/predict`                      | POST   | Make churn prediction for a customer       |
| `/api/v1/restart`                      | GET    | Reload model from updated configuration    |
| `/api/v1/trigger-training`             | POST   | Trigger Airflow ML pipeline                |
| `/api/v1/training-status/{dag_run_id}` | GET    | Get status of specific pipeline run        |

### Detailed Endpoint Documentation

#### 1. Prediction Endpoint

```http
POST /api/v1/predict
```

**Request Body:**

```json
{
  "gender": "string",
  "SeniorCitizen": 0 or 1,
  "Partner": "Yes" or "No",
  "Dependents": "Yes" or "No",
  "tenure": integer,
  "PhoneService": "Yes" or "No",
  "MultipleLines": "Yes" or "No" or "No phone service",
  "InternetService": "DSL" or "Fiber optic" or "No",
  "OnlineSecurity": "Yes" or "No" or "No internet service",
  "OnlineBackup": "Yes" or "No" or "No internet service",
  "DeviceProtection": "Yes" or "No" or "No internet service",
  "TechSupport": "Yes" or "No" or "No internet service",
  "StreamingTV": "Yes" or "No" or "No internet service",
  "StreamingMovies": "Yes" or "No" or "No internet service",
  "Contract": "Month-to-month" or "One year" or "Two year",
  "PaperlessBilling": "Yes" or "No",
  "PaymentMethod": "Electronic check" or "Mailed check" or "Bank transfer (automatic)" or "Credit card (automatic)",
  "MonthlyCharges": float,
  "TotalCharges": float
}
```

**Response:**

```json
{
  "churn_prediction": true or false
}
```

#### 2. Trigger Training

```http
POST /api/v1/trigger-training
```

**Response:**

```json
{
  "message": "Training pipeline triggered successfully",
  "dag_id": "telco_churn_training_pipeline",
  "dag_run_id": "manual__2025-11-27T15:29:04.176890+00:00",
  "execution_date": "2025-11-27T15:29:04.176890+00:00",
  "state": "queued",
  "airflow_ui": "http://localhost:8080/dags/telco_churn_training_pipeline/grid"
}
```

#### 3. Check Training Status

```http
GET /api/v1/training-status/{dag_run_id}
```

**Response:**

```json
{
  "dag_id": "telco_churn_training_pipeline",
  "dag_run_id": "manual__2025-11-27T15:29:04.176890+00:00",
  "state": "success",
  "start_date": "2025-11-27T15:29:04.176890+00:00",
  "end_date": "2025-11-27T15:35:22.123456+00:00",
  "execution_date": "2025-11-27T15:29:04.176890+00:00",
  "airflow_ui": "http://localhost:8080/dags/telco_churn_training_pipeline/grid?dag_run_id=..."
}
```

---

## 📁 Project Structure

```
telco-churn-ML-pipeline/
│
├── 🎭 airflow/                    # Apache Airflow orchestration
│   ├── dags/
│   │   └── ml_pipeline.py         # Main DAG definition
│   ├── logs/                      # Airflow execution logs
│   ├── config/                    # Airflow configuration
│   ├── Dockerfile                 # Airflow container image
│   ├── docker-compose.yaml        # Airflow stack composition
│   ├── requirements.txt           # Airflow dependencies
│   └── start-airflow.sh          # Airflow startup script
│
├── 🚀 deployment/                 # Model deployment & API
│   ├── api/
│   │   └── v1/
│   │       └── main.py           # FastAPI application
│   ├── models/
│   │   └── telcom_customer.py    # Pydantic models
│   ├── services/
│   │   └── model_service.py      # Model loading & prediction
│   ├── Dockerfile                 # API container image
│   └── requirements.txt          # API dependencies
│
├── 🔧 pipeline/                   # ML pipeline modules
│   ├── ingest.py                 # Data ingestion from Kaggle
│   ├── preprocess.py             # Data preprocessing
│   ├── train.py                  # Model training
│   └── update_config.py          # Config update after training
│
├── ⚙️  configs/                   # Configuration files
│   └── prod.yml                  # Production model config
│
├── 📊 data/                       # Data storage
│   ├── raw/                      # Raw datasets
│   └── processed/                # Processed datasets
│
├── 📓 notebooks/                  # Jupyter notebooks
│   ├── preprocessing.ipynb       # EDA & feature engineering
│   └── train.ipynb              # Model training experiments
│
├── 🧪 tests/                      # Test suite
│   ├── test_api_endpoint.py     # API endpoint tests
│   ├── test_model.py            # Model tests
│   └── test_sample_prediction.py # Prediction tests
│
├── 📝 docs/                       # Documentation
│   ├── DEVELOPMENT.md            # Development guide
│   ├── DEPLOYMENT.md             # Deployment guide
│   ├── STRUCTURE.md              # Structure details
│   └── DISTRIBUTED_ARCHITECTURE.md
│
├── 🛠️  utils/                     # Utility functions
│   └── logger.py                # Logging configuration
│
├── 📦 mlruns/                     # MLflow experiment tracking
├── 📦 mlartifacts/                # MLflow model artifacts
├── 🐳 docker-compose.yml          # Main Docker composition
├── 📄 pyproject.toml             # Project dependencies
└── 📖 README.md                  # This file
```

---

## 🧪 Testing

The project includes comprehensive tests for API endpoints and model predictions.

### Run All Tests

```bash
# Using pytest
pytest

# With coverage
pytest --cov=deployment --cov=pipeline

# Verbose output
pytest -v
```

### Test Categories

| Test File                     | Description                          |
| ----------------------------- | ------------------------------------ |
| `test_api_endpoint.py`      | API endpoint functionality tests     |
| `test_model.py`             | Model loading and prediction tests   |
| `test_sample_prediction.py` | End-to-end prediction workflow tests |

### Manual Testing

**Test API Health:**

```bash
curl http://localhost:8000/
```

**Test Prediction:**

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d @tests/sample_customer.json
```

---

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

| Document                                                               | Description                                           |
| ---------------------------------------------------------------------- | ----------------------------------------------------- |
| **[DEVELOPMENT.md](docs/DEVELOPMENT.md)**                           | Development setup, workflow, and best practices       |
| **[DEPLOYMENT.md](docs/DEPLOYMENT.md)**                             | Deployment instructions and production setup          |
| **[STRUCTURE.md](docs/STRUCTURE.md)**                               | Detailed project structure and component descriptions |
| **[DISTRIBUTED_ARCHITECTURE.md](docs/DISTRIBUTED_ARCHITECTURE.md)** | Architecture design and scaling considerations        |

---

## 🔄 ML Pipeline Workflow

The Airflow DAG orchestrates the following tasks:

```
┌─────────────────┐
│  1. Data        │  Fetch Telco Churn dataset from Kaggle
│     Ingestion   │  
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. Data        │  Clean data, handle missing values,
│     Preprocess  │  encode categorical features
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. Model       │  Train 4 models with hyperparameter tuning:
│     Training    │  - Logistic Regression
│                 │  - Random Forest
│                 │  - XGBoost
│                 │  - LightGBM
│                 │  Track experiments with MLflow
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. Model       │  Select best model based on accuracy
│     Selection   │  Update production config (prod.yml)
│     & Config    │  Register model in MLflow
│     Update      │
└─────────────────┘
```

### Task Details

1. **Data Ingestion** (`run_ingest`)

   - Downloads dataset from Kaggle using `kagglehub`
   - Saves raw data to `data/raw/`
   - Passes data path to next task via XCom
2. **Data Preprocessing** (`run_preprocess`)

   - Handles missing values
   - Encodes categorical variables
   - Engineers features
   - Saves processed data to `data/processed/`
3. **Model Training** (`run_train`)

   - Trains 4 different models with GridSearchCV
   - Logs parameters, metrics, and artifacts to MLflow
   - Evaluates models on validation set
   - Returns best model information
4. **Config Update** (`run_update_config`)

   - Selects best performing model
   - Updates `configs/prod.yml` with model details
   - Triggers API to reload the new model

---

## 🎯 Model Registry & Versioning

The project uses **MLflow Model Registry** for model lifecycle management:

### Model Stages

- **None**: Newly trained models
- **Staging**: Models under evaluation
- **Production**: Currently deployed model
- **Archived**: Deprecated models

### Accessing Models

```python
import mlflow

# Load production model
model = mlflow.pyfunc.load_model("models:/LightGBM/Production")

# Load specific version
model = mlflow.pyfunc.load_model("models:/XGBoost/3")
```

### Model Metadata

Each model includes:

- Hyperparameters
- Training metrics (accuracy, precision, recall, F1, AUC)
- Feature importance
- Training timestamp
- Data version/hash

---

## 🐳 Docker Services

### Service Overview

| Service                     | Container             | Port | Purpose                     |
| --------------------------- | --------------------- | ---- | --------------------------- |
| **API**               | `telco-api`         | 8000 | Model serving & predictions |
| **Airflow Webserver** | `airflow-webserver` | 8080 | Pipeline UI & monitoring    |
| **Airflow Scheduler** | `airflow-scheduler` | -    | Task scheduling & execution |
| **PostgreSQL**        | `postgres`          | 5432 | Airflow metadata storage    |

### Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build

# Remove volumes (clean slate)
docker-compose down -v

# Check service status
docker-compose ps
```

### Accessing Containers

```bash
# Execute command in API container
docker-compose exec api bash

# Execute command in Airflow
docker-compose -f airflow/docker-compose.yaml exec airflow-webserver bash

# View API logs
docker-compose logs -f api

# View Airflow scheduler logs
docker-compose -f airflow/docker-compose.yaml logs -f airflow-scheduler
```

---

## 🔧 Configuration

### Production Model Config (`configs/prod.yml`)

This file is automatically updated by the pipeline with the best model:

```yaml
model:
  name: "LightGBM"
  version: "3"
  run_id: "a1b2c3d4e5f6g7h8"
  accuracy: 0.8234
  registered_model_uri: "models:/LightGBM/3"
```

### Environment Variables

**Airflow** (`.env` in `airflow/` directory):

```bash
MLFLOW_TRACKING_URI=http://host.docker.internal:5000
AIRFLOW_PUBLIC_URL=http://localhost:8080
API_SERVER_URL=http://host.docker.internal:8000
AIRFLOW_UID=50000
```

**API** (environment variables in `docker-compose.yml`):

```bash
AIRFLOW_BASE_URL=http://host.docker.internal:8080
AIRFLOW_USERNAME=airflow
AIRFLOW_PASSWORD=airflow
```

---

## 🚨 Troubleshooting

### Common Issues

**1. Airflow containers fail to start**

```bash
# Set correct permissions
chmod -R 777 airflow/logs airflow/dags airflow/plugins

# Set AIRFLOW_UID
export AIRFLOW_UID=$(id -u)
```

**2. API cannot connect to Airflow**

- Ensure Airflow is running on port 8080
- Check `AIRFLOW_BASE_URL` environment variable
- Use `host.docker.internal` for container-to-host communication

**3. Model prediction fails**

- Check if model config exists: `configs/prod.yml`
- Verify MLflow artifacts are present: `mlartifacts/`
- Restart API service: `curl http://localhost:8000/api/v1/restart`

**4. Pipeline task fails in Airflow**

- Check logs in Airflow UI
- Verify all dependencies are installed
- Check data paths and permissions

### Logs Location

- **Airflow**: `airflow/logs/`
- **API**: Check Docker logs with `docker-compose logs api`
- **Application**: `logs/` directory

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines

- Add docstrings to functions and classes
- Write unit tests for new features
- Update documentation as needed

---

## 🙏 Acknowledgments

- **Dataset**: [Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) from Kaggle
- **MLflow**: For experiment tracking and model registry
- **Apache Airflow**: For workflow orchestration
- **FastAPI**: For high-performance API framework

---

## 📧 Contact

**Sai Dhinakar**

- GitHub: [@SaiDhinakar](https://github.com/SaiDhinakar)
- Repository: [telco-churn-ML-pipeline](https://github.com/SaiDhinakar/telco-churn-ML-pipeline)

---

## 🔗 References

- [MLflow Documentation](https://www.mlflow.org/docs/latest/index.html)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation
  ](https://docs.docker.com/)

---

<div align="center">

**⭐ If you find this project helpful, please consider giving it a star! ⭐**

</div>

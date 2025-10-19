# Telco Customer Churn MLOps Pipeline

A comprehensive MLOps pipeline for predicting customer churn in telecommunications companies using machine learning models with MLflow tracking and deployment capabilities.

## Project Overview

This project implements an end-to-end machine learning pipeline to predict customer churn for telecommunications companies. The pipeline includes data preprocessing, model training, evaluation, tracking, and deployment using modern MLOps practices.

## Dataset

**Source**: [Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

The dataset contains customer information including demographics, services used, and churn status for a telecommunications company.

## Features

- **Data Processing**: Comprehensive EDA and feature engineering
- **Model Training**: Multiple ML algorithms implementation and comparison
- **Model Tracking**: MLflow integration for experiment tracking and model registry
- **Model Deployment**: Containerized API for model inference
- **Testing**: Comprehensive test suite for API and models
- **Documentation**: Complete project documentation

## Machine Learning Models

The pipeline implements and compares the following models:

- **Logistic Regression**
- **Random Forest**
- **XGBoost**
- **LightGBM**

Models are evaluated using multiple metrics:

- AUC (Area Under Curve)
- F1-Score
- Accuracy
- Precision
- Recall

## Technology Stack

- **Python 3.12**
- **MLflow**: Experiment tracking and model registry
- **FastAPI**: API framework for model deployment
- **Docker**: Containerization
- **UV**: Package management
- **Pytest**: Testing framework
- **Pydantic**: Data validation

## Project Structure

```
telco-churn-mlops-pipeline/
├── configs/          # Configuration files
├── data/            # Raw and processed datasets
├── deployment/      # Model inference and API code
├── docs/           # Project documentation
├── notebooks/      # Jupyter notebooks for development
├── tests/          # Test scripts
├── utils/          # Utility functions
├── mlruns/         # MLflow experiment tracking
└── mlartifacts/    # MLflow model artifacts
```

## Quick Start

### Prerequisites

- Python 3.12
- UV package manager
- Docker (for deployment)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SaiDhinakar/telco-churn-mlops-pipeline
   cd telco-churn-mlops-pipeline
   ```
2. Install dependencies:

   ```bash
   uv sync
   ```
3. Start MLflow tracking server:

   ```bash
   mlflow ui
   ```

### Development Workflow

1. **Data Preprocessing**: Run `notebooks/preprocessing.ipynb` for EDA and feature engineering
2. **Model Training**: Use `notebooks/train.ipynb` to train and track models
3. **Model Selection**: Use MLflow UI to compare models and select the best performer
4. **Configuration**: Update `configs/prod.yml` with selected model details
5. **Testing**: Run tests using `pytest`

### Deployment

Deploy the model API using Docker:

```bash
# Build and run for the first time
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop the service
docker-compose down
```

## Model Registry

The project uses MLflow Model Registry for model lifecycle management:

- **@champion**: Current production model
- **@challenger**: Model being evaluated for production

## API Endpoints

The deployed API provides endpoints for:

- Health checks
- Model predictions
- Model metadata

## Testing

Run the test suite:

```bash
pytest
```

Tests include:

- API endpoint testing
- Model prediction testing
- Data validation testing

## Documentation

For detailed information, see the `docs/` folder:

- [`DEVELOPMENT.md`](docs/DEVELOPMENT.md): Development setup and workflow
- [`DEPLOYMENT.md`](docs/DEPLOYMENT.md): Deployment instructions
- [`STRUCTURE.md`](docs/STRUCTURE.md): Project structure details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## References

- [MLflow Documentation](https://www.mlflow.org/docs/latest/index.html)
- [Kaggle Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

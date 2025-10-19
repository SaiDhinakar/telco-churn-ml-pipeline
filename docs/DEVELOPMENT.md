# Development Guide

## Prerequisites

- Python 3.12
- UV package manager

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/SaiDhinakar/telco-churn-mlops-pipeline
   cd telco-churn-mlops-pipeline
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

## MLflow Setup

1. Start MLflow tracking server:
   ```bash
   mlflow ui
   ```

2. Access the MLflow UI to manage and track model metrics and performance.

## Model Development

### Notebooks

- `preprocessing.ipynb`: Used for exploratory data analysis (EDA), feature engineering, and exporting the cleaned dataset
- `train.ipynb`: Used for training multiple models and tracking model artifacts using MLflow

### Model Management

1. Ensure MLflow is running in the background
2. Use the MLflow UI to create production-ready models
3. Tag models with appropriate aliases (`@challenger`, `@champion`)
4. Update `configs/prod.yml` according to your development requirements

## Testing

Run tests using pytest:
```bash
pytest
```

## Additional Resources

For more information, visit the [MLflow documentation](https://www.mlflow.org/docs/latest/index.html).

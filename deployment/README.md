# Deployment Guide

## Overview

This Docker setup provides a complete MLOps pipeline with:

- **API Service**: FastAPI-based prediction service
- **MLflow Server**: Model tracking and serving
- **Persistent Storage**: Shared volumes for models and logs

## Quick Start

### 1. Build and Start Services

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f api
docker-compose logs -f mlflow
```

### 2. Access Services

- **API Documentation**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5000
- **Health Check**: http://localhost:8000/

### 3. Test Prediction

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "gender": "Male",
       "SeniorCitizen": 0,
       "Partner": "Yes",
       "Dependents": "No",
       "tenure": 12,
       "PhoneService": "Yes",
       "MultipleLines": "No",
       "InternetService": "DSL",
       "OnlineSecurity": "Yes",
       "OnlineBackup": "No",
       "DeviceProtection": "No",
       "TechSupport": "No",
       "StreamingTV": "No",
       "StreamingMovies": "No",
       "Contract": "Month-to-month",
       "PaperlessBilling": "Yes",
       "PaymentMethod": "Electronic check",
       "MonthlyCharges": 29.85,
       "TotalCharges": 358.2
     }'
```

## Configuration

### Environment Variables

- `MLFLOW_TRACKING_URI`: MLflow server URL (default: http://mlflow:5000)
- `CONFIG_ENV`: Configuration environment (docker/prod/dev)
- `PYTHONPATH`: Python module path

### Volume Mounts

- `./logs:/app/logs` - Application logs
- `./mlartifacts:/app/mlartifacts` - MLflow artifacts
- `./mlruns:/app/mlruns` - MLflow runs
- `./configs:/app/configs` - Configuration files

## Troubleshooting

### Service Health Checks

```bash
# Check API health
curl http://localhost:8000/

# View service logs
docker-compose logs api
docker-compose logs mlflow
```

### Common Issues

1. **Port conflicts**: Change ports in docker-compose.yml
2. **Permission issues**: Ensure proper file permissions
3. **Model loading**: Check MLflow connection and model availability

## Production Considerations

- Use production-grade reverse proxy (Nginx)
- Implement proper logging and monitoring
- Use secrets management for sensitive data
- Scale services based on load requirements
- Regular backup of MLflow artifacts and runs

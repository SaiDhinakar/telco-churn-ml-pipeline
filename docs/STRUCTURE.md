```
telco-churn-mlops-pipeline/
│
├── data/                        → Stores all datasets (raw, processed, external, interim)
│
├── notebooks/                   → Jupyter notebooks for EDA, prototyping, and experimentation
│
├── src/                         → Core project source code (all logic for data, models, and pipelines)
│   ├── data_preprocessing/       → Code for data cleaning, encoding, imputation, and splitting
│   ├── features/                 → Feature engineering, transformation, and selection logic
│   ├── models/                   → Model training, evaluation, inference, and saving logic
│   ├── pipelines/                → End-to-end pipeline orchestration (training, inference, retraining)
│   └── utils/                    → Utility functions (logging, config loading, helpers)
│
├── tests/                       → Automated unit, integration, and regression tests for CI/CD
│
├── deployment/                  → Model serving and deployment resources
│   ├── api/                      → API for model inference (FastAPI/Flask)
│   └── scripts/                  → Shell or Python scripts for serving, monitoring, or updating models
│
├── .github/workflows            → Continuous Integration and Deployment workflows
│                                → Contains pipelines for testing, building, and deploying models
│
├── docs/                        → Project documentation, architecture diagrams, and design notes
│
├── configs/                     → Central configuration management for environments or credentials
│
└── monitoring/                  → Model monitoring and drift detection setup (optional but enterprise-grade)
```

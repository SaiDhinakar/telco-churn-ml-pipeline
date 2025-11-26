"""
Model Training Step
This module handles model training with MLflow tracking.
"""

import logging
import os
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import mlflow
import mlflow.sklearn
import mlflow.xgboost
import mlflow.lightgbm

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

models = {
    'logistic_regression': {
        'model': Pipeline([
            ('scaler', StandardScaler()),
            ('logreg', LogisticRegression())
        ]),
        'params': {
            'logreg__C': [0.01, 0.1, 1, 10, 100],
            'logreg__solver': ['liblinear', 'lbfgs']
        }
    },
    'random_forest': {
        'model': RandomForestClassifier(),
        'params': {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30]
        }
    },
    'xgboost': {
        'model': XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        'params': {
            'learning_rate': [0.01, 0.1, 0.2],
            'n_estimators': [50, 100, 200],
            'max_depth': [3, 5, 7]
        }
    },
    'LightGBM': {
        'model': LGBMClassifier(),
        'params': {
            'learning_rate': [0.01, 0.1, 0.2],
            'n_estimators': [50, 100, 200],
            'num_leaves': [31, 50, 100]
        }
    }
}


def load_processed_data(data_path: str) -> pd.DataFrame:
    """
    Load processed data.
    
    Args:
        data_path: Path to processed data
        
    Returns:
        DataFrame containing processed data
    """
    logger.info(f"Loading processed data from: {data_path}")
    df = pd.read_csv(data_path)
    logger.info(f"Loaded data shape: {df.shape}")
    return df


def split_data(
    df: pd.DataFrame,
    target_column: str = 'Churn',
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split data into train and test sets.
    
    Args:
        df: Input DataFrame
        target_column: Name of target column
        test_size: Proportion of test set
        random_state: Random seed
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    logger.info("Splitting data into train and test sets...")
    
    target = df['Churn']
    features = df.drop(columns=['Churn'])
    
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=test_size, random_state=random_state, stratify=target
    )
    
    logger.info(f"Train set size: {X_train.shape[0]}")
    logger.info(f"Test set size: {X_test.shape[0]}")
    
    return X_train, X_test, y_train, y_test


def train_models(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    tracking_uri: str = "http://localhost:5000",
    experiment_name: str = "Telco_Churn_Models"
) -> Dict[str, Dict[str, float]]:
    """
    Train multiple models with GridSearchCV and track with MLflow.
    
    Args:
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
        tracking_uri: MLflow tracking URI
        experiment_name: Name of MLflow experiment
        
    Returns:
        Dictionary of model results
    """
    logger.info("Setting up MLflow...")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    
    results = {}
    
    for model_name, mp in models.items():
        logger.info(f"Training {model_name}...")
        
        # Perform GridSearchCV
        clf = GridSearchCV(
            mp['model'], 
            mp['params'], 
            cv=5, 
            scoring='f1', 
            n_jobs=-1
        )
        clf.fit(X_train, y_train)
        
        # Get best model and predictions
        best_model = clf.best_estimator_
        y_pred = best_model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # Log to MLflow
        with mlflow.start_run(run_name=model_name):
            mlflow.log_param("best_params", clf.best_params_)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("f1_score", f1)
            
            # Log model based on type
            if model_name == 'logistic_regression':
                mlflow.sklearn.log_model(best_model, artifact_path="model")
            elif model_name == 'random_forest':
                mlflow.sklearn.log_model(best_model, artifact_path="model")
            elif model_name == 'xgboost':
                mlflow.xgboost.log_model(best_model, artifact_path="model")
            elif model_name == 'LightGBM':
                mlflow.lightgbm.log_model(best_model, artifact_path="model")
        
        logger.info(f"{model_name} - F1 Score: {f1:.4f}")
        
        results[model_name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'best_params': clf.best_params_
        }
    
    return results


def train_pipeline(
    data_path: Optional[str] = None,
    tracking_uri: Optional[str] = None,
    experiment_name: str = "Telco_Churn_Models"
) -> Dict[str, Dict[str, float]]:
    """
    Main training pipeline with MLflow tracking.
    
    Args:
        data_path: Path to processed data
        tracking_uri: MLflow tracking URI
        experiment_name: Name of MLflow experiment
        
    Returns:
        Dictionary containing training results for all models
    """
    logger.info("Starting training pipeline...")
    
    # Determine project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Default paths
    if data_path is None:
        data_path = os.path.join('data', 'processed', 'cleaned_telco_customer_churn.csv')
    
    if tracking_uri is None:
        tracking_uri = os.getenv(
            'MLFLOW_TRACKING_URI',
            'http://localhost:5000'
        )
    
    try:
        df = load_processed_data(data_path)
        
        X_train, X_test, y_train, y_test = split_data(df)
        
        results = train_models(
            X_train, X_test, y_train, y_test,
            tracking_uri=tracking_uri,
            experiment_name=experiment_name
        )
        
        logger.info("Training pipeline completed successfully!")
        logger.info(f"Trained {len(results)} models")
        
        for model_name, metrics in results.items():
            logger.info(f"{model_name}: F1={metrics['f1_score']:.4f}, Accuracy={metrics['accuracy']:.4f}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        raise


def main():
    """Main execution function."""
    train_pipeline()


if __name__ == "__main__":
    main()

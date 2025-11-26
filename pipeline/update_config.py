"""
Update Configuration Step
This module selects the best model based on accuracy and updates the production config.
"""

import logging
import os
from pathlib import Path
from typing import Dict, Tuple, Optional
import yaml
import mlflow
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_best_models(
    tracking_uri: str = "http://localhost:5000",
    experiment_name: str = "Telco_Churn_Models",
    metric: str = "accuracy"
) -> Tuple[Dict[str, any], Dict[str, any]]:
    """
    Get the best and second-best models based on specified metric.
    
    Args:
        tracking_uri: MLflow tracking URI
        experiment_name: Name of MLflow experiment
        metric: Metric to use for model selection (default: accuracy)
        
    Returns:
        Tuple of (champion_model_info, challenger_model_info)
    """
    logger.info(f"Connecting to MLflow at: {tracking_uri}")
    mlflow.set_tracking_uri(tracking_uri)
    
    # Get experiment
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise ValueError(f"Experiment '{experiment_name}' not found")
    
    logger.info(f"Found experiment: {experiment_name}")
    
    # Search runs and sort by metric
    runs_df = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=[f"metrics.{metric} DESC"]
    )
    
    if runs_df.empty:
        raise ValueError(f"No runs found in experiment '{experiment_name}'")
    
    logger.info(f"Found {len(runs_df)} runs in experiment")
    
    # Get top 2 models
    champion = runs_df.iloc[0]
    challenger = runs_df.iloc[1] if len(runs_df) > 1 else champion
    
    champion_info = {
        'run_id': champion['run_id'],
        'run_name': champion['tags.mlflow.runName'],
        'accuracy': champion[f'metrics.{metric}'],
        'f1_score': champion.get('metrics.f1_score', 0),
        'precision': champion.get('metrics.precision', 0),
        'recall': champion.get('metrics.recall', 0)
    }
    
    challenger_info = {
        'run_id': challenger['run_id'],
        'run_name': challenger['tags.mlflow.runName'],
        'accuracy': challenger[f'metrics.{metric}'],
        'f1_score': challenger.get('metrics.f1_score', 0),
        'precision': challenger.get('metrics.precision', 0),
        'recall': challenger.get('metrics.recall', 0)
    }
    
    logger.info(f"Champion Model: {champion_info['run_name']} - Accuracy: {champion_info['accuracy']:.4f}")
    logger.info(f"Challenger Model: {challenger_info['run_name']} - Accuracy: {challenger_info['accuracy']:.4f}")
    
    return champion_info, challenger_info


def register_models(
    champion_info: Dict[str, any],
    challenger_info: Dict[str, any]
) -> Tuple[str, str]:
    """
    Register models in MLflow Model Registry with aliases.
    
    Args:
        champion_info: Champion model information
        challenger_info: Challenger model information
        
    Returns:
        Tuple of (champion_model_uri, challenger_model_uri)
    """
    logger.info("Registering models in MLflow Model Registry...")
    
    # Register champion model
    champion_model_name = champion_info['run_name']
    champion_model_uri = f"runs:/{champion_info['run_id']}/model"
    
    try:
        champion_version = mlflow.register_model(
            champion_model_uri,
            champion_model_name
        )
        logger.info(f"Registered champion: {champion_model_name} version {champion_version.version}")
        
        # Set alias for champion
        client = mlflow.MlflowClient()
        client.set_registered_model_alias(
            champion_model_name,
            "champion",
            champion_version.version
        )
        logger.info(f"Set alias 'champion' for {champion_model_name}")
        
    except Exception as e:
        logger.warning(f"Model registration/alias failed: {e}")
    
    # Register challenger model
    challenger_model_name = challenger_info['run_name']
    challenger_model_uri = f"runs:/{challenger_info['run_id']}/model"
    
    try:
        challenger_version = mlflow.register_model(
            challenger_model_uri,
            challenger_model_name
        )
        logger.info(f"Registered challenger: {challenger_model_name} version {challenger_version.version}")
        
        # Set alias for challenger
        client.set_registered_model_alias(
            challenger_model_name,
            "challenger",
            challenger_version.version
        )
        logger.info(f"Set alias 'challenger' for {challenger_model_name}")
        
    except Exception as e:
        logger.warning(f"Model registration/alias failed: {e}")
    
    return (
        f"models:/{champion_model_name}@champion",
        f"models:/{challenger_model_name}@challenger"
    )


def update_prod_config(
    champion_uri: str,
    challenger_uri: str,
    config_path: Optional[str] = None
) -> None:
    """
    Update production configuration file with best model URIs.
    
    Args:
        champion_uri: URI of the champion model
        challenger_uri: URI of the challenger model
        config_path: Path to prod.yml config file
        
    Returns:
        None
    """
    # Determine config path
    if config_path is None:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        config_path = project_root / 'configs' / 'prod.yml'
    else:
        config_path = Path(config_path)
    
    logger.info(f"Updating config file: {config_path}")
    
    # Load existing config or create new one
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
    else:
        config = {}
    
    # Update model URIs
    config['model_uri'] = champion_uri
    config['fallback_model_uri'] = challenger_uri
    
    # Ensure other config values exist
    config.setdefault('flavor', 'python_function')
    config.setdefault('mlflow_port', 5000)
    config.setdefault('mlflow_host', '127.0.0.1')
    config.setdefault('api_host', '127.0.0.1')
    config.setdefault('api_port', 8000)
    config.setdefault('workers', 2)
    config.setdefault('timeout', 120)
    
    # Create directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write updated config
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    logger.info("Configuration updated successfully!")
    logger.info(f"  Champion: {champion_uri}")
    logger.info(f"  Challenger: {challenger_uri}")


def update_config_pipeline(
    tracking_uri: Optional[str] = None,
    experiment_name: str = "Telco_Churn_Models",
    metric: str = "accuracy",
    config_path: Optional[str] = None,
    register: bool = True
) -> None:
    """
    Main pipeline to select best model and update production config.
    
    Args:
        tracking_uri: MLflow tracking URI
        experiment_name: Name of MLflow experiment
        metric: Metric to use for model selection
        config_path: Path to prod.yml config file
        register: Whether to register models in MLflow registry
        
    Returns:
        None
    """
    logger.info("Starting config update pipeline...")
    
    # Default tracking URI
    if tracking_uri is None:
        tracking_uri = os.getenv(
            'MLFLOW_TRACKING_URI',
            'http://localhost:5000'
        )
    
    try:
        # Get best models
        champion_info, challenger_info = get_best_models(
            tracking_uri=tracking_uri,
            experiment_name=experiment_name,
            metric=metric
        )
        
        # Register models and get URIs with aliases
        if register:
            champion_uri, challenger_uri = register_models(
                champion_info,
                challenger_info
            )
        else:
            # Use run URIs directly without registration
            champion_uri = f"runs:/{champion_info['run_id']}/model"
            challenger_uri = f"runs:/{challenger_info['run_id']}/model"
        
        # Update production config
        update_prod_config(
            champion_uri=champion_uri,
            challenger_uri=challenger_uri,
            config_path=config_path
        )
        
        logger.info("Config update pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during config update: {str(e)}")
        raise


def main():
    """Main execution function."""
    update_config_pipeline()


if __name__ == "__main__":
    main()

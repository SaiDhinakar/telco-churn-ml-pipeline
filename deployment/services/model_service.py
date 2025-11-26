import mlflow
import os
from configs import get_config, reload_config
import pandas as pd
from utils.logger import setup_logger

models_logger = setup_logger('model_service_logger', 'model_service.log')
model = None
config = get_config()

def initialize_model_service():
    """Initialize and load the ML model from the specified URI."""
    model_uri = config["model_uri"]
    fallback_model_uri = config["fallback_model_uri"]
    print(model_uri, '\n', fallback_model_uri)
    # Check if MLflow server is running, if not use local paths
    mlflow_host = config.get("mlflow_host", "127.0.0.1")
    mlflow_port = config.get("mlflow_port", 5000)
    
    try:
        import requests
        response = requests.get(f"http://{mlflow_host}:{mlflow_port}/health", timeout=2)
        server_running = response.status_code == 200
        models_logger.info(f"MLflow server health check: {server_running}")
    except:
        server_running = False

    if server_running:
        models_logger.info(f"MLflow server detected at {mlflow_host}:{mlflow_port}")
        mlflow.set_tracking_uri(f"http://{mlflow_host}:{mlflow_port}")
        
        try:
            model = mlflow.pyfunc.load_model(model_uri=model_uri)
            models_logger.info(f"Model loaded successfully from {model_uri}")
        except Exception as e:
            models_logger.error(f"Failed to load model from {model_uri}: {e}")
            models_logger.info("Using fallback model...")
            model = mlflow.pyfunc.load_model(model_uri=fallback_model_uri)
            models_logger.info(f"Fallback model loaded from {fallback_model_uri}")
    else:
        models_logger.info("No MLflow server detected, using local artifact paths")
        # Use local artifact paths for model loading
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        
        # LightGBM champion model path (local artifacts)
        champion_model_path = os.path.join(
            project_root, 
            "mlartifacts/878427477543592209/models/m-de9a52a05f5d4977a99cecddac67c397/artifacts"
        )
        
        # XGBoost challenger model path (local artifacts)
        fallback_model_path = os.path.join(
            project_root,
            "mlartifacts/878427477543592209/models/m-3ae216e9f8194d8485da598362f03817/artifacts"
        )
        
        try:
            model = mlflow.pyfunc.load_model(champion_model_path)
            models_logger.info(f"Champion model loaded from local path: {champion_model_path}")
        except Exception as e:
            models_logger.error(f"Failed to load champion model from local path: {e}")
            models_logger.info("Using fallback model...")
            model = mlflow.pyfunc.load_model(fallback_model_path)
            models_logger.info(f"Fallback model loaded from local path: {fallback_model_path}")

    if model is None:
        models_logger.error("Failed to load both champion and fallback models")
        raise RuntimeError("Failed to load both champion and fallback models")

    return model

def predict(data):
    """Make prediction using the loaded model."""
    try:
        # Convert dict to pandas DataFrame if needed
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        
        prediction = model.predict(data)
        models_logger.info(f"Prediction made: {prediction}")
        return prediction[0] if hasattr(prediction, '__len__') and len(prediction) == 1 else prediction
    except Exception as e:
        models_logger.error(f"Prediction error: {e}")
        raise

def get_model():
    """Return the currently loaded model."""
    return model

def restart_model_service():
    """Restart the model service by re-initializing the model."""
    global model
    global config
    
    config = reload_config()
    models_logger.info("Restarting the model service...")
    model = initialize_model_service()
    models_logger.info("Model service restarted successfully.")
    
model = initialize_model_service()
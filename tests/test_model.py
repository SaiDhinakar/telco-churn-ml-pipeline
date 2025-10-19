import mlflow
import pytest
import os
import sys
import requests

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from configs import config

def is_mlflow_server_running(host="127.0.0.1", port=5000):
    """Check if MLflow server is running at the specified host and port."""
    try:
        response = requests.get(f"http://{host}:{port}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def test_model_loading_with_server():
    """Test model loading specifically when MLflow server is expected to be running."""
    mlflow_host = config.get("mlflow_host", "127.0.0.1")
    mlflow_port = config.get("mlflow_port", 5000)
    
    if not is_mlflow_server_running(mlflow_host, mlflow_port):
        pytest.skip(f"MLflow server not running at {mlflow_host}:{mlflow_port}")
    
    # Set up MLflow tracking URI
    mlflow.set_tracking_uri(f"http://{mlflow_host}:{mlflow_port}")
    
    # Test loading champion model from registry
    model = mlflow.pyfunc.load_model(model_uri=config["model_uri"])
    assert model is not None, f"Failed to load champion model: {config['model_uri']}"
    print(f"✅ Successfully loaded champion model from server: {config['model_uri']}")

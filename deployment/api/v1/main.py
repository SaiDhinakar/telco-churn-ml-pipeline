from fastapi import FastAPI, APIRouter, HTTPException
import requests
import os
from dotenv import load_dotenv

from deployment.models.telcom_customer import PredictionRequest, PredictionResponse
from utils.logger import setup_logger
from deployment.services.model_service import predict
from deployment.services.model_service import restart_model_service

load_dotenv()

api_logger = setup_logger('api_logger', 'api.log')

app = FastAPI(title="Telcom Customer Churn Prediction API", version="1.0.0")

# Airflow configuration
AIRFLOW_BASE_URL = os.getenv("AIRFLOW_BASE_URL", "http://localhost:8080")
AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME", "airflow")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD", "airflow")
DAG_ID = "telco_churn_training_pipeline"

@app.get("/")
def root():
    return {
        "message": "Welcome to the Telcom Customer Churn Prediction API",
        "documentation": "Use /docs for API documentation"
        }

router = APIRouter(prefix="/api/v1", tags=["api/v1"])

@router.post("/predict", response_model=PredictionResponse)
def predict_churn(request: PredictionRequest):
    try:
        prediction = predict(request.dict())
        api_logger.info(f"Prediction request: {request.dict()}, Prediction: {prediction}")
        return PredictionResponse(churn_prediction=bool(prediction))
    except Exception as e:
        api_logger.error(f"Error occurred: {e}")
        return {"error": str(e)}

@router.get("/restart")
def restart_service():
    api_logger.info("Restarting the backend service...")
    try:
        restart_model_service()
        api_logger.info("Service restarted successfully.")
        return {"message": "Service restarted."}
    except Exception as e:
        api_logger.error(f"Error during restart: {e}")
        return {"error": str(e)}


@router.post("/trigger-training")
def trigger_training_pipeline():
    """
    Trigger the Airflow ML training pipeline DAG.
    """
    api_logger.info(f"Triggering Airflow DAG: {DAG_ID}")
    
    try:
        # Airflow API endpoint for triggering DAG
        url = f"{AIRFLOW_BASE_URL}/api/v1/dags/{DAG_ID}/dagRuns"
        
        # Payload for triggering the DAG
        payload = {
            "conf": {}  # Optional: add configuration parameters here
        }
        
        # Make request to Airflow API
        response = requests.post(
            url,
            json=payload,
            auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD),
            headers={"Content-Type": "application/json"}
        )
        
        # Check response
        if response.status_code == 200:
            dag_run_data = response.json()
            api_logger.info(f"DAG triggered successfully. Run ID: {dag_run_data.get('dag_run_id')}")
            return {
                "message": "Training pipeline triggered successfully",
                "dag_id": DAG_ID,
                "dag_run_id": dag_run_data.get('dag_run_id'),
                "execution_date": dag_run_data.get('execution_date'),
                "state": dag_run_data.get('state'),
                "airflow_ui": f"{AIRFLOW_BASE_URL}/dags/{DAG_ID}/grid"
            }
        else:
            api_logger.error(f"Failed to trigger DAG. Status: {response.status_code}, Response: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to trigger DAG: {response.text}"
            )
            
    except requests.exceptions.ConnectionError:
        api_logger.error("Cannot connect to Airflow. Make sure Airflow is running.")
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Airflow. Make sure Airflow is running at " + AIRFLOW_BASE_URL
        )
    except Exception as e:
        api_logger.error(f"Error triggering DAG: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/training-status/{dag_run_id}")
def get_training_status(dag_run_id: str):
    """
    Get the status of a specific DAG run.
    """
    api_logger.info(f"Checking status for DAG run: {dag_run_id}")
    
    try:
        url = f"{AIRFLOW_BASE_URL}/api/v1/dags/{DAG_ID}/dagRuns/{dag_run_id}"
        
        response = requests.get(
            url,
            auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD)
        )
        
        if response.status_code == 200:
            dag_run_data = response.json()
            return {
                "dag_id": dag_run_data.get('dag_id'),
                "dag_run_id": dag_run_data.get('dag_run_id'),
                "state": dag_run_data.get('state'),
                "start_date": dag_run_data.get('start_date'),
                "end_date": dag_run_data.get('end_date'),
                "execution_date": dag_run_data.get('execution_date'),
                "airflow_ui": f"{AIRFLOW_BASE_URL}/dags/{DAG_ID}/grid?dag_run_id={dag_run_id}"
            }
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to get DAG status: {response.text}"
            )
            
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Airflow"
        )
    except Exception as e:
        api_logger.error(f"Error getting DAG status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
# Include the router in the app
app.include_router(router)
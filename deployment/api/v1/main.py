from fastapi import FastAPI, APIRouter
from deployment.models.telcom_customer import PredictionRequest, PredictionResponse
from utils.logger import setup_logger
from deployment.services.model_service import predict
from deployment.services.model_service import restart_model_service


api_logger = setup_logger('api_logger', 'api.log')

app = FastAPI(title="Telcom Customer Churn Prediction API", version="1.0.0")

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
    
# Include the router in the app
app.include_router(router)
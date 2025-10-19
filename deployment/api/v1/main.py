from fastapi import FastAPI, APIRouter
from deployment.models.telcom_customer import PredictionRequest, PredictionResponse
from deployment.services import model_service


app = FastAPI(title="Telcom Customer Churn Prediction API", version="1.0.0")

@app.get("/")
def root():
    return {
        "message": "Welcome to the Telcom Customer Churn Prediction API",
        "documentation": "Use /docs for API documentation"
        }

router = APIRouter(prefix="/api/v1", tags=["api/v1"])

sample_data = {
    "SeniorCitizen": 0,
    "Partner": 0,
    "Dependents": 0,
    "tenure": 8,
    "PhoneService": 1,
    "InternetService": 2,
    "OnlineSecurity": 0,
    "OnlineBackup": 0,
    "DeviceProtection": 1,
    "TechSupport": 0,
    "StreamingTV": 1,
    "StreamingMovies": 1,
    "Contract": 0,
    "PaperlessBilling": 1,
    "PaymentMethod": 0,
    "MonthlyCharges": 99.65,
    "TotalCharges": 820.5,
}

@router.post("/predict", response_model=PredictionResponse)
def predict_churn(request: PredictionRequest):
    from deployment.services.model_service import predict
    prediction = predict(request.dict())
    return PredictionResponse(churn_prediction=bool(prediction))

# Include the router in the app
app.include_router(router)
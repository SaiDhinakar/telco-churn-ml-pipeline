from pydantic import BaseModel
from typing import Literal

class PredictionRequest(BaseModel):
    SeniorCitizen: bool
    Partner: bool
    Dependents: bool
    tenure: int
    PhoneService: bool
    InternetService: Literal[0, 1, 2]
    OnlineSecurity: bool
    OnlineBackup: bool
    DeviceProtection: bool
    TechSupport: bool
    StreamingTV: bool
    StreamingMovies: bool
    Contract: Literal[0, 1, 2]
    PaperlessBilling: bool
    PaymentMethod: Literal[0, 1, 2]
    MonthlyCharges: float
    TotalCharges: float

class PredictionResponse(BaseModel):
    churn_prediction: bool
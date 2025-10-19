import pandas as pd
from configs import config
import mlflow


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
							

target = 1  # Expected target value for the sample data

def test_sample_prediction():
    """Test prediction on a sample input using the champion model."""
    # Load the champion model from MLflow
    model = mlflow.pyfunc.load_model(model_uri=config["model_uri"])
    
    # Convert sample data to DataFrame
    sample_df = pd.DataFrame([sample_data])
    
    # Make prediction
    prediction = model.predict(sample_df)
    
    # Check that prediction is valid (e.g., not None and of expected type)
    assert prediction is not None, "Prediction returned None"
    assert len(prediction) == 1, "Prediction output length is not 1"
    assert prediction[0] == target, f"Prediction {prediction[0]} does not match expected target {target}"
    print(f"✅ Sample prediction successful: {prediction[0]}")
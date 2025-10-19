import requests

def test_api_endpoint():
    """Test the API endpoint for model prediction."""
    api_url = "http://localhost:8000/api/v1/predict"
    sample_payload = {
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
    response = requests.post(api_url, json=sample_payload)
    assert response.status_code == 200, f"API request failed with status code {response.status_code}"
    response_json = response.json()
    assert "churn_prediction" in response_json, "Response does not contain 'churn_prediction'"
    print(f"✅ API endpoint test successful: {response_json}")
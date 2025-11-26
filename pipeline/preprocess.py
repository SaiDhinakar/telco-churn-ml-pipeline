"""
Data Preprocessing Step
This module handles data cleaning, feature engineering, and transformation.
"""

import logging
import os
from pathlib import Path
import pandas as pd
from typing import Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_raw_data(raw_data_path: str) -> pd.DataFrame:
    """
    Load raw data from file.
    
    Args:
        raw_data_path: Path to raw data file
        
    Returns:
        DataFrame containing raw data
    """
    logger.info(f"Loading raw data from: {raw_data_path}")
    df = pd.read_csv(raw_data_path)
    logger.info(f"Loaded data shape: {df.shape}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw data.
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    logger.info("Cleaning data...")
    
    df = df.dropna(axis=0)
    cleaned_data = df.drop(columns=["customerID", "gender", "MultipleLines"])
        
    cleaned_df = cleaned_data.copy()
    
    logger.info(f"Data cleaned. Shape after cleaning: {cleaned_df.shape}")
    return cleaned_df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform feature engineering.
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        DataFrame with engineered features
    """
    logger.info("Performing feature engineering...")
    cleaned_data = df.copy()

    cleaned_data['Partner'] = cleaned_data['Partner'].map({'Yes': 1, 'No': 0})
    cleaned_data['Dependents'] = cleaned_data['Dependents'].map({'Yes': 1, 'No': 0})
    cleaned_data['PhoneService'] = cleaned_data['PhoneService'].map({'Yes': 1, 'No': 0})
    cleaned_data['InternetService'] = cleaned_data['InternetService'].map({'No': 0, 'DSL': 1, 'Fiber optic': 2})
    cleaned_data['OnlineSecurity'] = cleaned_data['OnlineSecurity'].map({'Yes': 1, 'No': 0, 'No internet service': 0})
    cleaned_data['OnlineBackup'] = cleaned_data['OnlineBackup'].map({'Yes': 1, 'No': 0, 'No internet service': 0})
    cleaned_data['DeviceProtection'] = cleaned_data['DeviceProtection'].map({'Yes': 1, 'No': 0, 'No internet service': 0})
    cleaned_data['TechSupport'] = cleaned_data['TechSupport'].map({'Yes': 1, 'No': 0, 'No internet service': 0})
    cleaned_data['StreamingTV'] = cleaned_data['StreamingTV'].map({'Yes': 1, 'No': 0, 'No internet service': 0})
    cleaned_data['StreamingMovies'] = cleaned_data['StreamingMovies'].map({'Yes': 1, 'No': 0, 'No internet service': 0})
    cleaned_data['Contract'] = cleaned_data['Contract'].map({'Month-to-month': 0, 'One year': 1, 'Two year': 2})
    cleaned_data['PaperlessBilling'] = cleaned_data['PaperlessBilling'].map({'Yes': 1, 'No': 0})
    cleaned_data['PaymentMethod'] = cleaned_data['PaymentMethod'].map({'Electronic check': 0, 'Mailed check': 1, 'Bank transfer (automatic)': 2, 'Credit card (automatic)': 3})
    cleaned_data['TotalCharges'] = pd.to_numeric(cleaned_data['TotalCharges'], errors='coerce')
    cleaned_data['TotalCharges'].fillna(0, inplace=True)
    cleaned_data['Churn'] = cleaned_data['Churn'].map({'Yes': 1, 'No': 0})
    
    engineered_df = cleaned_data.copy()
    
    logger.info(f"Feature engineering completed. Final shape: {engineered_df.shape}")
    return engineered_df


def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save processed data to file.
    
    Args:
        df: Processed DataFrame
        output_path: Path to save processed data
        
    Returns:
        None
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Processed data saved to: {output_path}")


def preprocess_data(
    raw_data_path: str = None,
    processed_data_path: str = None
) -> None:
    """
    Main preprocessing pipeline.
    
    Args:
        raw_data_path: Path to raw data
        processed_data_path: Path to save processed data
        
    Returns:
        None
    """
    logger.info("Starting data preprocessing pipeline...")
    
    # Default paths
    if raw_data_path is None:
        raw_data_path = os.path.join("data","raw",'telco-customer-churn.csv')
    
    if processed_data_path is None:
        processed_data_path = os.path.join("data","processed",'cleaned_telco_customer_churn.csv')
    
    try:
        # Load raw data
        df = load_raw_data(raw_data_path)
        
        # Clean data
        df = clean_data(df)
        
        # Feature engineering
        df = feature_engineering(df)
        
        # Save processed data
        save_processed_data(df, processed_data_path)
        
        logger.info("Preprocessing pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during preprocessing: {str(e)}")
        raise


def main():
    """Main execution function."""
    preprocess_data()


if __name__ == "__main__":
    main()

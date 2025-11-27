"""
Data Ingestion Step
This module handles data ingestion from various sources.
"""

import os
import shutil
import logging
import kagglehub
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def ingest_data(output_path: str = None) -> str:
    """
    Ingest data from Kaggle and save to raw data directory.
    
    Args:
        output_path: Path to save ingested data. If None, uses default path.
        
    Returns:
        str: Path to the ingested data file
    """
    logger.info("Starting data ingestion...")
    
    # Determine the project root (assuming this script is in pipeline/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Default output path
    if output_path is None:
        output_path = os.path.join('data', 'raw', 'telco-customer-churn.csv')
    
    try:
        # Check if file already exists
        if os.path.exists(output_path):
            logger.info(f"File already exists: {output_path}. Skipping download.")
            return output_path
        
        # Download from Kaggle
        logger.info("Downloading dataset from Kaggle...")
        downloaded_dir_path = kagglehub.dataset_download("blastchar/telco-customer-churn", force_download=False)
        logger.info(f"Dataset downloaded to: {downloaded_dir_path}")
        
        # Create destination directory
        dest_dir = Path(output_path).parent
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Find the CSV file in the downloaded directory
        source_csv_filename = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
        source_csv_path = Path(downloaded_dir_path) / source_csv_filename
        
        if not source_csv_path.exists():
            raise FileNotFoundError(f"Expected CSV file not found: {source_csv_path}")
        
        # Copy the file to the destination
        shutil.copy2(str(source_csv_path), output_path)
        
        logger.info(f"Data ingested successfully. Saved to: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error during data ingestion: {str(e)}")
        raise


def main():
    """Main execution function."""
    ingest_data()


if __name__ == "__main__":
    main()

"""
Telco Churn ML Pipeline DAG
This DAG orchestrates the end-to-end ML training pipeline using Python operators.
"""

import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# Add project path to Python path
sys.path.insert(0, '/opt/airflow/project')

# Import pipeline functions
from pipeline.ingest import ingest_data
from pipeline.preprocess import preprocess_data
from pipeline.train import train_pipeline
from pipeline.update_config import update_config_pipeline


# Default arguments for the DAG
default_args = {
    'owner': 'data-science-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def run_ingest(**context):
    """
    Task to ingest data from Kaggle.
    """
    raw_data_path = '/opt/airflow/project/data/raw/telco-customer-churn.csv'
    result_path = ingest_data(output_path=raw_data_path)
    context['ti'].xcom_push(key='raw_data_path', value=result_path)
    return result_path


def run_preprocess(**context):
    """
    Task to preprocess raw data.
    """
    raw_data_path = context['ti'].xcom_pull(task_ids='ingest_data', key='raw_data_path')
    processed_data_path = '/opt/airflow/project/data/processed/cleaned_telco_customer_churn.csv'
    
    result_path = preprocess_data(
        input_path=raw_data_path,
        output_path=processed_data_path
    )
    context['ti'].xcom_push(key='processed_data_path', value=result_path)
    return result_path


def run_train(**context):
    """
    Task to train multiple models.
    """
    processed_data_path = context['ti'].xcom_pull(task_ids='preprocess_data', key='processed_data_path')
    
    results = train_pipeline(
        data_path=processed_data_path,
        tracking_uri='/opt/airflow/project/mlruns',
        experiment_name='Telco_Churn_Models'
    )
    
    context['ti'].xcom_push(key='training_results', value=results)
    return results


def run_update_config(**context):
    """
    Task to select best model and update config.
    """
    update_config_pipeline(
        tracking_uri='/opt/airflow/project/mlruns',
        experiment_name='Telco_Churn_Models',
        metric='accuracy',
        config_path='/opt/airflow/project/configs/prod.yml',
        register=True
    )
    return "Config updated successfully"


# Define the DAG
with DAG(
    dag_id='telco_churn_training_pipeline',
    default_args=default_args,
    description='End-to-end ML training pipeline for telco churn prediction',
    schedule_interval=None,  # Manual trigger or set to '@daily', '@weekly', etc.
    start_date=days_ago(1),
    catchup=False,
    tags=['ml', 'training', 'telco-churn'],
) as dag:

    # Task 1: Data Ingestion
    ingest_task = PythonOperator(
        task_id='ingest_data',
        python_callable=run_ingest,
        provide_context=True,
    )

    # Task 2: Data Preprocessing
    preprocess_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=run_preprocess,
        provide_context=True,
    )

    # Task 3: Model Training
    train_task = PythonOperator(
        task_id='train_model',
        python_callable=run_train,
        provide_context=True,
    )

    # Task 4: Update Configuration
    update_config_task = PythonOperator(
        task_id='update_config',
        python_callable=run_update_config,
        provide_context=True,
    )

    # Define task dependencies
    ingest_task >> preprocess_task >> train_task >> update_config_task

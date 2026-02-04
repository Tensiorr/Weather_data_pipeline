from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

import sys

sys.path.insert(0, '/opt/airflow')
from src.pipeline import extract_data, transform_data, load_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
        'weather_etl_pipeline',
        default_args=default_args,
        description='ETL pipeline for weather data',
        schedule_interval='@hourly',
        start_date=datetime(2026, 1, 1),
        catchup=False,
        tags=['weather', 'etl'],
) as dag:
    # Task 1: Extract
    extract_task = PythonOperator(
        task_id='extract_weather_data',
        python_callable=extract_data,
    )

    # Task 2: Transform
    transform_task = PythonOperator(
        task_id='transform_weather_data',
        python_callable=transform_data,
    )

    # Task 3: Load
    load_task = PythonOperator(
        task_id='load_weather_data',
        python_callable=load_data,
    )

    extract_task >> transform_task >> load_task

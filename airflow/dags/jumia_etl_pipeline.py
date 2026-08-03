from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from etl.extract import extract_data
from etl.load_staging import load_staging
from etl.clean_data import clean_data
from etl.transform import transform
from etl.load_warehouse import load_datawarehouse

default_args = {
    "owner": "Fatima",
    "depends_on_past": False,
    "retries": 1,
}

FILE_PATH = "/opt/airflow/data/raw/jumia_products.csv"


with DAG(
    dag_id="jumia_etl_pipeline",
    description="Pipeline ETL Jumia",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["Jumia", "ETL", "Data Warehouse"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
        op_kwargs={
            "file_path": FILE_PATH
        },
    )

    load_staging_task = PythonOperator(
        task_id="load_staging",
        python_callable=load_staging,
        op_kwargs={
            "file_path": FILE_PATH
        },
    )

    clean_task = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform,
    )

    load_dw_task = PythonOperator(
        task_id="load_datawarehouse",
        python_callable=load_datawarehouse,
    )

    (
        extract_task
        >> load_staging_task
        >> clean_task
        >> transform_task
        >> load_dw_task
    )
    
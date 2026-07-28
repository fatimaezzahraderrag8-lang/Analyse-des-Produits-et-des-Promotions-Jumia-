from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


default_args = {
    "owner": "fatima",
    "retries": 1,
}


with DAG(
    dag_id="jumia_etl_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["ETL", "Jumia"],
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="cd /opt/airflow && python etl/extract.py",
    )

    load_staging = BashOperator(
        task_id="load_staging",
        bash_command="cd /opt/airflow && python etl/load_staging.py",
    )

    clean = BashOperator(
        task_id="clean_data",
        bash_command="cd /opt/airflow && python etl/clean_data.py",
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="cd /opt/airflow && python etl/transform.py",
    )

    warehouse = BashOperator(
        task_id="load_warehouse",
        bash_command="cd /opt/airflow && python etl/load_warehouse.py",
    )


    extract >> load_staging >> clean >> transform >> warehouse
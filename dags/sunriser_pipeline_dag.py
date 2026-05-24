from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "tran-dai-hai",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="sunriser_game_analytics_pipeline",
    default_args=default_args,
    description="Raw to Bronze to Silver to Power BI fact table pipeline",
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["sunriser", "game-analytics", "data-engineering"],
) as dag:

    ingest_raw_to_bronze = BashOperator(
        task_id="ingest_raw_to_bronze",
        bash_command="cd /opt/airflow && python src/ingest_raw_to_bronze.py",
    )

    bronze_to_silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command="cd /opt/airflow && python src/bronze_to_silver_pandas.py",
    )

    validate_silver_quality = BashOperator(
    task_id="validate_silver_quality",
    bash_command="cd /opt/airflow && python src/validate_silver_quality.py",
    )

    silver_to_powerbi = BashOperator(
        task_id="silver_to_powerbi_fact_events",
        bash_command="cd /opt/airflow && python src/silver_to_gold_pandas.py",
    )

    ingest_raw_to_bronze >> bronze_to_silver >> validate_silver_quality >> silver_to_powerbi
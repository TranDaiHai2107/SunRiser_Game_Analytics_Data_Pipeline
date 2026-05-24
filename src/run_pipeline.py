from ingest_raw_to_bronze import main as ingest_raw_to_bronze
from bronze_to_silver_pandas import main as bronze_to_silver
from silver_to_gold_pandas import main as silver_to_gold


def main():
    print("Step 1: Ingest raw to bronze")
    ingest_raw_to_bronze()

    print("Step 2: Transform bronze to silver")
    bronze_to_silver()

    print("Step 3: Export Power BI fact table")
    silver_to_gold()

    print("Pipeline completed successfully")


if __name__ == "__main__":
    main()
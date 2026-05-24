# Pipeline Steps

This document explains each step in the current ETL pipeline.

## 1. Ingest Raw to Bronze

Script:

```text
src/ingest_raw_to_bronze.py
```

Input:

```text
data/raw/Intern Test Data - Data.csv
```

Output:

```text
data/bronze/game_events_bronze.csv
```

Purpose:

- Read the original raw CSV.
- Add ingestion metadata.
- Save a Bronze copy for downstream processing.

## 2. Transform Bronze to Silver

Script:

```text
src/bronze_to_silver_pandas.py
```

Input:

```text
data/bronze/game_events_bronze.csv
```

Output:

```text
data/silver/game_events_clean/part-00000.parquet
```

Purpose:

- Standardize data types.
- Convert timestamp from microseconds to datetime.
- Create date and hour fields.
- Remove duplicate rows.
- Create event-level flags.
- Save clean data as Parquet.

## 3. Validate Silver Data

Script:

```text
src/validate_silver_quality.py
```

Input:

```text
data/silver/game_events_clean/part-00000.parquet
```

Purpose:

- Check that the Silver table is not empty.
- Check required columns.
- Validate event names.
- Validate binary flag columns.
- Validate basic event logic.

If validation fails, the pipeline stops before exporting the Power BI table.

## 4. Export Power BI Fact Table

Script:

```text
src/silver_to_gold_pandas.py
```

Input:

```text
data/silver/game_events_clean/part-00000.parquet
```

Output:

```text
powerbi_exports/sunriser_powerbi_fact_events.csv
```

Purpose:

- Select the final analytics-ready columns.
- Sort events by user and event time.
- Export a single CSV file for Power BI.

## 5. Airflow Orchestration

DAG:

```text
dags/sunriser_pipeline_dag.py
```

Task order:

```text
ingest_raw_to_bronze
  -> bronze_to_silver
  -> validate_silver_quality
  -> silver_to_powerbi_fact_events
```

Purpose:

- Run each pipeline step as a separate monitored task.
- Make failures visible in Airflow UI.
- Allow manual triggering and future scheduling.

## 6. Docker Execution

Local pipeline:

```bash
docker compose up --build
```

Airflow pipeline:

```bash
docker compose -f docker-compose.airflow.yml up
```

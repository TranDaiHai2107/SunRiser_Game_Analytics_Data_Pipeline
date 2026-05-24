# Architecture

This project follows a medallion-style batch ETL architecture. The goal is to transform raw game event data into a clean fact table that can be used directly in Power BI.

## High-Level Flow

```text
Raw CSV
  -> Bronze Layer
  -> Silver Layer
  -> Data Quality Check
  -> Power BI Export
```

## Raw Layer

The Raw layer stores the original source file exactly as received.

Example:

```text
data/raw/Intern Test Data - Data.csv
```

No transformation is applied in this layer. This makes it possible to trace all downstream outputs back to the original source file.

## Bronze Layer

The Bronze layer stores ingested raw data with lightweight metadata.

Typical metadata includes:

- `ingestion_time`
- `source_file`

The Bronze layer is still close to the raw source. It is useful for replaying or debugging the pipeline.

## Silver Layer

The Silver layer contains cleaned event-level data.

Main transformations:

- Convert `event_timestamp` from microseconds to timestamp.
- Create `event_time`, `event_date`, and `event_hour`.
- Cast numeric columns such as `level`, `app_version`, `time_played`, and `batch_event_index`.
- Standardize success values into boolean/text fields.
- Remove duplicate rows.
- Create helper flags such as `start_flag`, `end_flag`, `attempt_flag`, `success_flag`, and `fail_flag`.

The Silver layer is the main trusted dataset for downstream analytics.

## Data Quality Layer

Before exporting data to Power BI, the pipeline runs data quality checks on the Silver layer.

The checks are designed to prevent broken or incomplete data from reaching the BI layer.

Examples:

- Required columns must exist.
- Event names must be valid.
- Flag columns must be binary.
- `level_end` rows must have `attempt_flag = 1`.
- `level_start` rows must have `attempt_flag = 0`.

If any check fails, the Airflow task fails and the final export is not produced.

## BI Export Layer

The final BI layer exports one analytics-ready fact table:

```text
powerbi_exports/sunriser_powerbi_fact_events.csv
```

This table is imported into Power BI and used to create DAX metrics for level drop-off, success rate, retry behavior, and difficulty analysis.

## Orchestration

Apache Airflow orchestrates the pipeline using a DAG with four main tasks:

```text
ingest_raw_to_bronze
  -> bronze_to_silver
  -> validate_silver_quality
  -> silver_to_powerbi_fact_events
```

## Deployment

Docker and Docker Compose are used to make the pipeline reproducible across environments.

There are two main execution modes:

- `docker-compose.yml`: runs the local Python pipeline.
- `docker-compose.airflow.yml`: runs Airflow webserver, scheduler, metadata database, and DAG tasks.

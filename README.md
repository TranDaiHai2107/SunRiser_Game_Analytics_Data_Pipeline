# SunRiser Game Analytics Data Pipeline

## Project Overview

SunRiser is a game analytics data engineering project that transforms raw gameplay event logs into an analytics-ready fact table for Power BI.

The project started as an exploratory game case study and was extended into a local batch ETL pipeline with Docker, Airflow orchestration, data quality checks, and Power BI reporting.

## Case Study Objective

The original case study focuses on analyzing user progression across game levels. The goal is to identify levels with potential gameplay issues and provide suitable visualizations to monitor those issues.

The analysis answers three main questions:

- Which levels have high player drop-off?
- Which levels are unusually difficult or frustrating?
- How should these issues be monitored in Power BI?

## Business Context

The dataset contains gameplay events from users progressing through different levels. Each event is either a `level_start` or `level_end` event.

Important fields include:

- User and session identifiers
- Event timestamp
- Event name
- App version
- Level
- Time played
- Success result
- Game mode
- Country
- Device and operating system

The final Power BI dashboard uses the cleaned event-level table to analyze drop-off, success rate, retry behavior, and level difficulty.

## Key Insights from the Analysis

The final analysis report is available at:

```text
reports/pdf/SunRiser_Analysis_Report.pdf
```

Main findings:

- Overall success rate is around **74.27%**, which suggests that the game is generally playable across the analyzed levels.
- The data is concentrated mostly on **Mobile**, while Desktop and Tablet represent smaller user groups and should not be treated as equally representative.
- There is a major funnel issue from **Start Level** to **Attempt Level**.
- **Level 1 has an in-level drop-off rate of about 49.85%**, meaning almost half of users who start Level 1 do not continue into the next meaningful attempt/progression step.
- Platform filtering suggests that the Level 1 problem is not purely a device issue. Desktop drop-off is even higher than Mobile, so the issue is more likely related to onboarding, tutorial design, or early game experience.
- **Post-success drop-off between Level 3 and Level 4 is around 37-40%**, meaning many users win but still do not continue. This points to a weak reward loop or lack of motivation to proceed.
- There is a visible traffic spike around **15/02**, likely caused by a campaign, update, or in-game event. After that point, the trend declines, suggesting lower retention after the spike.
- Levels around **38-42** show a mid-game break point where continuation drops sharply.
- Levels after **50** show unstable continuation behavior, which may indicate inconsistent level design quality.
- Levels around **70-94** are difficult in the traditional sense, with fail rates reaching around **60%**.
- **Level 2 is a high-priority issue** because fail rate is around **54%** while average play time is short, suggesting that new users may fail too quickly before understanding the game.
- Levels **50-60** are not necessarily hard, but they appear long and may cause fatigue, especially for mobile players.

## Recommended Actions

Based on the analysis:

- Redesign Level 1 onboarding and tutorial flow to reduce early drop-off.
- Improve the reward loop after early successful levels, especially around Level 3-4.
- Review Level 2 map design because players may be failing too quickly.
- Rebalance difficult levels around Level 70+.
- Review long but easy levels around Level 50-60 to reduce player fatigue.
- Monitor drop-off, success rate, attempts per user, and median time by level in Power BI.

## Current Tech Stack

- Python / pandas
- Apache Airflow
- Docker / Docker Compose
- Power BI
- GitHub

## Current Pipeline Architecture

```text
Raw CSV
  -> Bronze Layer
  -> Silver Layer
  -> Data Quality Check
  -> Power BI fact table
```

## ETL Design

This project is currently a local batch ETL pipeline.

```text
Extract:
Read raw CSV game event logs.

Transform:
Clean and standardize the data with Python, convert timestamps, remove duplicates, and create event flags.

Load:
Export one analytics-ready CSV fact table for Power BI.
```

## Folder Structure

```text
dags/
  sunriser_pipeline_dag.py

data/
  raw/
  bronze/
  silver/

docs/
  architecture.md
  data_dictionary.md
  pipeline_steps.md

reports/
  pdf/
    SunRiser_Analysis_Report.pdf
  powerbi/
    Report_SunRiser-Tran Dai Hai.pbix

src/
  ingest_raw_to_bronze.py
  bronze_to_silver_pandas.py
  validate_silver_quality.py
  silver_to_gold_pandas.py
  run_pipeline.py

powerbi_exports/
  sunriser_powerbi_fact_events.csv
```

> Note: The `data/` and `powerbi_exports/` folders are excluded from version control because they contain raw/intermediate/output data files.

## Pipeline Layers

### Raw Layer

Stores the original source CSV without modification.

### Bronze Layer

Stores ingested raw data with additional ingestion metadata such as ingestion time and source file.

### Silver Layer

Stores cleaned event-level data. This layer standardizes schema, converts timestamps, removes duplicate rows, and creates helper flags.

### Data Quality Layer

Validates the Silver dataset before exporting data to Power BI.

### BI Export Layer

Exports the final analytics-ready fact table:

```text
powerbi_exports/sunriser_powerbi_fact_events.csv
```

This file is imported into Power BI and used to create DAX metrics.

## Airflow DAG

The Airflow DAG contains four main tasks:

```text
ingest_raw_to_bronze
  -> bronze_to_silver
  -> validate_silver_quality
  -> silver_to_powerbi_fact_events
```

## Data Quality Checks

The pipeline validates that:

- The Silver table is not empty.
- Required columns exist.
- `event_name` only contains `level_start` and `level_end`.
- `level` is mostly non-null.
- `event_timestamp` is mostly non-null.
- Flag columns only contain `0` or `1`.
- `level_end` rows have `attempt_flag = 1`.
- `level_start` rows have `attempt_flag = 0`.

## Power BI Metrics Supported

The exported fact table supports DAX metrics such as:

- Total Users
- Level Starts
- Level Ends
- Total Attempts
- Success Rate
- Fail Rate
- Completion Rate
- Drop-off Rate
- Attempts per User
- Average Time Played
- Median Time Played

## Reports

The project includes reporting artifacts:

```text
reports/pdf/SunRiser_Analysis_Report.pdf
reports/powerbi/Report_SunRiser-Tran Dai Hai.pbix
```

The PDF report summarizes the main insights and recommendations from the Power BI analysis.

## How to Run with Docker

Build and run the local pipeline:

```bash
docker compose up --build
```

Expected output:

```text
powerbi_exports/sunriser_powerbi_fact_events.csv
```

## How to Run with Airflow

Start Airflow services:

```bash
docker compose -f docker-compose.airflow.yml up
```

Open Airflow UI:

```text
http://localhost:8080
```

Default login:

```text
username: admin
password: admin
```

Trigger DAG:

```text
sunriser_game_analytics_pipeline
```

## Future Improvements

Planned improvements:

- Add Azure Data Lake Storage Gen2 for cloud storage.
- Add dbt for SQL-based Gold models and documentation.
- Replace pandas transformation with Spark for scalable processing.
- Add Kafka to simulate streaming game telemetry events.

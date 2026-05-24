from pathlib import Path

import pandas as pd


SILVER_PATH = Path("data/silver/game_events_clean/part-00000.parquet")
POWERBI_DIR = Path("powerbi_exports")
POWERBI_FACT_EVENTS_PATH = POWERBI_DIR / "sunriser_powerbi_fact_events.csv"

POWERBI_COLUMNS = [
    "user_id",
    "session_id",
    "event_timestamp",
    "event_time",
    "event_date",
    "event_hour",
    "batch_event_index",
    "event_name",
    "start_flag",
    "end_flag",
    "attempt_flag",
    "app_version",
    "app_version_text",
    "level",
    "level_text",
    "time_played",
    "time_played_p99_cap",
    "is_success_bool",
    "is_success_text",
    "success_flag",
    "fail_flag",
    "country",
    "game_mode",
    "device_category",
    "mobile_brand_name",
    "operating_system",
]


def add_powerbi_columns(df: pd.DataFrame) -> pd.DataFrame:
    fact_events = df.copy()

    if "time_played_p99_cap" not in fact_events.columns:
        p99_time = fact_events["time_played"].quantile(0.99)
        fact_events["time_played_p99_cap"] = fact_events["time_played"].clip(
            upper=p99_time
        )

    fact_events["app_version_text"] = fact_events["app_version"].astype("string")
    fact_events["level_text"] = fact_events["level"].astype("string")
    fact_events["is_success_text"] = (
        fact_events["is_success_bool"]
        .map({True: "Success", False: "Fail"})
        .fillna("Not applicable")
    )

    return fact_events


def validate_columns(df: pd.DataFrame) -> None:
    missing_columns = [col for col in POWERBI_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def main() -> None:
    if not SILVER_PATH.exists():
        raise FileNotFoundError(f"Silver file not found: {SILVER_PATH}")

    POWERBI_DIR.mkdir(parents=True, exist_ok=True)

    fact_events = pd.read_parquet(SILVER_PATH)
    fact_events = add_powerbi_columns(fact_events)
    validate_columns(fact_events)

    fact_events = fact_events[POWERBI_COLUMNS].sort_values(
        ["user_id", "event_time", "batch_event_index"]
    )

    fact_events.to_csv(
        POWERBI_FACT_EVENTS_PATH,
        index=False,
        encoding="utf-8-sig",
    )

    print("Power BI fact table created:", POWERBI_FACT_EVENTS_PATH)
    print("Rows:", len(fact_events))
    print("Columns:", len(fact_events.columns))
    print("Users:", fact_events["user_id"].nunique())
    print("Levels:", fact_events["level"].nunique())


if __name__ == "__main__":
    main()

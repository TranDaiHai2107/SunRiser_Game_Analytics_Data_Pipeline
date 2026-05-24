from pathlib import Path
import pandas as pd

BRONZE_PATH = Path("data/bronze/game_events_bronze.csv")
SILVER_DIR = Path("data/silver/game_events_clean")
SILVER_PATH = SILVER_DIR / "part-00000.parquet"
SUCCESS_PATH = SILVER_DIR / "_SUCCESS"

def main():
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(
        BRONZE_PATH,
        dtype={
            "user_id": "string",
            "session_id": "string",
            "event_name": "string",
            "country": "string",
            "game_mode": "string",
            "device_category": "string",
            "mobile_brand_name": "string",
            "operating_system": "string",
        },
    )

    df["event_timestamp"] = pd.to_numeric(df["event_timestamp"], errors="coerce")
    df["event_time"] = pd.to_datetime(df["event_timestamp"], unit="us", errors="coerce")
    df["event_date"] = df["event_time"].dt.date.astype("string")
    df["event_hour"] = df["event_time"].dt.hour

    df["batch_event_index"] = pd.to_numeric(df["batch_event_index"], errors="coerce").astype("Int64")
    df["app_version"] = pd.to_numeric(df["app_version"], errors="coerce").astype("Int64")
    df["level"] = pd.to_numeric(df["level"], errors="coerce").astype("Int64")
    df["time_played"] = pd.to_numeric(df["time_played"], errors="coerce")

    df["is_success_bool"] = (
        df["is_success"]
        .astype("string")
        .str.upper()
        .map({"TRUE": True, "FALSE": False})
    )

    df = df.drop_duplicates()
    df = df.dropna(subset=["event_name", "level"])

    df["user_id"] = df["user_id"].fillna("Unknown")
    df["session_id"] = df["session_id"].fillna("Unknown")

    df["start_flag"] = (df["event_name"] == "level_start").astype(int)
    df["end_flag"] = (df["event_name"] == "level_end").astype(int)
    df["attempt_flag"] = df["end_flag"]

    df["success_flag"] = (
        (df["event_name"] == "level_end") &
        (df["is_success_bool"] == True)
    ).astype(int)

    df["fail_flag"] = (
        (df["event_name"] == "level_end") &
        (df["is_success_bool"] == False)
    ).astype(int)

    df["is_success_text"] = df["is_success_bool"].map(
        {True: "Success", False: "Fail"}
    ).fillna("Not applicable")

    p99_time = df["time_played"].quantile(0.99)
    df["time_played_p99_cap"] = df["time_played"].clip(upper=p99_time)

    df["app_version_text"] = df["app_version"].astype("string")
    df["level_text"] = df["level"].astype("string")

    df.to_parquet(SILVER_PATH, index=False)
    SUCCESS_PATH.write_text("SUCCESS", encoding="utf-8")

    print("Silver layer created:", SILVER_PATH)
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

if __name__ == "__main__":
    main()
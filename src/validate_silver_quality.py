from pathlib import Path
import pandas as pd


SILVER_PATH = Path("data/silver/game_events_clean/part-00000.parquet")


def assert_condition(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main():
    if not SILVER_PATH.exists():
        raise FileNotFoundError(f"Silver file not found: {SILVER_PATH}")

    df = pd.read_parquet(SILVER_PATH)

    assert_condition(len(df) > 0, "Silver table is empty")

    required_columns = [
        "user_id",
        "session_id",
        "event_timestamp",
        "event_time",
        "event_name",
        "level",
        "start_flag",
        "end_flag",
        "success_flag",
        "fail_flag",
        "attempt_flag",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    assert_condition(
        len(missing_columns) == 0,
        f"Missing required columns: {missing_columns}",
    )

    valid_event_names = {"level_start", "level_end"}
    invalid_events = set(df["event_name"].dropna().unique()) - valid_event_names
    assert_condition(
        len(invalid_events) == 0,
        f"Invalid event_name values: {invalid_events}",
    )

    assert_condition(
        df["level"].notna().mean() >= 0.95,
        "More than 5% of rows have missing level",
    )

    assert_condition(
        df["event_timestamp"].notna().mean() >= 0.99,
        "More than 1% of rows have missing event_timestamp",
    )

    flag_columns = ["start_flag", "end_flag", "success_flag", "fail_flag", "attempt_flag"]
    for col in flag_columns:
        invalid_values = set(df[col].dropna().unique()) - {0, 1}
        assert_condition(
            len(invalid_values) == 0,
            f"{col} contains non-binary values: {invalid_values}",
        )

    level_end = df[df["event_name"] == "level_end"]

    assert_condition(
        (level_end["attempt_flag"] == 1).all(),
        "All level_end rows must have attempt_flag = 1",
    )

    assert_condition(
        (df[df["event_name"] == "level_start"]["attempt_flag"] == 0).all(),
        "All level_start rows must have attempt_flag = 0",
    )

    print("Silver data quality checks passed")
    print("Rows:", len(df))
    print("Users:", df["user_id"].nunique())
    print("Levels:", df["level"].nunique())


if __name__ == "__main__":
    main()
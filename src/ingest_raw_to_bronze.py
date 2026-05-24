from pathlib import Path
from datetime import datetime
import pandas as pd

RAW_PATH = Path("data/raw/Intern Test Data - Data.csv")
BRONZE_DIR = Path("data/bronze")
BRONZE_PATH = BRONZE_DIR / "game_events_bronze.csv"

def main():
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_PATH)
    df["ingestion_time"] = datetime.now().isoformat(timespec="seconds")
    df["source_file"] = RAW_PATH.name

    df.to_csv(BRONZE_PATH, index=False, encoding="utf-8-sig")

    print(f"Bronze file created: {BRONZE_PATH}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")

if __name__ == "__main__":
    main()
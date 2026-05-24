from pyspark.sql import SparkSession
from pyspark.sql import functions as F

BRONZE_PATH = "data/bronze/game_events_bronze.csv"
SILVER_PATH = "data/silver/game_events_clean"

def main():
    spark = (
        SparkSession.builder
        .appName("SunRiser Bronze to Silver")
        .getOrCreate()
    )

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(BRONZE_PATH)
    )

    silver_df = (
        df
        .dropDuplicates()
        .withColumn("event_timestamp", F.col("event_timestamp").cast("long"))
        .withColumn("batch_event_index", F.col("batch_event_index").cast("int"))
        .withColumn("app_version", F.col("app_version").cast("int"))
        .withColumn("session_id", F.col("session_id").cast("string"))
        .withColumn("user_id", F.col("user_id").cast("string"))
        .withColumn("level", F.col("level").cast("int"))
        .withColumn("time_played", F.col("time_played").cast("double"))
        .withColumn(
            "event_time",
            F.to_timestamp(F.from_unixtime(F.col("event_timestamp") / 1000000))
        )
        .withColumn("event_date", F.to_date("event_time"))
        .withColumn("event_hour", F.hour("event_time"))
        .withColumn(
            "is_success_bool",
            F.when(F.upper(F.col("is_success")) == "TRUE", F.lit(True))
             .when(F.upper(F.col("is_success")) == "FALSE", F.lit(False))
             .otherwise(F.lit(None))
        )
        .withColumn(
            "start_flag",
            F.when(F.col("event_name") == "level_start", 1).otherwise(0)
        )
        .withColumn(
            "end_flag",
            F.when(F.col("event_name") == "level_end", 1).otherwise(0)
        )
        .withColumn(
            "attempt_flag",
            F.when(F.col("event_name") == "level_end", 1).otherwise(0)
        )
        .withColumn(
            "success_flag",
            F.when(
                (F.col("event_name") == "level_end") &
                (F.col("is_success_bool") == True),
                1
            ).otherwise(0)
        )
        .withColumn(
            "fail_flag",
            F.when(
                (F.col("event_name") == "level_end") &
                (F.col("is_success_bool") == False),
                1
            ).otherwise(0)
        )
    )

    (
        silver_df
        .write
        .mode("overwrite")
        .parquet(SILVER_PATH)
    )

    print("Silver layer created:", SILVER_PATH)
    print("Rows:", silver_df.count())
    print("Columns:", len(silver_df.columns))

    spark.stop()

if __name__ == "__main__":
    main()
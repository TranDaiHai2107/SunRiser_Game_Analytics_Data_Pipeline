# Data Dictionary

This document describes the main fields in the final Power BI fact table:

```text
powerbi_exports/sunriser_powerbi_fact_events.csv
```

## Identifier Columns

| Column | Description |
|---|---|
| `user_id` | Unique identifier of the user. |
| `session_id` | Identifier of the game session. |
| `event_timestamp` | Original event timestamp in microseconds. |
| `batch_event_index` | Ordering index when multiple events share the same timestamp. |

## Time Columns

| Column | Description |
|---|---|
| `event_time` | Converted timestamp from `event_timestamp`. |
| `event_date` | Date extracted from `event_time`. |
| `event_hour` | Hour extracted from `event_time`. |

## Event Columns

| Column | Description |
|---|---|
| `event_name` | Event type. Expected values are `level_start` and `level_end`. |
| `level` | Game level number. |
| `level_text` | Level converted to text for Power BI labels. |
| `app_version` | Application version. |
| `app_version_text` | App version converted to text for Power BI labels. |

## Gameplay Columns

| Column | Description |
|---|---|
| `time_played` | Time played in seconds. Mostly available for `level_end` events. |
| `time_played_p99_cap` | Time played capped at p99 to reduce outlier impact in visuals. |
| `is_success_bool` | Boolean result for `level_end`: true if user won the level, false if user failed. |
| `is_success_text` | Text result: `Success`, `Fail`, or `Not applicable`. |

## Flag Columns

| Column | Description |
|---|---|
| `start_flag` | 1 if the row is a `level_start` event, otherwise 0. |
| `end_flag` | 1 if the row is a `level_end` event, otherwise 0. |
| `attempt_flag` | 1 if the row is a `level_end` event. Used to count attempts. |
| `success_flag` | 1 if the row is a successful `level_end`, otherwise 0. |
| `fail_flag` | 1 if the row is a failed `level_end`, otherwise 0. |

## User Segment Columns

| Column | Description |
|---|---|
| `country` | User country. |
| `game_mode` | Game mode. |
| `device_category` | Device category such as desktop, mobile, or tablet. |
| `mobile_brand_name` | Device brand name. |
| `operating_system` | User operating system. |

## Suggested Power BI Measures

```DAX
Total Attempts = SUM(sunriser_powerbi_fact_events[attempt_flag])
```

```DAX
Level Starts = SUM(sunriser_powerbi_fact_events[start_flag])
```

```DAX
Level Ends = SUM(sunriser_powerbi_fact_events[end_flag])
```

```DAX
Success Attempts = SUM(sunriser_powerbi_fact_events[success_flag])
```

```DAX
Fail Attempts = SUM(sunriser_powerbi_fact_events[fail_flag])
```

```DAX
Success Rate = DIVIDE([Success Attempts], [Total Attempts])
```

```DAX
Fail Rate = DIVIDE([Fail Attempts], [Total Attempts])
```

```DAX
Completion Rate = DIVIDE([Level Ends], [Level Starts])
```

```DAX
Drop-off Rate = 1 - [Completion Rate]
```

```DAX
Total Users = DISTINCTCOUNT(sunriser_powerbi_fact_events[user_id])
```

```DAX
Attempts per User = DIVIDE([Total Attempts], [Total Users])
```

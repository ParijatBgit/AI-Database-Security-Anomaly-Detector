import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
data_dir = project_root / "data" / "generated" / "oracle_extract"
users = pd.read_csv(data_dir / "db_users.csv")
logins = pd.read_csv(data_dir / "login_history.csv")
failures = pd.read_csv(data_dir / "login_failures.csv")
queries = pd.read_csv(data_dir / "query_logs.csv")
logins["login_time"] = pd.to_datetime(logins["login_time"])
logins["logout_time"] = pd.to_datetime(logins["logout_time"])
failures["attempt_time"] = pd.to_datetime(failures["attempt_time"])
queries["execution_time"] = pd.to_datetime(queries["execution_time"])
logins["hour_window"] = logins["login_time"].dt.floor("h")
failures["hour_window"] = failures["attempt_time"].dt.floor("h")
queries["hour_window"] = queries["execution_time"].dt.floor("h")
valid_users = set(users["user_id"].astype(int))
logins = logins[logins["user_id"].isin(valid_users)]
queries = queries[queries["user_id"].isin(valid_users)]
failures = failures[
    failures["user_id"].notna() &
    failures["user_id"].isin(valid_users)
].copy()

login_groups = {
    key: group for key, group in
    logins.groupby(["user_id", "hour_window"])
}
failure_groups = {
    key: group for key, group in
    failures.groupby(["user_id", "hour_window"])
}
query_groups = {
    key: group for key, group in
    queries.groupby(["user_id", "hour_window"])
}
all_keys = (
    set(login_groups.keys()) |
    set(failure_groups.keys()) |
    set(query_groups.keys())
)

records = []
training_path = (
    project_root / "data" / "processed" /
    "database_activity_processed.csv"
)
training_df = pd.read_csv(training_path)
median_session = training_df["session_duration"].median()

for user_id, hour_window in sorted(all_keys):
    login_data = login_groups.get((user_id, hour_window))
    failure_data = failure_groups.get((user_id, hour_window))
    query_data = query_groups.get((user_id, hour_window))
    if login_data is not None:
        login_hour = int(login_data["login_time"].iloc[0].hour)
    else:
        login_hour = int(hour_window.hour)
    login_failures = (
        len(failure_data) if failure_data is not None else 0
    )
    queries_per_hour = 0
    select_count = 0
    insert_count = 0
    update_count = 0
    delete_count = 0
    distinct_tables = 0
    access_denied_count = 0
    if query_data is not None:
        query_types = query_data["query_type"].str.upper()
        queries_per_hour = len(query_data)
        select_count = int((query_types == "SELECT").sum())
        insert_count = int((query_types == "INSERT").sum())
        update_count = int((query_types == "UPDATE").sum())
        delete_count = int((query_types == "DELETE").sum())
        distinct_tables = int(
            query_data["object_name"].nunique()
        )
        access_denied_count = int(
            (query_data["access_status"].str.upper() == "DENIED").sum()
        )

    session_duration = median_session
    if login_data is not None:
        completed_sessions = login_data.dropna(
            subset=["logout_time"]
        ).copy()
        if not completed_sessions.empty:
            durations = (
                completed_sessions["logout_time"] -
                completed_sessions["login_time"]
            ).dt.total_seconds() / 60
            valid_durations = durations[durations >= 0]
            if not valid_durations.empty:
                session_duration = valid_durations.median()

    after_hours_login = int(
        login_hour < 8 or login_hour >= 20
    )
    record = {
        "login_hour": login_hour,
        "login_failures": login_failures,
        "queries_per_hour": queries_per_hour,
        "select_count": select_count,
        "insert_count": insert_count,
        "update_count": update_count,
        "delete_count": delete_count,
        "distinct_tables": distinct_tables,
        "after_hours_login": after_hours_login,
        "access_denied_count": access_denied_count,
        "session_duration": session_duration
    }
    for uid in range(1, 7):
        record[f"user_{uid}"] = int(user_id == uid)

    records.append(record)

columns = [
    "login_hour",
    "login_failures",
    "queries_per_hour",
    "select_count",
    "insert_count",
    "update_count",
    "delete_count",
    "distinct_tables",
    "after_hours_login",
    "access_denied_count",
    "session_duration",
    "user_1",
    "user_2",
    "user_3",
    "user_4",
    "user_5",
    "user_6"
]

feature_df = pd.DataFrame(records, columns=columns)
output_dir = project_root / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "oracle_activity_features.csv"
feature_df.to_csv(output_path, index=False)

print("\nFEATURE EXTRACTION COMPLETED!")
print("Total activity records:", len(feature_df))
print("Total features:", len(feature_df.columns))
print("\nExtracted features:")
print(feature_df)
print("\nUnknown-user failed login attempts excluded from ML:",
      int(
          (
              pd.read_csv(data_dir / "login_failures.csv")["user_id"].isna()
          ).sum()
      )
)
print("\nSaved at:", output_path)

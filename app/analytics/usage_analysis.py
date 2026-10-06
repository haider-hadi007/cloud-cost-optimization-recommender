import pandas as pd
from app.database.database import get_connection
from app.config import PROCESSED_DIR

def load_usage():
    with get_connection() as conn:
        return pd.read_sql_query(
            "SELECT * FROM usage_metrics ORDER BY timestamp", conn
        )

def analyze_usage(df=None):
    if df is None:
        df = load_usage()
    if df.empty:
        return pd.DataFrame()

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["hour"] = df["timestamp"].dt.hour
    df["idle"] = (df["cpu_usage"] < 10) & (df["memory_usage"] < 20)

    summary = df.groupby("resource_id").agg(
        avg_cpu=("cpu_usage", "mean"),
        max_cpu=("cpu_usage", "max"),
        avg_memory=("memory_usage", "mean"),
        max_memory=("memory_usage", "max"),
        idle_percent=("idle", lambda x: x.mean() * 100),
        samples=("id", "count")
    ).reset_index()

    peak = df.groupby(["resource_id", "hour"])["cpu_usage"].mean().reset_index()
    peak_hours = peak.loc[peak.groupby("resource_id")["cpu_usage"].idxmax()][
        ["resource_id", "hour"]
    ].rename(columns={"hour": "peak_hour"})

    summary = summary.merge(peak_hours, on="resource_id", how="left")
    summary = summary.round(2)

    out = PROCESSED_DIR / "usage_summary.csv"
    summary.to_csv(out, index=False)
    return summary

if __name__ == "__main__":
    result = analyze_usage()
    print(result.to_string(index=False))

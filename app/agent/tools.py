from app.database.database import get_connection
from app.analytics.usage_analysis import analyze_usage, load_usage
from app.analytics.anomaly_detection import detect_anomalies
from app.optimization.simulator import what_if

def get_metrics():
    with get_connection() as conn:
        resources = conn.execute(
            "SELECT COUNT(*) AS n FROM resources"
        ).fetchone()["n"]
        samples = conn.execute(
            "SELECT COUNT(*) AS n FROM usage_metrics"
        ).fetchone()["n"]
    return {"resources": resources, "usage_samples": samples}

def analyze_idle():
    summary = analyze_usage()
    if summary.empty:
        return []
    return summary.to_dict("records")

def detect_usage_anomalies():
    df = load_usage()
    result = detect_anomalies(df)
    if result.empty:
        return []
    return result[result["anomaly"] == 1].to_dict("records")

def simulate_cost():
    return what_if(142.80, idle_hours_per_day=4, idle_threshold=10, archive_old_data=True)

def list_recommendations():
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT resource_id,recommendation,reason,confidence,estimated_saving
               FROM recommendations ORDER BY estimated_saving DESC"""
        ).fetchall()
    return [dict(r) for r in rows]

from app.database.database import get_connection
from app.analytics.usage_analysis import analyze_usage, load_usage
from app.analytics.anomaly_detection import detect_anomalies
from app.analytics.evaluate import evaluate_prediction

def generate_report():
    summary = analyze_usage()
    usage = load_usage()
    anomalies = detect_anomalies(usage)
    anomaly_count = int(anomalies["anomaly"].sum()) if not anomalies.empty else 0
    prediction = evaluate_prediction(usage)

    print("\n========== RESEARCH EVALUATION ==========")
    print(f"Usage samples: {len(usage)}")
    print(f"Resources: {summary['resource_id'].nunique() if not summary.empty else 0}")
    print(f"Anomalies detected: {anomaly_count}")
    print(f"Prediction evaluation: {prediction}")

    if not summary.empty:
        print("\nUtilization summary:")
        print(summary.to_string(index=False))

if __name__ == "__main__":
    generate_report()

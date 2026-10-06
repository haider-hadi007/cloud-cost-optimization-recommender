import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    if df.empty or len(df) < 5:
        return df.assign(anomaly=0, anomaly_score=0.0)

    features = df[["cpu_usage", "memory_usage", "network_rx_mb", "network_tx_mb"]].fillna(0)
    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42
    )
    pred = model.fit_predict(features)
    score = -model.decision_function(features)

    result = df.copy()
    result["anomaly"] = (pred == -1).astype(int)
    result["anomaly_score"] = score.round(4)
    return result

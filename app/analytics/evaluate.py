import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

def evaluate_prediction(df):
    if df.empty:
        return {"status": "no data"}

    data = df.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)
    data["hour"] = data["timestamp"].dt.hour
    data["dayofweek"] = data["timestamp"].dt.dayofweek
    data["lag_cpu"] = data.groupby("resource_id")["cpu_usage"].shift(1)
    data = data.dropna()

    if len(data) < 20:
        return {"status": "not enough data", "samples": len(data)}

    X = data[["hour", "dayofweek", "lag_cpu", "memory_usage"]]
    y = data["cpu_usage"]

    split = int(len(data) * 0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    return {
        "status": "ok",
        "test_samples": len(y_test),
        "mae": round(float(mean_absolute_error(y_test, pred)), 3)
    }

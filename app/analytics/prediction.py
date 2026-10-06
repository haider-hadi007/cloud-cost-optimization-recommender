import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def train_cpu_predictor(df):
    if df.empty:
        return None

    data = df.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)
    data["hour"] = data["timestamp"].dt.hour
    data["dayofweek"] = data["timestamp"].dt.dayofweek
    data["lag_cpu"] = data.groupby("resource_id")["cpu_usage"].shift(1)
    data = data.dropna()

    if len(data) < 10:
        return None

    X = data[["hour", "dayofweek", "lag_cpu", "memory_usage"]]
    y = data["cpu_usage"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)
    return model

def predict_next(model, hour, dayofweek, lag_cpu, memory_usage):
    if model is None:
        return None
    return float(model.predict([[hour, dayofweek, lag_cpu, memory_usage]])[0])

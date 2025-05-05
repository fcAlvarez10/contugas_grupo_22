# src/serialization.py

import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

from .ingestion    import load_data
from .features     import add_features, prepare_ml_matrix

RANDOM_STATE = 42

def train_and_save_if(data_path: str,
                      contamination: float,
                      output_path: str) -> None:
    """
    Entrena IsolationForest en todo el dataset y serializa scaler+modelo.
    """
    df = load_data(data_path)
    df_fe = add_features(df)
    X     = prepare_ml_matrix(df_fe)

    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)

    model = IsolationForest(contamination=contamination,
                            random_state=RANDOM_STATE)
    model.fit(X_scaled)

    joblib.dump({"scaler": scaler, "model": model}, output_path)

def load_model(path: str) -> dict:
    """
    Carga dict {'scaler':..., 'model':...} generado por train_and_save_if.
    """
    return joblib.load(path)

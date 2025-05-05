# src/detectors.py

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

RANDOM_STATE = 42

def fit_predict(det_name: str,
                X_train, X_val,
                contamination: float,
                n_neighbors: int = None):
    """
    Entrena IsolationForest o LOF y devuelve (predictions, scores).
    """
    scaler = StandardScaler().fit(X_train)
    Xtr, Xvl = scaler.transform(X_train), scaler.transform(X_val)

    if det_name == "if":
        model = IsolationForest(
            contamination=contamination,
            random_state=RANDOM_STATE
        )
    elif det_name == "lof":
        k = n_neighbors or 20
        model = LocalOutlierFactor(
            n_neighbors=k,
            contamination=contamination,
            novelty=True
        )
    else:
        raise ValueError(f"Detector desconocido: {det_name}")

    model.fit(Xtr)
    preds_val  = model.predict(Xvl)
    scores_val = model.decision_function(Xvl)
    return preds_val, scores_val

# src/evaluation.py

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

from .detectors import fit_predict
from .metrics import metrics_block_unsup

def run_cv(X: pd.DataFrame,
           cont_df: pd.DataFrame,
           contamination_grid: list,
           neighbors_grid: list,
           n_splits: int = 3) -> pd.DataFrame:
    """
    Ejecuta CV temporal y devuelve DataFrame con métricas para cada combinación.
    """
    tscv = TimeSeriesSplit(n_splits=n_splits)
    results = []

    for det in ["if", "lof"]:
        for c in contamination_grid:
            neighs = neighbors_grid if det == "lof" else [None]
            for n in neighs:
                gaps, bcs, exts, rates = [], [], [], []
                for train_idx, val_idx in tscv.split(X):
                    Xtr, Xvl = X.iloc[train_idx], X.iloc[val_idx]
                    preds, scores = fit_predict(det, Xtr, Xvl, contamination=c, n_neighbors=n)
                    gap, bc, ext = metrics_block_unsup(preds, scores, cont_df.iloc[val_idx].values)
                    gaps.append(gap); bcs.append(bc); exts.append(ext)
                    rates.append((preds == -1).mean())
                results.append({
                    "detector":      det,
                    "contamination": c,
                    "n_neighbors":   n,
                    "gap_cv":        np.mean(gaps),
                    "bimodality_cv": np.mean(bcs),
                    "ext_cov_cv":    np.mean(exts),
                    "anomaly_rate":  np.mean(rates)
                })

    return pd.DataFrame(results).round(3)

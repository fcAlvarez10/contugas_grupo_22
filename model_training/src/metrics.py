# src/metrics.py

import numpy as np
from scipy.stats import kurtosis, skew
from scipy.stats import zscore

def gap_score(scores: np.ndarray, preds: np.ndarray) -> float:
    normals = scores[preds == 1]
    anoms   = scores[preds == -1]
    iqr = np.subtract(*np.percentile(scores, [75, 25]))
    return np.abs(np.median(normals) - np.median(anoms)) / (iqr + 1e-9)

def bimodality_coefficient(scores: np.ndarray) -> float:
    n = len(scores)
    g = skew(scores)
    k = kurtosis(scores, fisher=False)
    return (g**2 + 1) / (k + (3*((n-1)**2)/((n-2)*(n-3))))

def extreme_coverage(df_cont: np.ndarray, preds: np.ndarray, z_thresh: float = 2) -> float:
    z = zscore(df_cont, nan_policy="omit")
    is_extreme = (np.abs(z) > z_thresh).any(axis=1)
    return is_extreme[preds == -1].mean()

def metrics_block_unsup(preds: np.ndarray, scores: np.ndarray, cont_df_val: np.ndarray):
    """
    Devuelve GAP, bimodality coefficient y extreme coverage para un fold.
    """
    gap = gap_score(scores, preds)
    bc  = bimodality_coefficient(scores)
    ext = extreme_coverage(cont_df_val, preds)
    return gap, bc, ext

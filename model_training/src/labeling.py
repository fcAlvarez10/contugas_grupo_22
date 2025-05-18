# src/labeling.py

import numpy as np

def rolling_iqr_mask(df, variable: str, window: int) -> pd.Series:
    q1 = df.groupby('Cliente')[variable].transform(
             lambda x: x.rolling(window, 1).quantile(0.25))
    q3 = df.groupby('Cliente')[variable].transform(
             lambda x: x.rolling(window, 1).quantile(0.75))
    iqr = q3 - q1
    return ((df[variable] < (q1 - 1.5*iqr)) |
            (df[variable] > (q3 + 1.5*iqr))).astype(int)

def make_pseudo_label(df, window: int = 48) -> np.ndarray:
    """
    Genera etiquetas binarias [-1, 1] según rolling IQR de Presion, Volumen y Temperatura.
    """
    m_p = rolling_iqr_mask(df, 'Presion',     window)
    m_v = rolling_iqr_mask(df, 'Volumen',     window)
    m_t = rolling_iqr_mask(df, 'Temperatura', window)
    return ((m_p + m_v + m_t) >= 1).replace({1: -1, 0: 1}).to_numpy()

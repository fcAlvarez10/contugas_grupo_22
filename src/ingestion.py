# src/ingestion.py

import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    """
    Lee un fichero CSV o Excel y devuelve un DataFrame.
    """
    if path.lower().endswith((".xls", ".xlsx")):
        return pd.read_excel(path)
    else:
        return pd.read_csv(path)

def initial_eda(df: pd.DataFrame) -> None:
    """
    Imprime forma y primeros registros del DataFrame.
    """
    print("Shape:", df.shape)
    print(df.head())

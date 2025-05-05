# src/features.py

import numpy as np
import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df = df.sort_values(['Cliente', 'Fecha']).reset_index(drop=True)

    # Temporales básicas
    df['hour']        = df['Fecha'].dt.hour
    df['day_of_week'] = df['Fecha'].dt.dayofweek
    df['is_weekend']  = (df['day_of_week'] >= 5).astype(int)

    # Señales cíclicas
    df['sin_hour']        = np.sin(2*np.pi * df['hour']        / 24)
    df['cos_hour']        = np.cos(2*np.pi * df['hour']        / 24)
    df['sin_day_of_week'] = np.sin(2*np.pi * df['day_of_week'] / 7)
    df['cos_day_of_week'] = np.cos(2*np.pi * df['day_of_week'] / 7)

    # One-hot por cliente
    df = pd.get_dummies(df, columns=['Cliente'], prefix='C')

    # Ratios y productos
    df['ratio_pres_vol']  = df['Presion']     / (df['Volumen']     + 1e-6)
    df['ratio_pres_temp'] = df['Presion']     / (df['Temperatura'] + 1e-6)
    df['ratio_vol_temp']  = df['Volumen']     / (df['Temperatura'] + 1e-6)
    df['prod_pres_vol']   = df['Presion'] * df['Volumen']
    df['prod_pres_temp']  = df['Presion'] * df['Temperatura']
    df['prod_vol_temp']   = df['Volumen'] * df['Temperatura']

    # Transformaciones log-safe
    df['log_presion']     = np.log1p(df['Presion'])
    df['log_volumen']     = np.log1p(df['Volumen'])
    df['log_temperatura'] = np.log1p(df['Temperatura'])

    # Estadísticos fila
    trio = df[['Presion', 'Volumen', 'Temperatura']]
    df['mean_three'] = trio.mean(axis=1)
    df['std_three']  = trio.std(axis=1)
    df['max_three']  = trio.max(axis=1)
    df['min_three']  = trio.min(axis=1)

    # Imputación medianas
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    return df

def prepare_ml_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina columnas no usadas en entrenamiento.
    """
    return df.drop(columns=['Fecha'])

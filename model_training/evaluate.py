# evaluate.py

import os
import argparse
import pandas as pd

from src.serialization import load_model
from src.features      import add_features, prepare_ml_matrix

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True,
                        help="Ruta al fichero CSV o XLSX de nuevos datos")
    args = parser.parse_args()

    # Carga y preparación
    ext = os.path.splitext(args.input)[1].lower()
    df = pd.read_excel(args.input) if ext in (".xls", ".xlsx") else pd.read_csv(args.input)
    df_fe = add_features(df)
    X     = prepare_ml_matrix(df_fe)

    # Carga modelo
    pipeline = load_model(os.path.join("models", "if_contamination_0.05.pkl"))
    scaler, model = pipeline["scaler"], pipeline["model"]

    # Predicción
    X_scaled = scaler.transform(X)
    df["prediction"] = model.predict(X_scaled)

    print(df.head())

if __name__ == "__main__":
    main()

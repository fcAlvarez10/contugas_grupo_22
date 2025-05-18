# train_and_serialize.py

import os
from src.serialization import train_and_save_if

if __name__ == "__main__":
    DATA_PATH   = os.path.join("data", "raw", "datos_clientes.xlsx")
    OUTPUT_PATH = os.path.join("models", "if_contamination_0.05.pkl")

    train_and_save_if(DATA_PATH,
                      contamination=0.05,
                      output_path=OUTPUT_PATH)

    print(f"✅ Modelo serializado en '{OUTPUT_PATH}'")

# Proyecto Unsupervised

Detección de anomalías en series temporales de clientes  
con modelos no supervisados (IsolationForest y LOF).

## Estructura

proyecto_unsupervised/
├── data/
│   raw/           # Datos originales
├── notebooks/         # Prototipos y EDA
├── src/               # Módulos Python
├── models/            # Modelos serializados
├── train_and_serialize.py
├── evaluate.py
├── requirements.txt
└── README.md

## Instalación

pip install -r requirements.txt

## Entrenar y serializar

python train_and_serialize.py

Esto generará models/if_contamination_0.05.pkl.

## Evaluar nuevos datos

python evaluate.py --input data/raw/nuevos_datos.xlsx

Verás por pantalla las primeras filas con su columna prediction.

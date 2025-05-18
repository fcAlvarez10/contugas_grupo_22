from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, NumberRange
import joblib
from datetime import datetime
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for CSRF protection

# Load the trained model
loaded_objects = joblib.load('model/if_contamination_0.05.pkl')
scaler = loaded_objects['scaler']
model = loaded_objects['model']

def preprocess_features(df):
    df = df.copy()
    fecha = pd.to_datetime(df['fecha_hora'])
    
    # Temporales básicas
    df['hour'] = fecha.dt.hour
    df['day_of_week'] = fecha.dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # Señales cíclicas
    df['sin_hour'] = np.sin(2*np.pi * df['hour'] / 24)
    df['cos_hour'] = np.cos(2*np.pi * df['hour'] / 24)
    df['sin_day_of_week'] = np.sin(2*np.pi * df['day_of_week'] / 7)
    df['cos_day_of_week'] = np.cos(2*np.pi * df['day_of_week'] / 7)
    
    # One-hot por cliente
    cliente_cols = [f'C_CLIENTE{i}' for i in range(1, 21)]
    for col in cliente_cols:
        client_num = int(col.split('CLIENTE')[1])
        df[col] = (df['cliente'] == client_num).astype(int)
    
    # Ratios y productos
    df['ratio_pres_vol'] = df['Presion'] / (df['Volumen'] + 1e-6)
    df['ratio_pres_temp'] = df['Presion'] / (df['Temperatura'] + 1e-6)
    df['ratio_vol_temp'] = df['Volumen'] / (df['Temperatura'] + 1e-6)
    df['prod_pres_vol'] = df['Presion'] * df['Volumen']
    df['prod_pres_temp'] = df['Presion'] * df['Temperatura']
    df['prod_vol_temp'] = df['Volumen'] * df['Temperatura']
    
    # Transformaciones log-safe
    df['log_presion'] = np.log1p(df['Presion'])
    df['log_volumen'] = np.log1p(df['Volumen'])
    df['log_temperatura'] = np.log1p(df['Temperatura'])
    
    # Estadísticos fila
    trio = df[['Presion', 'Volumen', 'Temperatura']]
    df['mean_three'] = trio.mean(axis=1)
    df['std_three'] = trio.std(axis=1)
    df['max_three'] = trio.max(axis=1)
    df['min_three'] = trio.min(axis=1)
    
    # Eliminar columnas originales que no se usan en el modelo
    df = df.drop(columns=['fecha_hora', 'cliente', 'hour', 'day_of_week'])
    
    return df

class AnomalyDetectionForm(FlaskForm):
    datetime = DateTimeLocalField('Fecha-Hora', 
                                format='%Y-%m-%dT%H:%M',
                                validators=[DataRequired()])
    
    cliente = SelectField('Cliente',
                         choices=[f'CLIENTE{i}' for i in range(1, 21)],
                         validators=[DataRequired()])
    
    volumen = FloatField('Volumen',
                        validators=[DataRequired(), NumberRange(min=0)])
    
    presion = FloatField('Presión',
                        validators=[DataRequired(), NumberRange(min=0)])
    
    temperatura = FloatField('Temperatura',
                           validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AnomalyDetectionForm()
    result = None
    
    if form.validate_on_submit():
        # Prepare the input data
        input_data = pd.DataFrame({
            'fecha_hora': [form.datetime.data],
            'cliente': [form.cliente.data],
            'Volumen': [form.volumen.data],
            'Presion': [form.presion.data],
            'Temperatura': [form.temperatura.data]
        })
        
        # Convert cliente to numeric (CLIENTE1 -> 1, CLIENTE2 -> 2, etc.)
        input_data['cliente'] = input_data['cliente'].str.extract('(\\d+)').astype(int)
        
        # Preprocess features
        processed_data = preprocess_features(input_data)
        
        # Ensure column order matches training
        expected_columns = ['Presion', 'Temperatura', 'Volumen', 'hour', 'day_of_week', 'is_weekend',
                          'sin_hour', 'cos_hour', 'sin_day_of_week', 'cos_day_of_week'] + \
                         [f'C_CLIENTE{i}' for i in range(1, 21)] + \
                         ['ratio_pres_vol', 'ratio_pres_temp', 'ratio_vol_temp',
                          'prod_pres_vol', 'prod_pres_temp', 'prod_vol_temp',
                          'log_presion', 'log_volumen', 'log_temperatura',
                          'mean_three', 'std_three', 'max_three', 'min_three']
        
        processed_data = processed_data.reindex(columns=expected_columns, fill_value=0)
        
        # Scale the features
        scaled_data = scaler.transform(processed_data)
        
        # Make prediction
        prediction = model.predict(scaled_data)
        is_anomaly = prediction[0] == -1
        
        result = {
            'is_anomaly': is_anomaly,
            'message': 'ANOMALÍA DETECTADA' if is_anomaly else 'REGISTRO NORMAL'
        }
    
    return render_template('index.html', form=form, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 
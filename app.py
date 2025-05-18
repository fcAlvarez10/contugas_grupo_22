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
model = joblib.load('model/if_contamination_0.05.pkl')

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
            'volumen': [form.volumen.data],
            'presion': [form.presion.data],
            'temperatura': [form.temperatura.data]
        })
        
        # Convert datetime to numeric (timestamp)
        input_data['fecha_hora'] = pd.to_datetime(input_data['fecha_hora']).astype(np.int64) // 10**9
        
        # Convert cliente to numeric using label encoding (CLIENTE1 -> 1, CLIENTE2 -> 2, etc.)
        input_data['cliente'] = input_data['cliente'].str.extract('(\\d+)').astype(int)
        
        # Make prediction
        prediction = model.predict(input_data)
        is_anomaly = prediction[0] == -1
        
        result = {
            'is_anomaly': is_anomaly,
            'message': 'ANOMALÍA DETECTADA' if is_anomaly else 'REGISTRO NORMAL'
        }
    
    return render_template('index.html', form=form, result=result)

if __name__ == '__main__':
    app.run(debug=True) 
import numpy as np
import pandas as pd
import warnings
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from datetime import datetime

warnings.filterwarnings('ignore')

data = pd.read_csv('../data/data.csv')

# Función para calcular la diferencia en minutos entre la hora de salida y la hora de llegada
def get_min_diff(data):
    try:
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        return ((fecha_o - fecha_i).total_seconds()) / 60
    except Exception as e:
        return None

data['min_diff'] = data.apply(get_min_diff, axis=1)

# Se marca como retraso si la diferencia en minutos excede el umbral
threshold_in_minutes = 15
data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)

# Crear las features y la variable target
features = pd.concat([
    pd.get_dummies(data['OPERA'], prefix='OPERA'),
    pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'), 
    pd.get_dummies(data['MES'], prefix='MES')
], axis=1)

target = data['delay']

# Seleccionar las características más importantes para el modelo
top_10_features = [
    "OPERA_Latin American Wings", 
    "MES_7",
    "MES_10",
    "OPERA_Grupo LATAM",
    "MES_12",
    "TIPOVUELO_I",
    "MES_4",
    "MES_11",
    "OPERA_Sky Airline",
    "OPERA_Copa Air"
]

# Dividir los datos en conjunto de entrenamiento y prueba y calcular balance de clases
x_train, x_test, y_train, y_test = train_test_split(features[top_10_features], target, test_size=0.33, random_state=42)

n_y0 = len(y_train[y_train == 0])
n_y1 = len(y_train[y_train == 1])
scale = n_y0 / n_y1

# Entrenar el modelo de Regresión Lógistica con balance de clases
reg_model = LogisticRegression(class_weight={1: n_y0/len(y_train), 0: n_y1/len(y_train)})
reg_model.fit(x_train, y_train)

# Realizar predicciones
reg_y_preds = reg_model.predict(x_test)

print(confusion_matrix(y_test, reg_y_preds))
print(classification_report(y_test, reg_y_preds))

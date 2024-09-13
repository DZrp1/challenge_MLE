import sys
import os

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)

import fastapi
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
from challenge.model import DelayModel

app = fastapi.FastAPI()

model = DelayModel()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '../data/data.csv')

try:
    data = pd.read_csv(DATA_PATH)

    airlines = data['OPERA'].unique().tolist()  
    types = data['TIPOVUELO'].unique().tolist()  
    months = data['MES'].unique().tolist()

    features, target = model.preprocess(data, target_column="delay")
    model.fit(features, target)

except Exception as e:
    raise RuntimeError(f"Error al entrenar el modelo: {str(e)}")

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

class PredictRequest(BaseModel):
    flights: List[Flight]

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: PredictRequest) -> dict:
    for flight in request.flights:
        if flight.OPERA not in airlines:
            raise HTTPException(status_code=400, detail=f"Aerolínea '{flight.OPERA}' no es válida. Aerolíneas válidas: {', '.join(airlines)}.")
        if flight.TIPOVUELO not in types:
            raise HTTPException(status_code=400, detail=f"Tipo de vuelo '{flight.TIPOVUELO}' no es válido. Debe ser 'N' (Nacional) o 'I' (Internacional).")
        if flight.MES not in months:
            raise HTTPException(status_code=400, detail=f"El mes '{flight.MES}' no es válido. Debe estar entre 1 y 12.")

    try:
        # Convertir los datos a un DataFrame
        df = pd.DataFrame([flight.dict() for flight in request.flights])
        if df.empty:
            raise HTTPException(status_code=400, detail="No se recibieron datos válidos")
        
        # Preprocesar los datos (donde las aerolíneas no relevantes se les asigna 0)
        try:
            features = model.preprocess(df)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        
        # Realizar la predicción
        predictions = model.predict(features)
        return {"predict": predictions}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {str(e)}")

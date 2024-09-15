import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from fastapi import HTTPException, FastAPI
from pydantic import BaseModel
from typing import List
from joblib import load
import pandas as pd

app = FastAPI()

model_data = load("challenge/trained_model_with_metadata.joblib") # C:/Personales/Programas_Python/challenge_MLE/
model = model_data['model']
preprocess = model_data['preprocessor'] 
airlines = model_data['airlines']
types = model_data['types']
months = model_data['months']

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

class PredictRequest(BaseModel):
    flights: List[Flight]

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict(request: PredictRequest) -> dict:
    # Validate the received data
    for flight in request.flights:
        if flight.OPERA not in airlines:
            raise HTTPException(status_code=400, detail=f"Airline '{flight.OPERA}' is not valid. Valid airlines: {', '.join(airlines)}.")
        if flight.TIPOVUELO not in types:
            raise HTTPException(status_code=400, detail=f"Flight type '{flight.TIPOVUELO}' is not valid.")
        if flight.MES not in months:
            raise HTTPException(status_code=400, detail=f"The month '{flight.MES}' is not valid. It must be between 1 and 12.")

    df = pd.DataFrame([flight.dict() for flight in request.flights])
    
    # Apply the saved preprocessing
    features = preprocess(df)
    predictions = model.predict(features)
    predictions_list = predictions.tolist()
    
    return {"predict": predictions_list}
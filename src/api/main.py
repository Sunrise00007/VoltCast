from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import datetime

from src.db import load_history
from src.api.utils import load_inference_artifacts, format_prediction_input
from src.config import Config

app = FastAPI(title="EV Charging Forecaster API", version="1.0")

# Global variables for model artifacts
model = None
preprocessor = None

@app.on_event("startup")
async def startup_event():
    global model, preprocessor
    try:
        model, preprocessor = load_inference_artifacts()
        print("Model and artifacts loaded successfully.")
    except Exception as e:
        print(f"Warning: Could not load model. Ensure training is done. Error: {e}")

class PredictionResponse(BaseModel):
    station_id: int
    current_time: datetime.datetime
    predicted_available_ports: float
    status: str

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "active", "system": "EV Forecasting System"}

@app.get("/predict/{station_id}", response_model=PredictionResponse)
def predict_availability(station_id: int):
    global model, preprocessor
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Train model first.")

    # 1. Fetch recent history for this station
    df = load_history(station_id=station_id)
    
    # We need at least SEQ_LENGTH records
    if len(df) < Config.SEQ_LENGTH:
        raise HTTPException(status_code=400, detail=f"Insufficient historical data for Station {station_id}. Need {Config.SEQ_LENGTH} records.")
    
    # Take the last SEQ_LENGTH records
    recent_data = df.tail(Config.SEQ_LENGTH).copy()
    
    # 2. Preprocess
    input_tensor = format_prediction_input(recent_data.to_dict('records'), preprocessor)
    
    # 3. Inference
    prediction_norm = model(input_tensor).item()
    
    # 4. Inverse Transform (Denormalize)
    # We normalized 4 columns. We need to create a dummy array to inverse transform just the target
    # Scaler min/max for 'available_ports' is at index 0
    
    # Manual denormalization for efficiency/simplicity
    # available_scaled = (x - min) / (max - min) -> x = available_scaled * (max - min) + min
    avail_min = preprocessor.scaler.data_min_[0]
    avail_max = preprocessor.scaler.data_max_[0]
    
    predicted_ports = prediction_norm * (avail_max - avail_min) + avail_min
    predicted_ports = max(0, round(predicted_ports)) # Clip to 0
    
    return {
        "station_id": station_id,
        "current_time": datetime.datetime.now(),
        "predicted_available_ports": predicted_ports,
        "status": "High Availability" if predicted_ports > 1 else "Congested"
    }
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import datetime
import os

from src.db import load_history, get_stations, get_station
from src.api.utils import load_inference_artifacts, format_prediction_input, build_maps_directions_url
from src.config import Config

app = FastAPI(title="EV Charging Forecaster API", version="1.0")

# Add CORS middleware to allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    station_name: str
    station_type: str
    total_ports: int
    address: str
    latitude: float
    longitude: float
    current_time: datetime.datetime
    predicted_available_ports: float
    availability_percentage: float
    status: str
    navigation_available: bool

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "active", "system": "EV Forecasting System"}

@app.get("/dashboard", tags=["UI"])
async def get_dashboard():
    """Serve the dashboard HTML UI"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="Dashboard not found")


@app.get("/stations", tags=["Stations"])
def list_stations():
    return get_stations()


@app.get("/stations/{station_id}/navigate", tags=["Stations"])
def navigate_station(station_id: int, mode: str = Query("driving")):
    station = get_station(station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    url = build_maps_directions_url(station['latitude'], station['longitude'], travel_mode=mode)
    return {"station_id": station_id, "maps_url": url}

@app.get("/predict/{station_id}", response_model=PredictionResponse)
def predict_availability(station_id: int):
    global model, preprocessor
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Train model first.")
    
    # Get station metadata
    station = get_station(station_id)
    if not station:
        raise HTTPException(status_code=404, detail=f"Station {station_id} not found")
    
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
    # Manual denormalization for efficiency/simplicity
    avail_min = preprocessor.scaler.data_min_[0]
    avail_max = preprocessor.scaler.data_max_[0]
    
    predicted_ports = prediction_norm * (avail_max - avail_min) + avail_min
    predicted_ports = max(0, round(predicted_ports)) # Clip to 0
    
    # Calculate availability percentage
    total_ports = station.get('total_ports', 10)  # Default to 10 if not specified
    availability_percentage = (predicted_ports / total_ports) * 100 if total_ports > 0 else 0
    
    # Determine status and navigation availability
    is_high_availability = predicted_ports > 1
    status = "High Availability" if is_high_availability else "Congested"
    navigation_available = predicted_ports > 0  # Can navigate if at least 1 port available
    
    return {
        "station_id": station_id,
        "station_name": station.get('name', f"Station {station_id}"),
        "station_type": station.get('type', 'unknown'),
        "total_ports": total_ports,
        "address": station.get('address', ''),
        "latitude": station.get('latitude', 0.0),
        "longitude": station.get('longitude', 0.0),
        "current_time": datetime.datetime.now(),
        "predicted_available_ports": predicted_ports,
        "availability_percentage": round(availability_percentage, 1),
        "status": status,
        "navigation_available": navigation_available
    }
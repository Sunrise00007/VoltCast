import torch
import pandas as pd
import numpy as np
from src.config import Config
from src.model import EVChargingLSTM
from src.preprocessing import DataPreprocessor

def load_inference_artifacts():
    # Load Model
    # Try to infer number of stations from DB to create correct embedding size
    try:
        from src.db import get_stations
        stations = get_stations()
        num_stations = max([s['id'] for s in stations]) + 1 if stations else 100
    except Exception:
        num_stations = 100

    model = EVChargingLSTM(
        hidden_dim=Config.HIDDEN_DIM,
        num_layers=Config.NUM_LAYERS,
        station_emb_dim=Config.STATION_EMBED_DIM,
        num_stations=num_stations
    )
    # Load with strict=False to allow loading older state dicts without station embedding weights
    state = torch.load(Config.MODEL_PATH, map_location=torch.device('cpu'))
    model.load_state_dict(state, strict=False)
    model.eval()
    
    # Load Scaler
    preprocessor = DataPreprocessor()
    preprocessor.load()
    
    return model, preprocessor

def format_prediction_input(records, preprocessor):
    """
    Takes raw dictionary records (last 12 steps), processes them,
    and returns tensor for model.
    """
    df = pd.DataFrame(records)
    df = preprocessor.transform(df)
    
    # Extract features in correct order (station_id is last and will be used as an embedding index)
    # available_ports, total_ports, latitude, longitude, hour, day_of_week, station_id
    if 'station_id' not in df.columns:
        df = df.copy()
        df['station_id'] = 0
    features = df[['available_ports', 'total_ports', 'latitude', 'longitude', 'hour', 'day_of_week', 'station_id']].values
    
    # Add batch dimension: (1, seq_len, features)
    tensor_input = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
    return tensor_input


def build_maps_directions_url(lat, lon, travel_mode='driving'):
    """Return a Google Maps deep-link URL for directions."""
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode={travel_mode}"
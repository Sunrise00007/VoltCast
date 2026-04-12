import torch
import pandas as pd
import numpy as np
from api.config import Config
from api.model import EVChargingLSTM
from api.preprocessing import DataPreprocessor

def load_inference_artifacts():
    try:
        from api.db import get_stations
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
    state = torch.load(Config.MODEL_PATH, map_location=torch.device('cpu'))
    model.load_state_dict(state, strict=False)
    model.eval()
    preprocessor = DataPreprocessor()
    preprocessor.load()
    return model, preprocessor

def format_prediction_input(records, preprocessor):
    df = pd.DataFrame(records)
    df = preprocessor.transform(df)
    if 'station_id' not in df.columns:
        df = df.copy()
        df['station_id'] = 0
    features = df[['available_ports', 'total_ports', 'latitude', 'longitude', 'hour', 'day_of_week', 'station_id']].values
    tensor_input = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
    return tensor_input

def build_maps_directions_url(lat, lon, travel_mode='driving'):
    return f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode={travel_mode}"
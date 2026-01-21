import torch
import pandas as pd
import numpy as np
from src.config import Config
from src.model import EVChargingLSTM
from src.preprocessing import DataPreprocessor

def load_inference_artifacts():
    # Load Model
    model = EVChargingLSTM(hidden_dim=Config.HIDDEN_DIM, num_layers=Config.NUM_LAYERS)
    model.load_state_dict(torch.load(Config.MODEL_PATH, map_location=torch.device('cpu')))
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
    
    # Extract features in correct order
    # available_ports, total_ports, latitude, longitude, hour, day_of_week
    features = df[['available_ports', 'total_ports', 'latitude', 'longitude', 'hour', 'day_of_week']].values
    
    # Add batch dimension: (1, seq_len, features)
    tensor_input = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
    return tensor_input
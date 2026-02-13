import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
from src.config import Config

class DataPreprocessor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        # Features to scale: available_ports, total_ports, lat, lon
        # station_id is NOT scaled; we'll use a learned embedding for station IDs in the model
        self.feature_cols = ['available_ports', 'total_ports', 'latitude', 'longitude']
        
    def fit(self, df):
        # Ensure station_id exists and is numeric
        if 'station_id' not in df.columns:
            df = df.copy()
            df['station_id'] = 0
        self.scaler.fit(df[self.feature_cols])
        
    def transform(self, df):
        # 1. Date Features
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        # 2. Ensure station_id present
        if 'station_id' not in df.columns:
            df = df.copy()
            df['station_id'] = 0

        # 3. Scale Numeric
        df[self.feature_cols] = self.scaler.transform(df[self.feature_cols])
        
        return df

    def save(self, path=None):
        """Save scaler to disk. If path not provided uses Config.SCALER_PATH"""
        path = path or Config.SCALER_PATH
        joblib.dump(self.scaler, path)
        
    def load(self, path=None):
        """Load scaler from disk. If path not provided uses Config.SCALER_PATH"""
        path = path or Config.SCALER_PATH
        self.scaler = joblib.load(path)


def create_sequences(data, seq_length, target_col_idx=0, include_station_id=True):
    """
    Converts DataFrame to [Samples, Seq_Len, Features]
    target_col_idx 0 corresponds to 'available_ports' (scaled)

    include_station_id: if True, sequences include station_id as the last feature (for global model
    which uses embeddings). If False (per-station mode), station_id is excluded and model receives only
    numeric+time features.
    """
    sequences = []
    targets = []

    if include_station_id:
        # Order: available_ports, total_ports, latitude, longitude, hour, day_of_week, station_id
        data_array = data[['available_ports', 'total_ports', 'latitude', 'longitude', 'hour', 'day_of_week', 'station_id']].values
    else:
        # Exclude station_id for per-station models
        # Order: available_ports, total_ports, latitude, longitude, hour, day_of_week
        data_array = data[['available_ports', 'total_ports', 'latitude', 'longitude', 'hour', 'day_of_week']].values

    for i in range(len(data_array) - seq_length):
        seq = data_array[i:i+seq_length]
        target = data_array[i+seq_length][target_col_idx] # Predict next available_ports
        sequences.append(seq)
        targets.append(target)
        
    return np.array(sequences), np.array(targets)
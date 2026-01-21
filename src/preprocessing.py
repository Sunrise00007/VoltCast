import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
from src.config import Config

class DataPreprocessor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        # Features to scale: available_ports, total_ports, lat, lon
        self.feature_cols = ['available_ports', 'total_ports', 'latitude', 'longitude']
        
    def fit(self, df):
        self.scaler.fit(df[self.feature_cols])
        
    def transform(self, df):
        # 1. Date Features
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        # 2. Scale Numeric
        df[self.feature_cols] = self.scaler.transform(df[self.feature_cols])
        
        return df

    def save(self):
        joblib.dump(self.scaler, Config.SCALER_PATH)
        
    def load(self):
        self.scaler = joblib.load(Config.SCALER_PATH)

def create_sequences(data, seq_length, target_col_idx=0):
    """
    Converts DataFrame to [Samples, Seq_Len, Features]
    target_col_idx 0 corresponds to 'available_ports' (scaled)
    """
    sequences = []
    targets = []
    
    # Convert to numpy array
    # Order: available_ports, total_ports, lat, lon, hour, day_of_week
    data_array = data[['available_ports', 'total_ports', 'latitude', 'longitude', 'hour', 'day_of_week']].values
    
    for i in range(len(data_array) - seq_length):
        seq = data_array[i:i+seq_length]
        target = data_array[i+seq_length][target_col_idx] # Predict next available_ports
        sequences.append(seq)
        targets.append(target)
        
    return np.array(sequences), np.array(targets)
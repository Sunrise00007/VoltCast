import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
from api.config import Config

class DataPreprocessor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.feature_cols = ['available_ports', 'total_ports', 'latitude', 'longitude']
    def fit(self, df):
        if 'station_id' not in df.columns:
            df = df.copy()
            df['station_id'] = 0
        self.scaler.fit(df[self.feature_cols])
    def transform(self, df):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        if 'station_id' not in df.columns:
            df = df.copy()
            df['station_id'] = 0
        df[self.feature_cols] = self.scaler.transform(df[self.feature_cols])
        return df
    def save(self, path=None):
        path = path or Config.SCALER_PATH
        joblib.dump(self.scaler, path)
    def load(self, path=None):
        path = path or Config.SCALER_PATH
        self.scaler = joblib.load(path)
def create_sequences(data, seq_length, target_col_idx=0, include_station_id=True):
    sequences = []
    targets = []
    if include_station_id:
        data_array = data[['available_ports', 'total_ports', 'latitude', 'longitude', 'hour', 'day_of_week', 'station_id']].values
    else:
        data_array = data[['available_ports', 'total_ports', 'latitude', 'longitude', 'hour', 'day_of_week']].values
    for i in range(len(data_array) - seq_length):
        seq = data_array[i:i+seq_length]
        target = data_array[i+seq_length][target_col_idx]
        sequences.append(seq)
        targets.append(target)
    return np.array(sequences), np.array(targets)

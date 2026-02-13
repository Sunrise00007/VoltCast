import torch
import torch.nn as nn

class EVChargingLSTM(nn.Module):
    def __init__(self, hidden_dim, num_layers, station_emb_dim=8, num_stations=None, dropout=0.2):
        super(EVChargingLSTM, self).__init__()

        # Embeddings
        self.hour_embedding = nn.Embedding(24, 4)      # Map 0-23 to vector of size 4
        self.day_embedding = nn.Embedding(7, 2)        # Map 0-6 to vector of size 2

        # Station embedding (only create if embedding dim > 0)
        self.station_emb_dim = station_emb_dim
        if station_emb_dim and station_emb_dim > 0:
            if num_stations is None:
                num_stations = 100
            self.station_embedding = nn.Embedding(num_stations, station_emb_dim)

        # Input Dimension Calculation:
        # 4 numeric features (avail, total, lat, lon) + 4 (hour_emb) + 2 (day_emb)
        # If station_emb_dim > 0: + station_emb_dim
        input_dim = 4 + 4 + 2 + (station_emb_dim if station_emb_dim else 0)

        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout
        )

        # Regression Head
        self.fc = nn.Linear(hidden_dim, 1) # Predicting available_ports (normalized)
        self.relu = nn.ReLU()

    def forward(self, x):
        # x shape: (batch, seq_len, features)
        # Features indices: 0:4 numeric (available, total, lat, lon), 4: hour, 5: day, 6: station_id

        numeric = x[:, :, 0:4].float()
        hour_idx = x[:, :, 4].long()
        day_idx = x[:, :, 5].long()

        # Get embeddings
        hour_emb = self.hour_embedding(hour_idx)
        day_emb = self.day_embedding(day_idx)

        if self.station_emb_dim and hasattr(self, 'station_embedding'):
            # station_idx is the last feature in input when embeddings are used
            station_idx = x[:, :, 6].long()
            station_emb = self.station_embedding(station_idx)  # shape: (batch, seq_len, emb_dim)
            # Concatenate: (batch, seq_len, 4+4+2+station_emb_dim)
            combined = torch.cat([numeric, hour_emb, day_emb, station_emb], dim=2)
        else:
            # No station embedding; concatenate only numeric + time embeddings
            combined = torch.cat([numeric, hour_emb, day_emb], dim=2)

        # LSTM Pass
        lstm_out, _ = self.lstm(combined)

        # Take last time step output
        last_step = lstm_out[:, -1, :]

        # Prediction
        out = self.fc(last_step)
        return out
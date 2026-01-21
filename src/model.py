import torch
import torch.nn as nn

class EVChargingLSTM(nn.Module):
    def __init__(self, hidden_dim, num_layers, dropout=0.2):
        super(EVChargingLSTM, self).__init__()
        
        # Embeddings
        self.hour_embedding = nn.Embedding(24, 4)      # Map 0-23 to vector of size 4
        self.day_embedding = nn.Embedding(7, 2)        # Map 0-6 to vector of size 2
        
        # Input Dimension Calculation:
        # 4 numeric features (avail, total, lat, lon) + 4 (hour_emb) + 2 (day_emb) = 10
        input_dim = 10
        
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
        # Features indices: 0:4 numeric, 4: hour, 5: day
        
        numeric = x[:, :, 0:4].float()
        hour_idx = x[:, :, 4].long()
        day_idx = x[:, :, 5].long()
        
        # Get embeddings
        hour_emb = self.hour_embedding(hour_idx)
        day_emb = self.day_embedding(day_idx)
        
        # Concatenate: (batch, seq_len, 4+4+2)
        combined = torch.cat([numeric, hour_emb, day_emb], dim=2)
        
        # LSTM Pass
        lstm_out, _ = self.lstm(combined)
        
        # Take last time step output
        last_step = lstm_out[:, -1, :]
        
        # Prediction
        out = self.fc(last_step)
        return out
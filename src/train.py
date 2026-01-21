import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
import os

from src.db import load_history, init_db
from src.preprocessing import DataPreprocessor, create_sequences
from src.dataset import TimeSeriesDataset
from src.model import EVChargingLSTM
from src.config import Config

def train_model():
    # 1. Load Data
    init_db()
    df = load_history()
    
    if len(df) < Config.SEQ_LENGTH + 20:
        print("Not enough data to train. Run data_collector.py first.")
        return

    print(f"Training on {len(df)} records...")

    # 2. Preprocess
    preprocessor = DataPreprocessor()
    preprocessor.fit(df)
    df_processed = preprocessor.transform(df)
    preprocessor.save()
    
    # 3. Create Sequences (Sliding Window)
    X, y = create_sequences(df_processed, Config.SEQ_LENGTH)
    
    # 4. Split (Time-aware, not random shuffle of sequences ideally, but for simplicity here)
    # Ideally: Train on first 80% time, Test on last 20%
    split_idx = int(len(X) * 0.8)
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]
    
    train_dataset = TimeSeriesDataset(X_train, y_train)
    val_dataset = TimeSeriesDataset(X_val, y_val)
    
    train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE)
    
    # 5. Initialize Model
    model = EVChargingLSTM(hidden_dim=Config.HIDDEN_DIM, num_layers=Config.NUM_LAYERS)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=Config.LEARNING_RATE)
    
    # 6. Training Loop
    best_loss = float('inf')
    
    for epoch in range(Config.EPOCHS):
        model.train()
        train_loss = 0
        for seq, target in train_loader:
            optimizer.zero_grad()
            output = model(seq)
            loss = criterion(output.squeeze(), target)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for seq, target in val_loader:
                output = model(seq)
                loss = criterion(output.squeeze(), target)
                val_loss += loss.item()
        
        avg_train = train_loss / len(train_loader)
        avg_val = val_loss / len(val_loader)
        
        print(f"Epoch {epoch+1}/{Config.EPOCHS} | Train Loss: {avg_train:.4f} | Val Loss: {avg_val:.4f}")
        
        if avg_val < best_loss:
            best_loss = avg_val
            if not os.path.exists("models"): os.makedirs("models")
            torch.save(model.state_dict(), Config.MODEL_PATH)
            print("  -> Model Saved")

if __name__ == "__main__":
    train_model()
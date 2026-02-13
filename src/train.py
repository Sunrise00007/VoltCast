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

import argparse

def train_model(mode='global', station_id=None):
    # 1. Load Data
    init_db()
    df = load_history()
    
    if len(df) < Config.SEQ_LENGTH + 20:
        print("Not enough data to train. Run data_collector.py or scripts/generate_large_dataset.py first.")
        return

    print(f"Total records available: {len(df)}")

    if mode == 'per_station':
        # Train a model per station (either specific station_id or iterate all)
        stations = []
        if station_id:
            stations = [int(station_id)]
        else:
            from src.db import get_stations
            stations = [s['id'] for s in get_stations()]

        for sid in stations:
            print(f"\nTraining model for Station {sid}...")
            df_s = df[df['station_id'] == sid].copy()
            if len(df_s) < Config.SEQ_LENGTH + 20:
                print(f"  - Skipping Station {sid}: insufficient data ({len(df_s)} records)")
                continue

            preprocessor = DataPreprocessor()
            preprocessor.fit(df_s)
            df_processed = preprocessor.transform(df_s)

            # For per-station models we do NOT include station_id and do not use embeddings
            X, y = create_sequences(df_processed, Config.SEQ_LENGTH, include_station_id=False)
            split_idx = int(len(X) * 0.8)
            X_train, X_val = X[:split_idx], X[split_idx:]
            y_train, y_val = y[:split_idx], y[split_idx:]

            train_dataset = TimeSeriesDataset(X_train, y_train)
            val_dataset = TimeSeriesDataset(X_val, y_val)

            train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, shuffle=True)
            val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE)

            # Per-station model: no station embedding (model receives only numeric+time features)
            model = EVChargingLSTM(
                hidden_dim=Config.HIDDEN_DIM,
                num_layers=Config.NUM_LAYERS,
                station_emb_dim=0,  # disable station embedding
                num_stations=1
            )
            criterion = nn.MSELoss()
            optimizer = optim.Adam(model.parameters(), lr=Config.LEARNING_RATE)

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

                model.eval()
                val_loss = 0
                with torch.no_grad():
                    for seq, target in val_loader:
                        output = model(seq)
                        loss = criterion(output.squeeze(), target)
                        val_loss += loss.item()

                avg_train = train_loss / len(train_loader)
                avg_val = val_loss / len(val_loader)
                print(f"  Epoch {epoch+1}/{Config.EPOCHS} | Train Loss: {avg_train:.4f} | Val Loss: {avg_val:.4f}")

                if avg_val < best_loss:
                    best_loss = avg_val
                    path = f"models/model_station_{sid}.pt"
                    if not os.path.exists("models"): os.makedirs("models")
                    torch.save(model.state_dict(), path)
                    # Save scaler for this station
                    import joblib
                    scaler_path = f"models/scaler_station_{sid}.joblib"
                    joblib.dump(preprocessor.scaler, scaler_path)
                    print(f"    -> Saved {path} and {scaler_path}")

    else:
        # Global model using all data (includes station_id as a feature)
        print("Training global model on all stations...")
        preprocessor = DataPreprocessor()
        preprocessor.fit(df)
        df_processed = preprocessor.transform(df)
        preprocessor.save()

        # Global model: include station_id so model can use learned embeddings
        X, y = create_sequences(df_processed, Config.SEQ_LENGTH, include_station_id=True)
        split_idx = int(len(X) * 0.8)
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]

        train_dataset = TimeSeriesDataset(X_train, y_train)
        val_dataset = TimeSeriesDataset(X_val, y_val)

        train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE)

        # Use global station count so embeddings are correctly sized
        num_stations = int(df['station_id'].max()) + 1 if 'station_id' in df.columns else 100
        model = EVChargingLSTM(
            hidden_dim=Config.HIDDEN_DIM,
            num_layers=Config.NUM_LAYERS,
            station_emb_dim=Config.STATION_EMBED_DIM,
            num_stations=num_stations
        )
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=Config.LEARNING_RATE)

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['global', 'per_station'], default='global')
    parser.add_argument('--station', type=int, help='Station id to train (only for per_station mode)')
    parser.add_argument('--epochs', type=int, help='Override number of epochs')
    parser.add_argument('--batch-size', type=int, help='Override batch size')
    parser.add_argument('--lr', type=float, help='Override learning rate')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()

    # Allow CLI overrides to Config
    if args.epochs:
        Config.EPOCHS = args.epochs
    if args.batch_size:
        Config.BATCH_SIZE = args.batch_size
    if args.lr:
        Config.LEARNING_RATE = args.lr

    train_model(mode=args.mode, station_id=args.station)
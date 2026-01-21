import torch
import numpy as np
from torch.utils.data import DataLoader
from src.model import EVChargingLSTM
from src.config import Config
from src.db import load_history, init_db
from src.preprocessing import DataPreprocessor, create_sequences
from src.dataset import TimeSeriesDataset
from sklearn.metrics import mean_squared_error, mean_absolute_error

def evaluate():
    init_db()
    df = load_history()
    
    if len(df) < Config.SEQ_LENGTH + 20:
        print("Not enough data to evaluate. Run data_collector.py first.")
        return
    
    # Load preprocessor and preprocess data
    preprocessor = DataPreprocessor()
    preprocessor.load()
    df_processed = preprocessor.transform(df)
    
    # Create sequences
    X, y = create_sequences(df_processed, Config.SEQ_LENGTH)
    
    # Use last 20% for evaluation
    split_idx = int(len(X) * 0.8)
    X_val = X[split_idx:]
    y_val = y[split_idx:]
    
    if len(X_val) == 0:
        print("Not enough validation data.")
        return
    
    val_dataset = TimeSeriesDataset(X_val, y_val)
    val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE)
    
    # Load model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = EVChargingLSTM(hidden_dim=Config.HIDDEN_DIM, num_layers=Config.NUM_LAYERS)
    model.load_state_dict(torch.load(Config.MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()
    
    # Evaluate
    preds = []
    y_true = []
    with torch.no_grad():
        for seq, target in val_loader:
            seq = seq.to(device)
            p = model(seq).cpu().numpy()
            preds.extend(p.flatten())
            y_true.extend(target.numpy())
    
    mse = mean_squared_error(y_true, preds)
    mae = mean_absolute_error(y_true, preds)
    
    print(f"Validation MSE: {mse:.4f}")
    print(f"Validation MAE: {mae:.4f}")

if __name__ == "__main__":
    evaluate()

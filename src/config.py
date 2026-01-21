import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OCM_API_KEY = os.getenv("OCM_API_KEY")
    DB_URL = os.getenv("DB_URL", "sqlite:///./ev_charging.db")
    
    # Geographic Bounds (Defaults to a region in Bangalore/India for relevance)
    LAT_MIN = float(os.getenv("LAT_MIN", "12.8"))
    LAT_MAX = float(os.getenv("LAT_MAX", "13.2"))
    LON_MIN = float(os.getenv("LON_MIN", "77.4"))
    LON_MAX = float(os.getenv("LON_MAX", "77.8"))
    
    # Model Params
    SEQ_LENGTH = 12  # Previous 12 timestamps (e.g., 3 hours if 15m intervals)
    PRED_HORIZON = 1 # Predict next step
    HIDDEN_DIM = 64
    NUM_LAYERS = 2
    DROPOUT = 0.2
    BATCH_SIZE = 32
    EPOCHS = 20
    LEARNING_RATE = 0.001
    
    MODEL_PATH = "models/model.pt"
    SCALER_PATH = "models/scaler.joblib"
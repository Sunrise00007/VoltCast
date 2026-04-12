import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OCM_API_KEY = os.getenv("OCM_API_KEY")
    DB_URL = os.getenv("DB_URL", "sqlite:///./ev_charging.db")
    LAT_MIN = float(os.getenv("LAT_MIN", "12.8"))
    LAT_MAX = float(os.getenv("LAT_MAX", "13.2"))
    LON_MIN = float(os.getenv("LON_MIN", "77.4"))
    LON_MAX = float(os.getenv("LON_MAX", "77.8"))
    SEQ_LENGTH = 12
    PRED_HORIZON = 1
    HIDDEN_DIM = 64
    NUM_LAYERS = 2
    DROPOUT = 0.2
    BATCH_SIZE = 32
    EPOCHS = 20
    LEARNING_RATE = 0.001
    MODEL_PATH = "models/model.pt"
    SCALER_PATH = "models/scaler.joblib"
    STATION_EMBED_DIM = int(os.getenv("STATION_EMBED_DIM", "8"))
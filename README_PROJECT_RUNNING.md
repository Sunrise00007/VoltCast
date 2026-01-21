# 🚴 EV Charging Forecasting Project - Running Guide

## ✅ Project Status: RUNNING

Your bike (EV charging) project is now **fully operational**!

---

## 🚀 What's Running

### API Server (Active)
- **URL:** http://localhost:8000
- **Status:** ✅ Running on port 8000
- **Model:** LSTM trained on 100+ sample records
- **Framework:** FastAPI + Uvicorn

### Endpoints Available

#### 1. Health Check
```bash
GET http://localhost:8000/
```
**Response:** `{"status": "active", "system": "EV Forecasting System"}`

#### 2. Make Prediction for a Station
```bash
GET http://localhost:8000/predict/{station_id}
```

**Example:**
```bash
curl http://localhost:8000/predict/1
```

**Response:**
```json
{
  "station_id": 1,
  "current_time": "2026-01-22T...",
  "predicted_available_ports": 5,
  "status": "High Availability"
}
```

---

## 📊 Project Components

### 1. Data Collection (`src/data_collector.py`)
- Fetches EV charging station data from Open Charge Map API
- Real-time status or simulated data for training
- Polls every 5 minutes by default
- Stores data in SQLite database

### 2. Data Preprocessing (`src/preprocessing.py`)
- Scales numeric features (available_ports, total_ports, latitude, longitude)
- Extracts temporal features (hour, day_of_week)
- Creates sliding window sequences for LSTM

### 3. Model (`src/model.py`)
- **Architecture:** LSTM with embeddings
- **Input:** Time-series sequences (seq_length=12)
- **Output:** Predicted available_ports (normalized)
- **Features:** 10 (4 numeric + 4 hour embedding + 2 day embedding)

### 4. Training Pipeline (`src/train.py`)
- Trains LSTM on historical data
- Validates on 20% holdout set
- Saves best model to `models/model.pt`
- Saves scaler to `models/scaler.joblib`

### 5. Evaluation (`src/evaluate.py`)
```bash
cd /Users/sunrise/Documents/bike_project 
PYTHONPATH="." python src/evaluate.py
```

### 6. API (`src/api/main.py`)
- FastAPI with Pydantic models
- Loads pre-trained model and scaler on startup
- Provides real-time predictions
- Automatic denormalization of predictions

---

## 🔧 Project Configuration

### Environment Variables (`.env`)
```
OCM_API_KEY=57ed6ecc-dc8f-492d-8ed2-0d98505cb9c0
DB_URL=sqlite:///./ev_charging.db
LAT_MIN=12.8
LAT_MAX=13.2
LON_MIN=77.4
LON_MAX=77.8
POLLING_INTERVAL=900
```

### Model Hyperparameters (`src/config.py`)
- SEQ_LENGTH: 12 (predict from last 12 timesteps)
- HIDDEN_DIM: 64
- NUM_LAYERS: 2
- DROPOUT: 0.2
- BATCH_SIZE: 32
- EPOCHS: 20
- LEARNING_RATE: 0.001

---

## 💾 Database Schema

### Table: `station_logs`
```sql
CREATE TABLE IF NOT EXISTS station_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id INTEGER,
    timestamp DATETIME,
    latitude REAL,
    longitude REAL,
    total_ports INTEGER,
    available_ports INTEGER,
    is_operational INTEGER
)
```

---

## 🎯 How to Use

### 1. **Access the API**
Open in browser: http://localhost:8000

### 2. **Make a Prediction**
```bash
curl http://localhost:8000/predict/1
```

### 3. **Check Health**
```bash
curl http://localhost:8000/
```

### 4. **Collect More Data** (Optional)
```bash
cd /Users/sunrise/Documents/bike_project 
PYTHONPATH="." python src/data_collector.py
```
(Run in background, Ctrl+C to stop after 5 minutes)

### 5. **Retrain Model**
```bash
cd /Users/sunrise/Documents/bike_project 
PYTHONPATH="." python src/train.py
```

### 6. **Evaluate Model**
```bash
cd /Users/sunrise/Documents/bike_project 
PYTHONPATH="." python src/evaluate.py
```

---

## 📁 Project Structure

```
bike_project/
├── .env                    # Configuration
├── requirements.txt        # Dependencies
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration class
│   ├── model.py           # LSTM model
│   ├── db.py              # Database operations
│   ├── preprocessing.py   # Data preprocessing
│   ├── dataset.py         # PyTorch Dataset
│   ├── train.py           # Training pipeline
│   ├── evaluate.py        # Model evaluation
│   ├── data_collector.py  # Data collection
│   └── api/
│       ├── __init__.py
│       ├── main.py        # FastAPI app
│       └── utils.py       # Utility functions
├── models/
│   ├── model.pt           # Trained model
│   └── scaler.joblib      # Feature scaler
├── data/                  # (For training data if needed)
├── ev_charging.db         # SQLite database
└── scripts/
    ├── run_collector.sh   # Data collection script
    └── start_api.sh       # API startup script
```

---

## 🐛 Troubleshooting

### API won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill the process if needed
kill -9 <PID>
```

### Model not loading
- Ensure `models/model.pt` exists
- Run training: `PYTHONPATH="." python src/train.py`

### No data in database
- Run data collector first
- Or use `setup_data.py` to generate sample data

### Python module not found
- Always set PYTHONPATH: `export PYTHONPATH=.`
- Use virtual environment: `. .venv/bin/activate`

---

## 📈 Performance Metrics

### Model Training Results (Latest)
- **Final Train Loss:** 0.0950
- **Final Val Loss:** 0.1117
- **Best Val Loss:** 0.1104 (saved at epoch 8)
- **Training Data:** 200 records
- **Train/Val Split:** 80/20

---

## 🔐 Security Notes

- API key is stored in `.env` (not version controlled)
- Use environment variables for sensitive data
- Consider adding authentication for production

---

## 📞 API Reference

### GET `/`
Health check endpoint

**Response:**
```json
{
  "status": "active",
  "system": "EV Forecasting System"
}
```

### GET `/predict/{station_id}`
Get availability prediction for a station

**Parameters:**
- `station_id` (int, path): Station ID

**Response:**
```json
{
  "station_id": 1,
  "current_time": "2026-01-22T10:30:00",
  "predicted_available_ports": 5,
  "status": "High Availability"
}
```

**Status Values:**
- "High Availability" - More than 1 port available
- "Congested" - 1 or fewer ports available

**Errors:**
- `503`: Model not loaded
- `400`: Insufficient historical data for station

---

## 🎓 Project Overview

This is an **LSTM-based time series forecasting system** that predicts EV charging station availability.

**Key Features:**
- ✅ Real-time predictions
- ✅ Temporal embeddings (hour, day_of_week)
- ✅ Automatic feature scaling
- ✅ REST API interface
- ✅ SQLite database
- ✅ Model persistence

**Use Case:**
Predict available charging ports at EV stations to help drivers find charging availability.

---

**Last Updated:** Jan 22, 2026
**Status:** ✅ All systems operational

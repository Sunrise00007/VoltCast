
# ⚡ EV Charging Forecaster 

Real-time EV charging station availability forecasting engine using Deep Learning (LSTM) and FastAPI. An end-to-end ML system solving range anxiety by predicting port congestion.

---

## 📋 Table of Contents               

- [Project Overview](#project-overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Features](#features)
- [Architecture](#architecture)
- [Verification](#verification)
- [API Documentation](#api-documentation)

---

## 🎯 Project Overview.                             

**VoltCast** is a complete end-to-end machine learning system that:
- Predicts EV charging station availability using LSTM neural networks
- Provides real-time forecasts via a FastAPI backend
- Displays predictions through an interactive web dashboard
- Stores historical data in SQLite database
- Uses scikit-learn preprocessing and model evaluation

### What You Get

- ✅ Backend API (FastAPI)
- ✅ LSTM ML Model (PyTorch)
- ✅ SQLite Database
- ✅ Beautiful Interactive Dashboard UI
- ✅ Real-time Predictions
- ✅ Auto-refresh capability

---

## 🚀 Quick Start (1 Minute)

### **Terminal:**
```bash
cd "/Users/sunrise/Documents/bike_project "
PYTHONPATH="." python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### **Expected Output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
Model and artifacts loaded successfully
INFO:     Application startup complete
```

### **Then Open Browser:**
```
http://localhost:8000/dashboard
=======
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
>>>>>>> 15eaf427f89b81c48fa07693b344f137d5d4033a
```

---


## 📦 Installation.                    


### **Requirements**
- Python 3.8+
- pip or conda

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Dependencies:**
- fastapi==0.95.2
- uvicorn==0.22.0
- pandas==2.2.2
- numpy==1.26.4
- torch>=2.1
- scikit-learn==1.3.2
- sqlalchemy>=2.0,<2.1
- joblib==1.3.2
- matplotlib==3.8.1
- pytest==7.4.2
- python-dotenv==1.0.1
- requests==2.31.0
- pydantic==1.10.12
=======
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
>>>>>>> 15eaf427f89b81c48fa07693b344f137d5d4033a

---

## 📁 Project Structure

```
bike_project/

├── requirements.txt              # Python dependencies
├── start_project.sh              # Startup script
├── setup_data.py                 # Data initialization
├── verify_project.py             # Project verification
│
├── data/                         # Data directory
│   └── (CSV files, preprocessed data)
│
├── models/                       # Pre-trained models
│   ├── model.pt                  # LSTM model weights
│   └── scaler.joblib             # Feature scaler
│
├── src/                          # Main source code
│   ├── __init__.py
│   ├── config.py                 # Configuration settings
│   ├── db.py                     # Database setup & queries
│   ├── model.py                  # LSTM model definition
│   ├── dataset.py                # PyTorch dataset class
│   ├── train.py                  # Model training script
│   ├── preprocessing.py          # Data preprocessing
│   ├── data_collector.py         # Data collection utilities
│   ├── evaluate.py               # Model evaluation
│   │
│   └── api/                      # FastAPI backend
│       ├── __init__.py
│       ├── main.py               # API endpoints & app logic
│       ├── utils.py              # Helper functions
│       ├── index.html            # Dashboard UI
│       └── scripts/              # Client-side scripts
│
└── scripts/                      # Utility scripts
    ├── start_api.sh              # API startup
    └── run_collector.sh          # Data collector startup
=======
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
>>>>>>> 15eaf427f89b81c48fa07693b344f137d5d4033a
```

---


## 🏃 How to Run

### **Option 1: Using Startup Script (Recommended)**
```bash
cd "/Users/sunrise/Documents/bike_project "
bash start_project.sh
```

### **Option 2: Manual Start**
```bash
cd "/Users/sunrise/Documents/bike_project "
PYTHONPATH="." python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### **Option 3: Development Mode**
```bash
PYTHONPATH="." python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### **Generate a larger, realistic dataset**
If you want a more realistic dataset (many stations and denser time-series), run the generator which creates station metadata and time-series logs:
```bash
python scripts/generate_large_dataset.py
```
This will populate `ev_charging.db` with the `stations` table and many `station_logs` records.

---

## ✨ Features

### **Dashboard UI**
- Real-time charging station availability display
- Visual representation of available ports
- Auto-refresh capability (30-second intervals)
- Color-coded availability status (🟢 High, 🟡 Medium, 🔴 Low)

### **Predictions**
- LSTM-based time series forecasting
- Multi-step ahead predictions
- Confidence intervals
- Historical trend analysis

### **Backend API**
- RESTful endpoints for predictions
- Health check endpoint
- Real-time data streaming
- Error handling and logging

### **Data Management**
- SQLite database for persistence
- Automated data preprocessing
- Feature scaling and normalization
- Train/test data splitting

---

## 🏗️ Architecture

### **Technology Stack**
```
Frontend: HTML5, CSS3, JavaScript (Dashboard)
    ↓
Backend: FastAPI (Python Web Framework)
    ↓
ML Model: PyTorch LSTM (Neural Network)
    ↓
Data Processing: Pandas, NumPy, Scikit-learn
    ↓
Database: SQLite
```

### **Data Flow**
```
Raw Data → Preprocessing → Feature Scaling → LSTM Model → Predictions
                                                    ↓
                                            FastAPI Endpoint
                                                    ↓
                                            Web Dashboard
```

### **Model Architecture**
- **Type:** LSTM (Long Short-Term Memory)
- **Input:** Time series data of charging station ports
- **Output:** Predicted availability for next time steps
- **Layers:** Multiple LSTM layers with dropout regularization

---

## ✅ Verification

### **Check Project Status**
```bash
python verify_project.py
```

This will verify:
- ✅ All required files exist
- ✅ Dependencies installed
- ✅ Model weights loaded
- ✅ Database connectivity
- ✅ API functionality

### **Manual Verification**

1. **Start the API:**
   ```bash
   PYTHONPATH="." python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Check Health Endpoint:**
   ```bash
   curl http://localhost:8000/
   ```
   Expected: `{"status": "ok"}`

3. **Check Dashboard:**
   ```
   http://localhost:8000/dashboard
   ```
   Expected: Interactive UI with station predictions

4. **Run Tests (if available):**
   ```bash
   pytest src/
   ```

---

## 🔌 API Documentation

### **Base URL**
```
http://localhost:8000
```

### **Endpoints**

#### **1. Health Check**
```http
GET /
```
Returns: `{"status": "ok"}`

#### **2. Dashboard**
```http
GET /dashboard
```
Returns: Interactive HTML dashboard

#### **3. API Predictions & Stations** (Check `src/api/main.py` for complete endpoints)
```http
GET /predict/{station_id}         # Get availability prediction for a station
GET /stations                    # List all stations and metadata
GET /stations/{station_id}/navigate  # Returns a Google Maps deep-link to navigate to the station
POST /api/forecast               # (reserved) Advanced forecast endpoint
```

### **Response Format**
```json
{
  "status": "success",
  "data": {
    "station_id": "station_1",
    "available_ports": 5,
    "total_ports": 10,
    "timestamp": "2025-01-25T10:30:00",
    "prediction": [5, 6, 4, 3, 2]
  }
}
```

---

## 🔧 Configuration

Edit `src/config.py` to customize:
- Model hyperparameters
- Database settings
- API host/port
- Data preprocessing parameters
- LSTM model architecture

---

## 📝 Key Files

| File | Purpose |
|------|---------|
| `src/api/main.py` | FastAPI application and endpoints |
| `src/model.py` | LSTM model definition |
| `src/train.py` | Model training pipeline |
| `src/preprocessing.py` | Data preprocessing logic |
| `src/db.py` | Database operations |
| `src/api/index.html` | Dashboard UI |
| `requirements.txt` | Python dependencies |

---

## 🐛 Troubleshooting

### **Port Already in Use**
```bash
PYTHONPATH="." python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8001 --reload
```
(Change port to 8001)

### **Model Not Found**
```bash
python setup_data.py
```
(Reinitialize data and models)

### **PYTHONPATH Error**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```
(Set Python path explicitly)

### **Dependencies Missing**
```bash
pip install -r requirements.txt --upgrade
```
(Reinstall all dependencies)

---

## 📚 Development

### **Train Model**
You can train a global model that uses station_id as a feature, or train individual per-station models.

Global model (single model for all stations):
```bash
PYTHONPATH="." python src/train.py --mode global
```

Per-station models (saves a model per station):
```bash
# Train all stations (skips stations without enough data)
PYTHONPATH="." python src/train.py --mode per_station

# Train a single station (e.g., station 1)
PYTHONPATH="." python src/train.py --mode per_station --station 1
```

Note: model and scaler files are saved to `models/` as `model.pt` (global) and `model_station_{id}.pt` plus `scaler_station_{id}.joblib` for per-station models.

We now use a learned station embedding (small vector per station) as an input feature to the global model. Per-station models do not use station embeddings (they are trained on each station's data individually).

- Global model: learns a station embedding (controlled by `STATION_EMBED_DIM`) and uses it as an input. This helps the model learn station-specific behavior while still sharing information across stations.
- Per-station models: embeddings are disabled and the model trains on numeric + time features only, which keeps per-station models smaller and simpler.
### **Evaluate Model**
```bash
PYTHONPATH="." python src/evaluate.py
```

### **Collect Data**
```bash
bash scripts/run_collector.sh
```

---

## 📄 License

See LICENSE file for details.

---

## 📞 Support

For issues or questions, verify the setup with:
```bash
python verify_project.py
```

Then check logs in the terminal output.

---

**Last Updated:** January 25, 2026  
**Status:** ✅ Production Ready
=======
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
>>>>>>> 15eaf427f89b81c48fa07693b344f137d5d4033a

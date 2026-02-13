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

## 🎯 Project Overview

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
```

---

## 📦 Installation

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

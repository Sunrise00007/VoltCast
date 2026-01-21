# 📋 HOW TO VERIFY PROJECT IS WORKING

## Quick Verification (Easy Way) ✅

### Method 1: Run Verification Script
```bash
cd "/Users/sunrise/Documents/bike_project "
PYTHONPATH="." python verify_project.py
```

**You should see:** ✅ ALL CHECKS PASSED

---

## Manual Verification (Step by Step)

### ✅ Check 1: Files Exist
```bash
ls -lh "/Users/sunrise/Documents/bike_project /models/model.pt"
ls -lh "/Users/sunrise/Documents/bike_project /models/scaler.joblib"  
ls -lh "/Users/sunrise/Documents/bike_project /ev_charging.db"
```

**Expected:** All three files should exist with sizes:
- `model.pt`: ~215 KB
- `scaler.joblib`: ~1 KB
- `ev_charging.db`: ~24 KB

---

### ✅ Check 2: Database Has Data
```bash
cd "/Users/sunrise/Documents/bike_project "
PYTHONPATH="." python -c "
from src.db import load_history
df = load_history()
print(f'Total records: {len(df)}')
print(f'Stations: {df[\"station_id\"].nunique()}')
print(df.head(2))
"
```

**Expected Output:**
```
Total records: 200
Stations: 5
```

---

### ✅ Check 3: API is Running
```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{"status":"active","system":"EV Forecasting System"}
```

**If you get "Connection refused":** Start the API first:
```bash
cd "/Users/sunrise/Documents/bike_project "
PYTHONPATH="." python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

---

### ✅ Check 4: Model Works (Make Prediction)
```bash
curl http://localhost:8000/predict/1
```

**Expected Response:**
```json
{
  "station_id": 1,
  "current_time": "2026-01-22T...",
  "predicted_available_ports": 5.0,
  "status": "High Availability"
}
```

---

### ✅ Check 5: All Stations Work
```bash
for station in 1 2 3 4 5; do
  echo "Station $station:"
  curl -s http://localhost:8000/predict/$station
  echo ""
done
```

**Expected:** All 5 stations return predictions ✅

---

## What Each Status Means

| Status | Meaning |
|--------|---------|
| 🟢 **All Checks Passed** | Project is 100% working! |
| 🟡 **Files Missing** | Need to train model: `PYTHONPATH="." python src/train.py` |
| 🔴 **API Not Responding** | Start API: `PYTHONPATH="." python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000` |
| 🔴 **Model Loading Failed** | Retrain model or check if files are corrupt |

---

## Troubleshooting

### API says "Model not loaded"
**Fix:** 
```bash
cd "/Users/sunrise/Documents/bike_project "
PYTHONPATH="." python src/train.py
```

### Database says "No records"
**Fix:**
```bash
cd "/Users/sunrise/Documents/bike_project "
PYTHONPATH="." python setup_data.py
```

### "Module not found" error
**Fix:**
```bash
cd "/Users/sunrise/Documents/bike_project "
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| **Verify Everything** | `PYTHONPATH="." python verify_project.py` |
| **Start API** | `PYTHONPATH="." python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000` |
| **Train Model** | `PYTHONPATH="." python src/train.py` |
| **Generate Sample Data** | `PYTHONPATH="." python setup_data.py` |
| **Evaluate Model** | `PYTHONPATH="." python src/evaluate.py` |
| **Test Health** | `curl http://localhost:8000/` |
| **Test Prediction** | `curl http://localhost:8000/predict/1` |

---

## Expected Project Structure

```
✅ models/
   ├── model.pt (trained LSTM)
   └── scaler.joblib (feature scaler)

✅ ev_charging.db (SQLite database)

✅ API running on :8000
   ├── / (health check)
   └── /predict/{station_id} (predictions)

✅ 200 training records in database

✅ All dependencies installed
```

---

## Success Indicators ✨

If you see these, **PROJECT IS WORKING PERFECTLY**:

1. ✅ `verify_project.py` shows all tests passed
2. ✅ API responds to `http://localhost:8000/`
3. ✅ Predictions return for all stations
4. ✅ Database has 200+ records
5. ✅ Model and scaler files exist

**Congratulations! Your EV Charging Forecasting Project is fully operational! 🎉**

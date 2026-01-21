#!/usr/bin/env python3
"""
Project Status Verification Script
Run this to check if the EV Charging Forecasting project is working properly
"""

import os
import sys
import sqlite3
from pathlib import Path

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
CHECK = '✅'
CROSS = '❌'
ARROW = '➜'

def print_header(text):
    print(f"\n{BLUE}{'='*50}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*50}{RESET}\n")

def print_status(name, status, details=""):
    status_text = f"{GREEN}{CHECK} PASS{RESET}" if status else f"{RED}{CROSS} FAIL{RESET}"
    print(f"{ARROW} {name}: {status_text}")
    if details:
        print(f"  {details}")

def check_file_exists(filepath, name):
    exists = os.path.isfile(filepath)
    size = os.path.getsize(filepath) if exists else 0
    print_status(name, exists, f"Size: {size:,} bytes" if exists else "File not found")
    return exists

def check_database():
    db_path = "/Users/sunrise/Documents/bike_project /ev_charging.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Check record count
        cursor.execute("SELECT COUNT(*) FROM station_logs")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        print_status("Database Exists", True)
        print(f"  Tables: {[t[0] for t in tables]}")
        print(f"  Records: {count:,}")
        return True
    except Exception as e:
        print_status("Database Check", False, str(e))
        return False

def check_imports():
    """Test if all required modules can be imported"""
    required_modules = [
        'torch',
        'pandas',
        'numpy',
        'sklearn',
        'fastapi',
        'pydantic',
        'joblib',
    ]
    
    all_ok = True
    for module in required_modules:
        try:
            __import__(module)
            print_status(f"Module: {module}", True)
        except ImportError as e:
            print_status(f"Module: {module}", False, str(e))
            all_ok = False
    
    return all_ok

def check_model():
    """Test if model can be loaded"""
    try:
        import torch
        from src.model import EVChargingLSTM
        from src.config import Config
        
        model = EVChargingLSTM(
            hidden_dim=Config.HIDDEN_DIM,
            num_layers=Config.NUM_LAYERS
        )
        state = torch.load(Config.MODEL_PATH, map_location='cpu')
        model.load_state_dict(state)
        model.eval()
        
        print_status("Model Loading", True, "LSTM model loaded successfully")
        return True
    except Exception as e:
        print_status("Model Loading", False, str(e))
        return False

def check_scaler():
    """Test if scaler can be loaded"""
    try:
        import joblib
        from src.config import Config
        
        scaler = joblib.load(Config.SCALER_PATH)
        print_status("Scaler Loading", True, "Feature scaler loaded successfully")
        return True
    except Exception as e:
        print_status("Scaler Loading", False, str(e))
        return False

def test_api():
    """Test if API is responding"""
    try:
        import requests
        response = requests.get("http://localhost:8000/", timeout=5)
        
        if response.status_code == 200:
            print_status("API Health Check", True, f"Status: {response.status_code}")
            return True
        else:
            print_status("API Health Check", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_status("API Health Check", False, "API not responding (start with: python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000)")
        return False

def main():
    os.chdir("/Users/sunrise/Documents/bike_project ")
    sys.path.insert(0, "/Users/sunrise/Documents/bike_project ")
    
    print(f"\n{YELLOW}🚗 EV CHARGING FORECASTING PROJECT - STATUS CHECK{RESET}")
    
    # 1. File checks
    print_header("1. FILE VERIFICATION")
    model_ok = check_file_exists(
        "/Users/sunrise/Documents/bike_project /models/model.pt",
        "Trained Model"
    )
    scaler_ok = check_file_exists(
        "/Users/sunrise/Documents/bike_project /models/scaler.joblib",
        "Feature Scaler"
    )
    db_ok = check_file_exists(
        "/Users/sunrise/Documents/bike_project /ev_charging.db",
        "Database"
    )
    
    # 2. Database check
    print_header("2. DATABASE VERIFICATION")
    db_check_ok = check_database()
    
    # 3. Dependencies check
    print_header("3. DEPENDENCIES CHECK")
    deps_ok = check_imports()
    
    # 4. Model check
    print_header("4. MODEL & SCALER CHECK")
    model_load_ok = check_model()
    scaler_load_ok = check_scaler()
    
    # 5. API check
    print_header("5. API VERIFICATION")
    api_ok = test_api()
    
    # Summary
    print_header("SUMMARY")
    all_checks = [model_ok, scaler_ok, db_ok, db_check_ok, deps_ok, model_load_ok, scaler_load_ok, api_ok]
    passed = sum(all_checks)
    total = len(all_checks)
    
    if passed == total:
        print(f"{GREEN}🎉 ALL CHECKS PASSED! Project is working perfectly!{RESET}\n")
        print(f"✅ Model: Ready")
        print(f"✅ Database: {db_check_ok and 'Ready' or 'Check failed'}")
        print(f"✅ Dependencies: All installed")
        print(f"✅ API: {'Running' if api_ok else 'Not running (start it to complete)'}")
        return 0
    else:
        print(f"{RED}⚠️  {total - passed} check(s) failed. Please review above.{RESET}\n")
        if not api_ok:
            print(f"{YELLOW}💡 To start the API, run:{RESET}")
            print(f'   cd "/Users/sunrise/Documents/bike_project "')
            print(f'   PYTHONPATH="." python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000')
        return 1

if __name__ == "__main__":
    exit(main())

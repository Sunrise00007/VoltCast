#!/bin/bash

# EV Charging Forecaster - Complete Project Launcher
# This script starts the entire project end-to-end

PROJECT_DIR="/Users/sunrise/Documents/bike_project "
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🚗 EV CHARGING FORECASTER - PROJECT LAUNCHER 🚗           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Project directory not found: $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"
echo "✅ Project directory found"
echo ""

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found"
    exit 1
fi

echo "✅ Virtual environment active"
echo ""

# Set Python path
export PYTHONPATH="."

# Start the API server
echo "🚀 Starting API Server..."
echo "   URL: http://localhost:8000"
echo "   Dashboard: http://localhost:8000/dashboard"
echo ""
echo "Press Ctrl+C to stop the server"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Run the server
"$VENV_PYTHON" -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

#!/usr/bin/env python
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import random
from src.db import get_connection, init_db
from src.config import Config

# Initialize DB
init_db()

# Generate sample data for training
print("Generating sample training data...")
conn = get_connection()
records = []

# Create 100 data points across different stations and times
base_time = datetime.now() - timedelta(days=5)
for station_id in range(1, 6):  # 5 stations
    for i in range(20):  # 20 timestamps per station
        timestamp = base_time + timedelta(hours=i*6)
        records.append({
            'station_id': station_id,
            'timestamp': timestamp,
            'latitude': Config.LAT_MIN + random.random() * (Config.LAT_MAX - Config.LAT_MIN),
            'longitude': Config.LON_MIN + random.random() * (Config.LON_MAX - Config.LON_MIN),
            'total_ports': random.randint(4, 20),
            'available_ports': random.randint(0, 10),
            'is_operational': 1
        })

df = pd.DataFrame(records)
df.to_sql('station_logs', conn, if_exists='append', index=False)
conn.close()
print(f"✓ Generated {len(df)} sample records")

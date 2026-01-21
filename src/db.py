import sqlite3
import pandas as pd
from src.config import Config

def get_connection():
    conn = sqlite3.connect(Config.DB_URL.replace("sqlite:///", ""))
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for storing time-series logs of station status
    cursor.execute("""
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
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized.")

def save_records(records):
    if not records:
        return
    conn = get_connection()
    df = pd.DataFrame(records)
    df.to_sql('station_logs', conn, if_exists='append', index=False)
    conn.close()

def load_history(station_id=None):
    conn = get_connection()
    query = "SELECT * FROM station_logs"
    if station_id:
        query += f" WHERE station_id = {station_id}"
    query += " ORDER BY timestamp ASC"
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df
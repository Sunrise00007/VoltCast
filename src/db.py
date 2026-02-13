import sqlite3
import pandas as pd
from src.config import Config

def get_connection():
    conn = sqlite3.connect(Config.DB_URL.replace("sqlite:///", ""))
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for storing station metadata
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER PRIMARY KEY,
        name TEXT,
        latitude REAL,
        longitude REAL,
        address TEXT,
        type TEXT,
        total_ports INTEGER
    )
    """)
    
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


def save_stations(stations):
    """Save a list of station metadata dicts to the stations table."""
    if not stations:
        return
    conn = get_connection()
    df = pd.DataFrame(stations)
    df.to_sql('stations', conn, if_exists='replace', index=False)
    conn.close()


def get_stations():
    """Return a list of station metadata as dicts."""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM stations ORDER BY id ASC", conn)
    conn.close()
    return df.to_dict('records')


def get_station(station_id):
    """Return a single station or None."""
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM stations WHERE id = {int(station_id)}", conn)
    conn.close()
    if df.empty:
        return None
    return df.to_dict('records')[0]


def save_station_logs(records):
    """Convenience helper to append station logs (wraps existing save_records)."""
    save_records(records)
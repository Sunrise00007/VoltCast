import requests
import time
import random
from datetime import datetime
from src.config import Config
from src.db import init_db, save_records

def fetch_ocm_data():
    """
    Fetches data from Open Charge Map API.
    Note: Real-time status in OCM is sparse. 
    If status is missing, we simulate realistic availability based on time of day
    to ensure the model has training data for this project demonstration.
    """
    url = "https://api.openchargemap.io/v3/poi/"
    params = {
        "output": "json",
        "key": Config.OCM_API_KEY,
        "latitude": (Config.LAT_MIN + Config.LAT_MAX) / 2,
        "longitude": (Config.LON_MIN + Config.LON_MAX) / 2,
        "distance": 50, # km
        "distanceunit": "KM",
        "maxresults": 100
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        records = []
        current_time = datetime.now()
        
        for item in data:
            station_id = item.get('ID')
            addr_info = item.get('AddressInfo', {})
            lat = addr_info.get('Latitude')
            lon = addr_info.get('Longitude')
            
            # Count connections
            connections = item.get('Connections', [])
            total_ports = len(connections)
            if total_ports == 0: continue # Skip invalid stations
            
            # Try to get real status, otherwise simulate for training purposes
            # StatusTypeID: 50 = Operational
            operational_ports = 0
            has_real_status = False
            
            for conn in connections:
                status = conn.get('StatusType', {})
                if status and status.get('IsOperational') == True:
                    operational_ports += 1
                    has_real_status = True
            
            # SIMULATION BLOCK (For robust training data if API lacks real-time updates)
            if not has_real_status:
                # Simulate usage: Busy in evenings (17-21), Free at night
                hour = current_time.hour
                usage_prob = 0.1
                if 8 <= hour <= 11: usage_prob = 0.6
                if 17 <= hour <= 21: usage_prob = 0.9
                
                occupied = 0
                for _ in range(total_ports):
                    if random.random() < usage_prob:
                        occupied += 1
                available_ports = max(0, total_ports - occupied)
                is_operational = 1
            else:
                available_ports = operational_ports # Simplified for real data
                is_operational = 1 if available_ports > 0 else 0

            records.append({
                "station_id": station_id,
                "timestamp": current_time,
                "latitude": lat,
                "longitude": lon,
                "total_ports": total_ports,
                "available_ports": available_ports,
                "is_operational": is_operational
            })
            
        return records
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def run_collector_loop():
    init_db()
    print("Starting Data Collector Service...")
    while True:
        print(f"Polling OCM API at {datetime.now()}...")
        records = fetch_ocm_data()
        if records:
            save_records(records)
            print(f"Saved {len(records)} records.")
        else:
            print("No records found.")
        time.sleep(300)  # Wait 5 minutes before next poll

if __name__ == "__main__":
    run_collector_loop()
        
        # Sleep for 15 minutes (or as defined in .env)
        time.sleep(900)

if __name__ == "__main__":
    run_collector_loop()
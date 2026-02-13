"""Generate a larger, realistic dataset: station metadata + time-series logs.

Usage:
    python scripts/generate_large_dataset.py

This will initialize the DB, create ~30 stations centered around a lat/lon (default SF),
and produce 15-minute logs for 7 days for each station.
"""

import random
import datetime
from src.db import init_db, save_stations, save_station_logs


def generate(center_lat=37.7749, center_lon=-122.4194, num_stations=30, days=7, interval_minutes=15):
    init_db()

    stations = []
    for sid in range(1, num_stations + 1):
        lat = center_lat + (random.random() - 0.5) * 0.06
        lon = center_lon + (random.random() - 0.5) * 0.06
        stations.append({
            "id": sid,
            "name": f"Station {sid}",
            "latitude": lat,
            "longitude": lon,
            "address": f"{sid} Example St"
        })
    save_stations(stations)

    records = []
    start = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    periods = int(days * 24 * 60 / interval_minutes)

    for s in stations:
        total_ports = random.randint(6, 20)
        t = start
        for _ in range(periods):
            hour = t.hour
            if 7 <= hour <= 10:
                usage = 0.6
            elif 16 <= hour <= 19:
                usage = 0.8
            else:
                usage = 0.2
            # Simulate occupancy with some noise
            occupied = min(total_ports, max(0, int(random.gauss(total_ports * usage, 1.5))))
            available = max(0, total_ports - occupied)
            records.append({
                "station_id": s['id'],
                "timestamp": t,
                "latitude": s['latitude'],
                "longitude": s['longitude'],
                "total_ports": total_ports,
                "available_ports": available,
                "is_operational": 1
            })
            t += datetime.timedelta(minutes=interval_minutes)

    # Save all logs in batches (this may be large)
    save_station_logs(records)
    print(f"Generated {len(stations)} stations and {len(records)} log records")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate synthetic station dataset')
    parser.add_argument('--num-stations', type=int, default=30, help='Number of stations to generate')
    parser.add_argument('--days', type=int, default=7, help='Number of days of history')
    parser.add_argument('--interval', type=int, default=15, help='Interval minutes between records')
    parser.add_argument('--lat', type=float, default=37.7749, help='Center latitude')
    parser.add_argument('--lon', type=float, default=-122.4194, help='Center longitude')
    args = parser.parse_args()

    generate(center_lat=args.lat, center_lon=args.lon, num_stations=args.num_stations, days=args.days, interval_minutes=args.interval)
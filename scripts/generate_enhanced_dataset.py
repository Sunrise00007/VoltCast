#!/usr/bin/env python3
"""
Enhanced Dataset Generator for EV Charging Stations
Generates realistic station data with:
- More stations (50-100)
- Realistic usage patterns
- Varied station types (residential, commercial, highway)
- Better geographic distribution
- More dynamic availability patterns
"""

import random
import datetime
import math
from src.db import init_db, save_stations, save_station_logs

# Station types with different usage patterns
STATION_TYPES = {
    'residential': {
        'ports_range': (2, 8),
        'peak_hours': [(18, 22), (6, 9)],  # Evening and morning
        'base_usage': 0.3,
        'peak_usage': 0.9
    },
    'commercial': {
        'ports_range': (4, 12),
        'peak_hours': [(8, 12), (13, 17)],  # Business hours
        'base_usage': 0.2,
        'peak_usage': 0.8
    },
    'highway': {
        'ports_range': (6, 20),
        'peak_hours': [(11, 20)],  # Long daytime peak
        'base_usage': 0.4,
        'peak_usage': 0.95
    },
    'downtown': {
        'ports_range': (8, 25),
        'peak_hours': [(7, 10), (16, 19)],  # Rush hours
        'base_usage': 0.25,
        'peak_usage': 0.85
    }
}

# Bay Area coordinates for realistic distribution
BAY_AREA_LOCATIONS = [
    {'name': 'San Francisco', 'lat': 37.7749, 'lon': -122.4194, 'radius': 0.15},
    {'name': 'San Jose', 'lat': 37.3382, 'lon': -121.8863, 'radius': 0.12},
    {'name': 'Oakland', 'lat': 37.8044, 'lon': -122.2711, 'radius': 0.10},
    {'name': 'Palo Alto', 'lat': 37.4419, 'lon': -122.1430, 'radius': 0.08},
    {'name': 'Fremont', 'lat': 37.5485, 'lon': -121.9886, 'radius': 0.08},
]

def get_station_type():
    """Weighted random selection of station type"""
    weights = [0.35, 0.25, 0.20, 0.20]  # residential, commercial, highway, downtown
    return random.choices(list(STATION_TYPES.keys()), weights=weights)[0]

def calculate_usage_pattern(hour, station_type, day_of_week):
    """Calculate realistic usage based on time and station type"""
    config = STATION_TYPES[station_type]
    
    # Weekend vs weekday patterns
    if day_of_week >= 5:  # Weekend
        if station_type == 'commercial':
            return config['base_usage'] * 0.5  # Less commercial usage
        elif station_type == 'residential':
            return config['base_usage'] * 1.2  # More residential usage
        else:
            return config['base_usage']
    
    # Check if current hour is in peak time
    is_peak = any(start <= hour < end for start, end in config['peak_hours'])
    
    if is_peak:
        usage = config['peak_usage']
    else:
        usage = config['base_usage']
    
    # Add some randomness and daily variation
    daily_factor = random.gauss(1.0, 0.15)  # ±15% daily variation
    hourly_noise = random.gauss(0, 0.1)     # ±10% hourly noise
    
    usage = usage * daily_factor + hourly_noise
    return max(0, min(1, usage))  # Clamp between 0 and 1

def generate_realistic_address(station_type, location_name, station_id):
    """Generate realistic addresses based on station type and location"""
    street_types = {
        'residential': ['St', 'Ave', 'Dr', 'Ln', 'Ct'],
        'commercial': ['Blvd', 'St', 'Ave', 'Way', 'Plaza'],
        'highway': ['Hwy', 'Freeway Blvd', 'Service Rd', 'Exit Rd'],
        'downtown': ['St', 'Ave', 'Pl', 'Sq', 'Market St']
    }
    
    street_names = [
        'Oak', 'Pine', 'Elm', 'Maple', 'Cedar', 'Park', 'Main', 
        'First', 'Second', 'Broadway', 'Market', 'California',
        'Mission', 'Howard', 'Folsom', 'Geary', 'Van Ness'
    ]
    
    street_type = random.choice(street_types[station_type])
    street_name = random.choice(street_names)
    number = random.randint(100, 9999)
    
    if station_type == 'highway':
        return f"I-80 Exit {station_id}, {location_name}"
    else:
        return f"{number} {street_name} {street_type}, {location_name}"

def generate_enhanced_dataset(num_stations=50, days=14, interval_minutes=15):
    """Generate enhanced realistic dataset"""
    print(f"🚗 Generating enhanced dataset: {num_stations} stations, {days} days")
    
    init_db()
    
    # Generate stations with realistic distribution
    stations = []
    station_id = 1
    
    # Distribute stations across Bay Area locations
    for location in BAY_AREA_LOCATIONS:
        # Allocate stations based on location size
        location_stations = max(1, int(num_stations * 0.2))  # 20% per location roughly
        
        for i in range(location_stations):
            if station_id > num_stations:
                break
                
            station_type = get_station_type()
            
            # Generate coordinates within location radius
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, location['radius'])
            lat = location['lat'] + distance * math.cos(angle)
            lon = location['lon'] + distance * math.sin(angle)
            
            # Get station configuration
            config = STATION_TYPES[station_type]
            total_ports = random.randint(*config['ports_range'])
            
            stations.append({
                "id": station_id,
                "name": f"{location['name']} {station_type.title()} Station {station_id}",
                "latitude": lat,
                "longitude": lon,
                "address": generate_realistic_address(station_type, location['name'], station_id),
                "type": station_type,
                "total_ports": total_ports
            })
            
            station_id += 1
    
    # Fill remaining stations if needed
    while station_id <= num_stations:
        location = random.choice(BAY_AREA_LOCATIONS)
        station_type = get_station_type()
        
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, location['radius'])
        lat = location['lat'] + distance * math.cos(angle)
        lon = location['lon'] + distance * math.sin(angle)
        
        config = STATION_TYPES[station_type]
        total_ports = random.randint(*config['ports_range'])
        
        stations.append({
            "id": station_id,
            "name": f"{location['name']} {station_type.title()} Station {station_id}",
            "latitude": lat,
            "longitude": lon,
            "address": generate_realistic_address(station_type, location['name'], station_id),
            "type": station_type,
            "total_ports": total_ports
        })
        
        station_id += 1
    
    print(f"✅ Generated {len(stations)} stations")
    save_stations(stations)
    
    # Generate time-series logs
    records = []
    start = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    periods = int(days * 24 * 60 / interval_minutes)
    
    print(f"📊 Generating {periods} time points per station...")
    
    for station in stations:
        total_ports = station['total_ports']
        station_type = station['type']
        
        t = start
        for period in range(periods):
            hour = t.hour
            day_of_week = t.weekday()  # 0 = Monday, 6 = Sunday
            
            # Calculate realistic usage
            usage = calculate_usage_pattern(hour, station_type, day_of_week)
            
            # Add temporal correlation (smooth transitions)
            if period > 0:
                # Get previous available ports from last record
                prev_available = records[-1]['available_ports'] if records and records[-1]['station_id'] == station['id'] else total_ports
                # Smooth transition (max 30% change per interval)
                max_change = max(1, int(total_ports * 0.3))
                target_occupied = int(total_ports * usage)
                target_available = total_ports - target_occupied
                
                # Smooth the transition
                if abs(target_available - prev_available) > max_change:
                    if target_available > prev_available:
                        target_available = prev_available + max_change
                    else:
                        target_available = max(0, prev_available - max_change)
                
                available = target_available
            else:
                occupied = min(total_ports, max(0, int(random.gauss(total_ports * usage, 1.5))))
                available = max(0, total_ports - occupied)
            
            # Random maintenance events (1% chance)
            is_operational = 0 if random.random() < 0.01 else 1
            if not is_operational:
                available = 0
            
            records.append({
                "station_id": station['id'],
                "timestamp": t,
                "latitude": station['latitude'],
                "longitude": station['longitude'],
                "total_ports": total_ports,
                "available_ports": available,
                "is_operational": is_operational
            })
            
            t += datetime.timedelta(minutes=interval_minutes)
        
        if station['id'] % 10 == 0:
            print(f"   Generated data for station {station['id']}")
    
    # Save all logs
    print(f"💾 Saving {len(records)} log records...")
    save_station_logs(records)
    
    print(f"✨ Enhanced dataset generation complete!")
    print(f"   📍 {len(stations)} stations across {len(BAY_AREA_LOCATIONS)} Bay Area cities")
    print(f"   📈 {len(records)} time-series records")
    print(f"   📅 {days} days of historical data")
    print(f"   ⏱️  {interval_minutes}-minute intervals")
    
    # Print station type distribution
    type_counts = {}
    for station in stations:
        station_type = station['type']
        type_counts[station_type] = type_counts.get(station_type, 0) + 1
    
    print(f"\n📊 Station Type Distribution:")
    for station_type, count in type_counts.items():
        print(f"   {station_type.title()}: {count} stations")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate enhanced realistic EV station dataset')
    parser.add_argument('--num-stations', type=int, default=50, help='Number of stations to generate')
    parser.add_argument('--days', type=int, default=14, help='Number of days of history')
    parser.add_argument('--interval', type=int, default=15, help='Interval minutes between records')
    
    args = parser.parse_args()
    
    generate_enhanced_dataset(
        num_stations=args.num_stations,
        days=args.days,
        interval_minutes=args.interval
    )

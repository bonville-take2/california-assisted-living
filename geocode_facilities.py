"""
RCFE Facility Geocoding Script
Geocodes all RCFE facilities from the CSV file and saves to cache.
Run this once before using the main app.

Usage: python geocode_facilities.py
Time: ~3-4 hours (run overnight)
"""

import csv
import requests
import json
import time
from datetime import datetime

# Configuration
CSV_FILE = 'data/rcfe_data_latest.csv'
CACHE_FILE = 'geocode_cache.json'
RATE_LIMIT_DELAY = 1.0  # Nominatim requires 1 request per second

def geocode_address(address, city, state, zip_code):
    """
    Geocode a single address using Nominatim (OpenStreetMap).

    Args:
        address: Street address
        city: City name
        state: State code
        zip_code: ZIP code

    Returns:
        dict with 'lat' and 'lon' keys, or None if geocoding fails
    """
    # Construct full address
    full_address = f"{address}, {city}, {state} {zip_code}, USA"

    # Nominatim API endpoint
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': full_address,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'us'
    }
    headers = {
        'User-Agent': 'RCFE-Finder/1.0'  # Required by Nominatim
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.ok and response.json():
            data = response.json()[0]
            return {
                'lat': float(data['lat']),
                'lon': float(data['lon'])
            }
        else:
            return None

    except Exception as e:
        print(f"  Error geocoding: {e}")
        return None

def load_existing_cache():
    """Load existing geocode cache if it exists."""
    try:
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_cache(cache):
    """Save geocode cache to file."""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)
    print(f"Cache saved to {CACHE_FILE}")

def main():
    """Main geocoding process."""
    print("=" * 70)
    print("RCFE Facility Geocoding Script")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Load CSV data
    print(f"Loading data from {CSV_FILE}...")
    facilities = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        facilities = list(reader)

    total_facilities = len(facilities)
    print(f"Loaded {total_facilities} facilities")
    print()

    # Load existing cache
    cache = load_existing_cache()
    already_cached = len(cache)
    print(f"Found {already_cached} facilities already geocoded in cache")
    print()

    # Statistics
    geocoded_count = already_cached
    failed_count = 0
    skipped_count = 0

    # Process each facility
    print("Starting geocoding process...")
    print("Progress will be saved every 100 facilities")
    print("-" * 70)

    for row in facilities:
        facility_num = str(row.get('Facility Number', ''))

        # Skip if already in cache
        if facility_num in cache:
            skipped_count += 1
            continue

        # Get address components
        address = row.get('Facility Address', '').strip()
        city = row.get('Facility City', '').strip()
        state = row.get('Facility State', '').strip()
        zip_code = row.get('Facility Zip', '').strip()

        # Skip if missing critical address components
        if not address or not city or not state:
            print(f"Skipping {facility_num}: Missing address components")
            failed_count += 1
            continue

        # Geocode the facility
        result = geocode_address(address, city, state, zip_code)

        if result:
            cache[facility_num] = result
            geocoded_count += 1

            # Progress indicator
            if geocoded_count % 10 == 0:
                progress = (geocoded_count / total_facilities) * 100
                print(f"Progress: {geocoded_count}/{total_facilities} ({progress:.1f}%) - "
                      f"Last: {city}, CA")
        else:
            failed_count += 1
            print(f"Failed to geocode {facility_num}: {address}, {city}, {state}")

        # Save checkpoint every 100 facilities
        if (geocoded_count + failed_count) % 100 == 0:
            save_cache(cache)
            print(f"Checkpoint: Cache saved ({geocoded_count} geocoded, {failed_count} failed)")

        # Rate limiting (Nominatim requires 1 request/second)
        time.sleep(RATE_LIMIT_DELAY)

    # Final save
    save_cache(cache)

    # Print summary
    print()
    print("=" * 70)
    print("Geocoding Complete!")
    print("=" * 70)
    print(f"Total facilities: {total_facilities}")
    print(f"Successfully geocoded: {geocoded_count}")
    print(f"Failed: {failed_count}")
    print(f"Skipped (already cached): {skipped_count}")
    print(f"Success rate: {(geocoded_count / total_facilities) * 100:.1f}%")
    print()
    print(f"Cache saved to: {CACHE_FILE}")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == '__main__':
    main()

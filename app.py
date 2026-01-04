"""
RCFE Proximity Search - Flask Backend
Web application for finding RCFE facilities by proximity with violation data.

Usage: python app.py
Access: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import csv
import json
import requests
from math import radians, sin, cos, sqrt, asin
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration
CSV_FILE = 'data/rcfe_data_latest.csv'
CACHE_FILE = 'geocode_cache.json'
NOMINATIM_USER_AGENT = 'RCFE-Finder/1.0'

# Global data (loaded on startup)
facilities_data = None
geocode_cache = None

def load_data():
    """Load CSV data and geocode cache on app startup."""
    global facilities_data, geocode_cache

    print("Loading facilities data...")
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        facilities_data = list(reader)
    print(f"Loaded {len(facilities_data)} facilities")

    print("Loading geocode cache...")
    try:
        with open(CACHE_FILE, 'r') as f:
            geocode_cache = json.load(f)
        print(f"Loaded {len(geocode_cache)} geocoded facilities")
    except FileNotFoundError:
        print(f"Warning: {CACHE_FILE} not found. Run geocode_facilities.py first!")
        geocode_cache = {}

    print("App ready!")

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on Earth.

    Args:
        lat1, lon1: Latitude and longitude of point 1 (in decimal degrees)
        lat2, lon2: Latitude and longitude of point 2 (in decimal degrees)

    Returns:
        Distance in miles
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # Earth radius in miles
    radius_miles = 3959
    return radius_miles * c

def geocode_address(address):
    """
    Geocode an address using Nominatim.

    Args:
        address: Full address string

    Returns:
        dict with 'lat', 'lon', and 'display_name', or None if failed
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit': 1,
        'countrycodes': 'us'
    }
    headers = {
        'User-Agent': NOMINATIM_USER_AGENT
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.ok and response.json():
            data = response.json()[0]
            return {
                'lat': float(data['lat']),
                'lon': float(data['lon']),
                'display_name': data.get('display_name', address)
            }
        else:
            return None

    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

def parse_recent_violations(all_visit_dates, substantiated_allegations):
    """
    Count substantiated allegations from the last 2 years.

    Args:
        all_visit_dates: Comma-separated date string (e.g., "05/22/2025, 04/16/2025, ...")
        substantiated_allegations: Total substantiated allegations (all time)

    Returns:
        Count of recent (last 2 years) violations, or 0 if unable to parse
    """
    if not all_visit_dates or not substantiated_allegations:
        return 0

    try:
        substantiated_allegations = int(substantiated_allegations)
    except (ValueError, TypeError):
        return 0

    if substantiated_allegations == 0:
        return 0

    try:
        # Parse dates
        date_strings = str(all_visit_dates).split(',')
        two_years_ago = datetime.now() - timedelta(days=730)

        recent_count = 0
        for date_str in date_strings:
            date_str = date_str.strip()
            try:
                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                if date_obj >= two_years_ago:
                    recent_count += 1
            except ValueError:
                continue

        # Estimate: if all dates are recent, use full count
        # Otherwise, prorate based on recent date ratio
        total_dates = len(date_strings)
        if total_dates > 0:
            ratio = recent_count / total_dates
            estimated_recent_violations = int(substantiated_allegations * ratio)
            return estimated_recent_violations
        else:
            return 0

    except Exception as e:
        print(f"Error parsing violations: {e}")
        return 0

def check_ownership_change(license_first_date):
    """
    Check if facility has recent ownership change (licensed within last year).

    Args:
        license_first_date: License date string (e.g., "5/20/2010")

    Returns:
        True if licensed within last year, False otherwise
    """
    if not license_first_date or not license_first_date.strip():
        return False

    try:
        date_obj = datetime.strptime(str(license_first_date).strip(), '%m/%d/%Y')
        one_year_ago = datetime.now() - timedelta(days=365)
        return date_obj >= one_year_ago
    except ValueError:
        return False

def get_severity_shade(citation_count):
    """
    Determine shade level based on citation count.
    Uses neutral shading to avoid implying "good" or "bad" facilities.

    Args:
        citation_count: Number of total citations

    Returns:
        Shade string: 'light', 'medium', or 'dark'
    """
    if citation_count <= 5:
        return 'light'
    elif citation_count <= 15:
        return 'medium'
    else:
        return 'dark'

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/api/geocode', methods=['POST'])
def api_geocode():
    """
    Geocode a user's address.

    Request body: {"address": "123 Main St, Los Angeles, CA"}
    Response: {"success": true, "lat": 34.0522, "lon": -118.2437, "display_name": "..."}
    """
    data = request.get_json()
    address = data.get('address', '')

    if not address:
        return jsonify({'success': False, 'error': 'Address is required'}), 400

    result = geocode_address(address)

    if result:
        return jsonify({
            'success': True,
            'lat': result['lat'],
            'lon': result['lon'],
            'display_name': result['display_name']
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Could not geocode address. Please check and try again.'
        }), 400

@app.route('/api/search', methods=['POST'])
def api_search():
    """
    Search for nearby facilities.

    Request body: {"lat": 34.0522, "lon": -118.2437, "radius_miles": 10}
    Response: {"success": true, "facilities": [...]}
    """
    data = request.get_json()
    user_lat = data.get('lat')
    user_lon = data.get('lon')
    radius_miles = data.get('radius_miles', 50)  # Default 50 miles

    if user_lat is None or user_lon is None:
        return jsonify({'success': False, 'error': 'Latitude and longitude required'}), 400

    facilities = []

    # Filter to LICENSED, PENDING, and ON PROBATION facilities
    for row in facilities_data:
        # Skip closed facilities
        facility_status = row.get('Facility Status', '')
        if facility_status not in ['LICENSED', 'PENDING', 'ON PROBATION']:
            continue

        facility_num = str(row.get('Facility Number', ''))

        # Get geocoded coordinates from cache
        if facility_num not in geocode_cache:
            continue  # Skip facilities without geocoded data

        coords = geocode_cache[facility_num]
        fac_lat = coords['lat']
        fac_lon = coords['lon']

        # Calculate distance
        distance = haversine_distance(user_lat, user_lon, fac_lat, fac_lon)

        # Filter by radius
        if distance > radius_miles:
            continue

        # Count total citations
        citations_str = row.get('Citation Numbers', '').strip()
        if citations_str:
            # Split by comma and count
            citation_list = [c.strip() for c in citations_str.split(',') if c.strip()]
            total_citations = len(citation_list)
        else:
            total_citations = 0

        # Check ownership change
        ownership_change = check_ownership_change(row.get('License First Date', ''))

        # Determine shade based on total citations
        shade = get_severity_shade(total_citations)

        # Parse capacity
        try:
            capacity = int(row.get('Facility Capacity', '0'))
        except (ValueError, TypeError):
            capacity = 0

        # Build facility object
        facility = {
            'facility_number': facility_num,
            'name': row.get('Facility Name', 'Unknown'),
            'address': row.get('Facility Address', ''),
            'city': row.get('Facility City', ''),
            'state': row.get('Facility State', ''),
            'zip': row.get('Facility Zip', ''),
            'phone': row.get('Facility Telephone Number', ''),
            'capacity': capacity,
            'status': facility_status,
            'lat': fac_lat,
            'lon': fac_lon,
            'distance': round(distance, 2),
            'total_citations': total_citations,
            'ownership_change': ownership_change,
            'shade': shade
        }

        facilities.append(facility)

    # Sort by distance
    facilities.sort(key=lambda x: x['distance'])

    # Limit to top 50
    facilities = facilities[:50]

    return jsonify({
        'success': True,
        'count': len(facilities),
        'facilities': facilities
    })

if __name__ == '__main__':
    # Load data on startup
    load_data()

    # Run Flask app
    print("\nStarting RCFE Proximity Search App...")
    print("Access the app at: http://localhost:5001")
    print("Press Ctrl+C to stop\n")

    # Use debug mode only in development (not in production)
    import os
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=5001)
else:
    # When running via WSGI (PythonAnywhere, Heroku, etc.)
    load_data()

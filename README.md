# RCFE Facility Finder

A web application to find Residential Care Facilities for the Elderly (RCFE) near you, with violation data and ownership change warnings.

## Features

- 🗺️ **Interactive Map View** - See facilities on a map with colored pins
- 📋 **List View** - Browse facilities in a scrollable list
- 📍 **Proximity Search** - Find facilities near any address
- ⚠️ **Violation Tracking** - Color-coded by recent violations (last 2 years)
- 🔔 **Ownership Warnings** - Flags facilities with recent ownership changes
- 📱 **Mobile-Friendly** - Works on phones, tablets, and computers

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web server)
- pandas (data processing)
- requests (geocoding)
- playwright (for the scraper)

### Step 2: Geocode Facilities (One-Time Setup)

**Important:** This takes 3-4 hours. Run it overnight!

```bash
python geocode_facilities.py
```

What this does:
- Geocodes all 12,928 facilities using the free Nominatim service
- Saves coordinates to `geocode_cache.json`
- Shows progress every 10 facilities
- Saves checkpoints every 100 facilities (can resume if interrupted)

You only need to do this once! The geocode cache is reused for all future searches.

## Usage

### Start the App

```bash
python app.py
```

You'll see:
```
Loading facilities data...
Loaded 12928 facilities
Loading geocode cache...
Loaded 12345 geocoded facilities
App ready!

Starting RCFE Proximity Search App...
Access the app at: http://localhost:5000
```

### Use the App

1. Open your browser to **http://localhost:5000**
2. Enter an address (e.g., "123 Main St, Los Angeles, CA")
3. Click **Search**
4. View results on the map or switch to list view
5. Click markers or cards to see details

### Stop the App

Press **Ctrl+C** in the terminal

## Understanding the Results

### Violation Color-Coding

Results are color-coded based on **substantiated allegations in the last 2 years**:

- 🟢 **Green (0-2 violations)** - Low violation count
- 🟡 **Yellow (3-5 violations)** - Medium violation count
- 🔴 **Red (6+ violations)** - High violation count

### Ownership Change Warning

Facilities licensed within the last year show a 🔔 warning icon. Recent ownership changes can indicate:
- New management (may lack experience)
- Recent acquisition/restructuring
- Worth investigating further

### What's Shown

For each facility:
- **Distance** from your address (in miles)
- **Name** and address
- **Phone number**
- **Capacity** (number of residents)
- **Administrator** name
- **Recent violations** (last 2 years only)
- **Ownership change** flag (if applicable)

## Updating Data

When you download fresh data using the scraper:

```bash
# Download latest data
python rcfe_scraper.py

# Re-geocode new facilities (only geocodes facilities not in cache)
python geocode_facilities.py

# Restart the app
python app.py
```

The geocoding script will skip facilities already in the cache, so it's much faster on subsequent runs!

## File Structure

```
claude-test/
├── data/
│   ├── rcfe_data_latest.csv          # RCFE facility data
│   └── page_screenshot.png           # (from scraper)
├── templates/
│   └── index.html                    # Web interface
├── geocode_cache.json                # Geocoded coordinates (generated)
├── rcfe_scraper.py                   # Downloads fresh data weekly
├── geocode_facilities.py             # One-time geocoding setup
├── app.py                            # Flask web server
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── SETUP_INSTRUCTIONS.txt            # Scraper instructions
```

## Troubleshooting

### "geocode_cache.json not found"

You need to run `python geocode_facilities.py` first. This is the one-time setup step.

### "No facilities found"

Try:
- Entering a more specific address
- Expanding the search radius (currently 50 miles)
- Checking that you're in California (this data is California-only)

### Geocoding is slow

Yes, it takes 3-4 hours due to Nominatim's rate limit (1 request/second). This is normal. Run it overnight!

### Some facilities don't appear

Facilities without valid addresses couldn't be geocoded. The app only shows facilities with coordinates.

### App won't start

Make sure:
1. All dependencies are installed: `pip install -r requirements.txt`
2. You're in the correct directory
3. Port 5000 isn't already in use

## Technical Details

### Technologies Used

- **Backend:** Flask (Python web framework)
- **Frontend:** HTML, CSS, JavaScript
- **Map:** Leaflet.js + OpenStreetMap
- **Geocoding:** Nominatim (free OpenStreetMap service)
- **Data:** pandas for CSV processing

### How Proximity Search Works

1. User enters address
2. App geocodes address using Nominatim → gets latitude/longitude
3. Loads pre-geocoded facilities from cache
4. Calculates Haversine distance to each facility
5. Filters to LICENSED facilities within 50 miles
6. Parses violation dates, counts recent (last 2 years)
7. Checks license date for ownership changes
8. Sorts by distance, returns top 50
9. Displays on map with colored pins

### Distance Calculation

Uses the Haversine formula to calculate "as the crow flies" distance between two points on Earth. This gives straight-line distance, not driving distance.

### Violation Counting

The app parses the "All Visit Dates" column and counts substantiated allegations from the last 2 years only. Older violations are excluded as they may have been corrected.

## Privacy

- All data processing happens locally on your computer
- No data is sent to external services except:
  - Nominatim for geocoding (required)
  - OpenStreetMap for map tiles (standard)
- No user data is collected or stored

## Credits

- RCFE data from California Community Care Licensing Division (CCLD)
- Maps powered by OpenStreetMap
- Geocoding by Nominatim

## License

This is a personal tool built for finding RCFE facilities. The data is public information from the State of California.

---

**Questions or issues?** The code is self-contained and fully commented. Check the source files for implementation details.

# California Assisted Living Finder

## Overview

This application helps you search for **RCFEs (Residential Care Facilities for the Elderly)** in California, commonly known as:
- Assisted Living Facilities
- Memory Care Facilities
- Board and Care Homes
- Residential Care Homes

The app provides an interactive map-based search with facility information including licensing status, capacity, citation history, and contact details.

---

## Data Source

**Source:** California Department of Social Services - Community Care Licensing Division
**Website:** https://www.ccld.dss.ca.gov/carefacilitysearch/
**Data Last Updated:** January 2, 2026
**Dataset:** RCFE Public Facility Data

All information is public data maintained by the California Department of Social Services.

---

## Dataset Statistics

### Total Facilities in Dataset: 12,928

**By Licensing Status:**
- **LICENSED:** 8,232 facilities (63.7%)
- **CLOSED:** 3,867 facilities (29.9%)
- **PENDING:** 808 facilities (6.2%)
- **ON PROBATION:** 21 facilities (0.2%)

### Facilities Shown in This App: 9,061

This application displays **LICENSED**, **PENDING**, and **ON PROBATION** facilities only. Closed facilities are excluded.

---

## Geocoding Coverage

To display facilities on the map, addresses must be converted to geographic coordinates (latitude/longitude). This process is called "geocoding."

### Geocoding Results by Status:

**LICENSED Facilities:**
- Total: 8,232
- Successfully geocoded: 7,165 (87.0%)
- Not geocoded: 1,067 (13.0%)

**PENDING Facilities:**
- Total: 808
- Successfully geocoded: 689 (85.3%)
- Not geocoded: 119 (14.7%)

**ON PROBATION Facilities:**
- Total: 21
- Successfully geocoded: 20 (95.2%)
- Not geocoded: 1 (4.8%)

### Total Searchable Facilities: 7,874 (86.9% of active facilities)

**Why Some Facilities Couldn't Be Geocoded:**
- Incomplete or invalid addresses
- Missing street numbers
- Typographical errors in addresses
- Rural addresses not in geocoding database
- Very new addresses not yet mapped

---

## Facilities Not Included

**1,187 active facilities** (LICENSED, PENDING, or ON PROBATION) could not be geocoded and are **not shown on the map**.

For a complete list of facilities that are not included, see: [Facilities Not Geocoded](not_geocoded.txt)

**Breakdown:**
- LICENSED not geocoded: 1,067 facilities
- PENDING not geocoded: 119 facilities
- ON PROBATION not geocoded: 1 facility

---

## Search Features

### Interactive Map
- View facilities on an interactive map
- Color-coded by citation count (neutral blue shading)
- Pan and zoom to explore different areas
- Click markers for facility details

### Dynamic Search
- Enter your address to find nearby facilities
- Searches within a 50-mile radius from your location
- Returns up to 50 closest facilities
- Results sorted by distance from your location
- Move the map to automatically search new areas

### Filters
- **Facility Name:** Search by facility name
- **Facility Size:** Filter by capacity (1-6, 7-49, 50+ residents)

### Facility Information
- Licensing status (LICENSED, PENDING, ON PROBATION)
- Phone number (clickable to call)
- Facility capacity
- Total citation count
- Recent ownership change indicator
- Direct link to full details on DSS website

---

## Citation Information

**What Citations Represent:**
Citations are regulatory violations issued by the California Department of Social Services. The total citation count includes all historical citations from the "Citation Numbers" field in the state database.

**Important Notes:**
- Citation counts are displayed with neutral blue shading (not "good" or "bad")
- Light shade: 0-5 citations
- Medium shade: 6-15 citations
- Dark shade: 16+ citations
- Citation count is informational only; review full facility details on the DSS website

**For Complete Facility Information:**
Click "View Full Details on DSS Website" to see:
- Detailed inspection reports
- Specific violation descriptions
- Correction plans
- Visit history
- Additional facility information

---

## Ownership Change Indicator

Facilities licensed within the past year are flagged with 🔔 "Recent ownership change."

**Why This Matters:**
- New ownership may mean different management
- Different policies and procedures
- New staff and operational changes
- Review recent inspection reports for current performance

---

## Data Dictionary

For detailed information about all data fields used in this application, see: [Data Dictionary](DATA_DICTIONARY.md)

The data dictionary includes:
- Field definitions and examples
- Data formats and ranges
- How each field is used in the app
- Important notes about data quality

---

## Technical Information

**Geocoding Service:** OpenStreetMap Nominatim
**Distance Calculation:** Haversine formula (great circle distance)
**Map Provider:** OpenStreetMap
**Search Radius:** 50 miles from your location
**Update Frequency:** Data updated from DSS as available

**Accessibility:**
This application is designed to meet WCAG 2.1 AA accessibility standards, including:
- Keyboard navigation
- Screen reader support
- Proper ARIA labels
- High contrast color schemes
- Skip links for navigation

---

## Privacy & Data Usage

- No personal information is collected
- Address searches are processed locally (not stored)
- All facility data is public information from the California Department of Social Services
- Map tiles provided by OpenStreetMap

---

## Questions or Issues?

For questions about specific facilities or licensing issues, contact:

**California Department of Social Services**
Community Care Licensing Division
Website: https://www.ccld.dss.ca.gov/
Phone: (844) 538-8766

For questions about this application or to report data issues, please note that this is an independent tool using public DSS data.

---

## Version Information

**Application:** California Assisted Living Finder
**Data Version:** January 2, 2026
**Facilities in Database:** 12,928
**Searchable Facilities:** 7,874
**Coverage:** 86.9% of active facilities

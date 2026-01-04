# California Assisted Living Finder - Data Dictionary

## Data Source
**Source:** California Department of Social Services - Community Care Licensing Division
**Website:** https://www.ccld.dss.ca.gov/carefacilitysearch/
**Last Updated:** January 2026
**Dataset:** RCFE (Residential Care Facilities for the Elderly) Public Data

---

## About the Data

This application displays information about **RCFEs (Residential Care Facilities for the Elderly)**, which are commonly known as:
- Assisted Living Facilities
- Memory Care Facilities
- Board and Care Homes
- Residential Care Homes

All data is sourced from the California Department of Social Services and is updated regularly from their public facility database.

---

## Fields Included in Search Results

### Facility Number
**What it is:** Unique 9-digit state-issued identifier
**Example:** "191800001"
**Use:** Links to detailed facility information on DSS website

### Facility Name
**What it is:** Official registered name of the facility
**Example:** "HOLLENBECK PALMS"
**Use:** Primary identifier in search results

### Facility Status
**What it is:** Current licensing status
**Possible Values:**
- **LICENSED** - Active and legally operating
- **PENDING** - License application in process
- **ON PROBATION** - License under review/restrictions
- **CLOSED** - No longer operating (not shown in results)

**Note:** This app shows LICENSED, PENDING, and ON PROBATION facilities only.

### Address (Street, City, State, ZIP)
**What it is:** Physical location of the facility
**Use:** Geocoded for map display and distance calculations

### Facility Telephone Number
**What it is:** Main contact phone number
**Format:** (XXX) XXX-XXXX
**Use:** Direct contact link in results

### Facility Capacity
**What it is:** Maximum number of residents allowed by license
**Range:**
- **1-6 residents** - Small residential homes
- **7-49 residents** - Medium facilities
- **50+ residents** - Large facilities

**Important:** Facilities with 6 or fewer residents have different licensing requirements than larger facilities.

### License First Date
**What it is:** Date the current license was first issued
**Format:** M/D/YYYY
**Important:** This date changes when ownership changes
**Use:** Facilities licensed within the last year are flagged as "Recent ownership change"

### Citation Numbers
**What it is:** Comma-separated list of California regulation codes that were violated
**Example:** "87303(e)(2), 87555(b)(7), 87468.1(a)(1)"
**Format:** California Code of Regulations Title 22 citations
**Use:** Total count of citations is displayed; indicates regulatory compliance history

### Total Citations
**What it is:** Count of all regulatory citations issued to the facility
**Calculation:** Number of citation codes in the Citation Numbers field
**Display:** Shown with neutral blue shading:
- **Light shade (0-5 citations)** - Fewer citations
- **Medium shade (6-15 citations)** - Moderate citations
- **Dark shade (16+ citations)** - More citations

**Important:** Citation count is informational only and does not indicate "good" or "bad" facilities. Review full facility details on the DSS website.

### Recent Ownership Change
**What it is:** Indicator if facility was licensed within the past year
**Calculation:** License First Date is within last 365 days
**Display:** Warning flag (🔔) in results
**Why it matters:** New ownership may mean different management, policies, or operational changes

---

## Distance Calculation

**Method:** Haversine formula (great circle distance)
**Units:** Miles
**Radius:** Search results show facilities within 50 miles of your location
**Sorting:** Results are sorted by distance (nearest first)

---

## Data Notes

- All data is public information maintained by the California Department of Social Services
- Facilities must be geocoded (address converted to coordinates) to appear on the map
- Only facilities with valid addresses that can be geocoded are shown
- Citation counts represent historical compliance issues; review full details on DSS website
- For complete facility information including inspection reports, visit the DSS facility detail page

---

## For More Information

**California Department of Social Services**
Community Care Licensing Division
Website: https://www.ccld.dss.ca.gov/

**Facility Search Tool:**
https://www.ccld.dss.ca.gov/carefacilitysearch/

**RCFE Regulations:**
California Code of Regulations, Title 22, Division 6, Chapter 8

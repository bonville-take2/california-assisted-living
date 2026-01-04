# RCFE Data Dictionary - Complete Column Breakdown

## Overview
This document explains all 38 columns in the RCFE (Residential Care Facilities for the Elderly) dataset from California's Community Care Licensing Division.

---

## FACILITY IDENTIFICATION & CONTACT (Columns 1-13)

### 1. Facility Type
**What it is:** The classification of the facility
**Example:** "RCFE-CONTINUING CARE RETIREMENT COMMUNITY"
**Common values:** RCFE, RCFE-ADULT DAY PROGRAM, RCFE-CONTINUING CARE RETIREMENT COMMUNITY
**Use in app:** Filter to show only specific facility types

### 2. Facility Number
**What it is:** Unique state-issued identifier for the facility
**Example:** "216801686"
**Format:** 9-digit number
**Use in app:** Primary key for linking data (geocode cache, searches)

### 3. Facility Name
**What it is:** Official registered name of the facility
**Example:** "ALDERSLY"
**Use in app:** Display name in search results

### 4. Licensee
**What it is:** Legal entity/person who holds the license
**Example:** "ALDERSLY/LIFE CARE SERVICES,LLC"
**Notes:** May be individual, corporation, or LLC
**Use in app:** Shows ownership/corporate entity

### 5. Facility Administrator
**What it is:** Name of person managing day-to-day operations
**Example:** "MIKE SHARKEY"
**Use in app:** Contact person for facility inquiries

### 6. Facility Telephone Number
**What it is:** Main phone number
**Example:** "(415) 453-7425"
**Use in app:** Clickable link to call on mobile devices

### 7-10. Address Fields
- **Facility Address:** Street address
- **Facility City:** City name
- **Facility State:** Always "CA" (California)
- **Facility Zip:** ZIP code
**Use in app:** Geocoding, display location

### 11. County Name
**What it is:** California county where facility is located
**Example:** "MARIN"
**Use in app:** Could filter/group by county

### 12. Regional Office
**What it is:** State licensing office number that oversees this facility
**Example:** "21"
**Notes:** California has multiple regional licensing offices
**Use in app:** Not typically shown to users

### 13. Facility Capacity
**What it is:** Maximum number of residents allowed by license
**Example:** "172"
**Range:** Can be 1-6 (small homes) to 500+ (large facilities)
**Use in app:** Important metric - shows facility size

---

## LICENSING STATUS (Columns 14-16)

### 14. Facility Status
**What it is:** Current licensing status
**Example:** "LICENSED"
**Common values:**
- LICENSED = Active, operating legally
- CLOSED = No longer operating
- SUSPENDED = License temporarily revoked
- PENDING = Application in process
**Use in app:** **CRITICAL** - Only show LICENSED facilities

### 15. License First Date
**What it is:** Date the current license was first issued
**Example:** "11/5/2004"
**Format:** M/D/YYYY
**Important:** Changes when facility sold/ownership changes
**Use in app:** Detect ownership changes (if < 1 year ago = recent change)

### 16. Closed Date
**What it is:** Date facility closed (if applicable)
**Example:** Usually blank for active facilities
**Use in app:** Should be blank for LICENSED facilities

---

## VISIT HISTORY (Columns 17-28)

### 17. Last Visit Date
**What it is:** Most recent inspection/visit by state
**Example:** "11/6/2025"
**Use in app:** Shows how recently facility was inspected

### 18-21. Visit Counts
- **Inspection Visits:** Routine scheduled inspections
- **Complaint Visits:** Visits triggered by complaints
- **Other Visits:** Follow-ups, POC verifications, etc.
- **Total Visits:** Sum of all visits
**Example:** 5 inspections, 12 complaints, 15 other = 32 total
**Use in app:** High complaint visits = red flag

### 22. Citation Numbers
**What it is:** List of regulation codes that were violated
**Example:** "87555(b)(7), 87411(a), 87468.2(a)(4)..."
**Format:** California Code of Regulations Title 22 citations
**Use in app:** Could link to regulation details (advanced feature)

### 23. POC Dates
**What it is:** "Plan of Correction" dates - when facility submitted fix plans
**Example:** "04/22/2023, 12/30/2022, 10/04/2025..."
**Use in app:** Not typically shown to end users

### 24. All Visit Dates
**What it is:** **CRITICAL** - Comma-separated list of ALL visit dates
**Example:** "10/21/2025, 10/03/2025, 08/20/2025, 07/01/2025..."
**Format:** MM/DD/YYYY, comma-separated
**Use in app:** **We use this to count recent violations** (last 2 years)

### 25. Inspection Visit Dates
**What it is:** Subset of All Visit Dates - only scheduled inspections
**Example:** "10/03/2025, 10/15/2024, 09/26/2023..."
**Use in app:** Could show inspection frequency

### 26-27. Inspect TypeA / TypeB
**What it is:** Count of Type A/B violations found during inspections
**Example:** 0 Type A, 0 Type B
**Notes:** Often 0 because most violations come from complaints
**Use in app:** Shows inspection violations specifically

### 28. Other Visit Dates
**What it is:** Dates of follow-up visits, POC verifications
**Example:** "10/21/2025, 08/20/2025, 01/15/2025..."
**Use in app:** Less important than complaint visits

### 29-30. Other TypeA / TypeB
**What it is:** Count of Type A/B violations from "Other" visits
**Example:** 6 Type A, 4 Type B
**Use in app:** Part of total violation picture

### 31-32. Complaint Type A / Complaint Type B
**What it is:** **IMPORTANT** - Number of Type A vs Type B complaint visits
**Example:** 2 Type A complaints, 0 Type B complaints
**What's the difference:**
- **Type A:** Serious violations affecting health/safety (e.g., medication errors, abuse, unsafe conditions)
- **Type B:** Less serious administrative/procedural violations (e.g., paperwork, licensing posting)
**Use in app:** Could differentiate serious vs minor issues

---

## ALLEGATIONS SUMMARY (Columns 33-37)

### Understanding Allegations
When someone files a complaint, the state investigates and each allegation is classified:

### 33. Total Allegations
**What it is:** Total number of allegations investigated (all outcomes)
**Example:** 26
**Use in app:** Shows how many complaints were filed

### 34. Inconclusive Allegations
**What it is:** Couldn't be proven or disproven
**Example:** 0
**Use in app:** Not actionable data

### 35. Substantiated Allegations ⭐ **MOST IMPORTANT**
**What it is:** Allegations that were **PROVEN TRUE** by investigators
**Example:** 3
**This is the key metric:** These are confirmed violations
**Use in app:** **This is what we're currently counting** - proven violations

### 36. Unsubstantiated Allegations
**What it is:** Allegations that were investigated but NOT proven
**Example:** 21
**Notes:** Complaint was made but evidence didn't support it
**Use in app:** Shows facility was accused but not guilty

### 37. Unfounded Allegations
**What it is:** Allegations that were completely baseless
**Example:** 2
**Use in app:** Shows some complaints were false

---

## DETAILED COMPLAINT BREAKDOWN (Column 38)

### 38. Complaint Info- Date, #Sub A, # Inc A, # Uns A, # Unf A, # TypeA, # TypeB ...
**What it is:** Complex comma-separated field with detailed breakdown of each complaint visit
**Format:** Appears to contain dates and allegation counts per visit
**Example:** "07/09/2025" (truncated in our sample)
**Notes:** This field has inconsistent formatting and is difficult to parse
**Use in app:** Not currently used - data is aggregated in other columns

---

## KEY METRICS FOR VIOLATION TRACKING

### What We're Currently Using:
1. **All Visit Dates (Column 24)** - To determine which violations are recent (last 2 years)
2. **Substantiated Allegations (Column 35)** - Total proven violations (all time)
3. **Our Calculation:**
   - Count how many visits occurred in last 2 years
   - Prorate: `recent_violations = total_substantiated × (recent_visits / total_visits)`

### What This Means:
- **Substantiated Allegations includes BOTH Type A and Type B violations**
- We're showing ALL proven violations, not just serious (Type A) ones
- The count is prorated based on visit dates to estimate recent violations

### Type A vs Type B Breakdown:
- **Complaint Type A (Column 31):** Number of Type A **complaint visits**
- **Complaint Type B (Column 32):** Number of Type B **complaint visits**
- These count VISITS, not individual allegations
- A single complaint visit can have multiple allegations

---

## RECOMMENDATIONS

### Currently Missing from App:
1. **Facility Capacity** - Should display (shows size)
2. **Last Visit Date** - Shows inspection recency
3. **Total Visits / Complaint Visits** - Shows scrutiny level
4. **Type A vs Type B distinction** - Could separate serious from minor violations

### Possible Enhancements:
1. Show "Serious (Type A) violations: X" separately from "Administrative (Type B) violations: Y"
2. Display "Last inspected: MM/DD/YYYY"
3. Show "Under complaint investigation" if recent complaint visits
4. Flag facilities with high complaint-to-inspection ratio

### Data Quality Notes:
- Column 38 (Complaint Info) appears truncated or malformed in many rows
- Some facilities may have missing/incomplete data
- Dates are in M/D/YYYY format (not zero-padded)
- The relationship between visit counts and allegations is complex - multiple allegations can occur in one visit

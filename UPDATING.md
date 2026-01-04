# Automatic Data Updates

## Overview

The California Assisted Living Finder includes an automatic update system that:
1. Downloads the latest data from the DSS website
2. Detects all types of changes (new facilities, ownership changes, new citations, etc.)
3. Only geocodes NEW facilities or facilities with changed addresses (saves hours!)
4. Updates all documentation and statistics
5. Creates detailed change logs

## How It Works

### Fully Automated Updates

The update system is **completely automated** - it handles everything from download to live website update:

1. ✅ Downloads latest data from DSS
2. ✅ Detects all changes
3. ✅ Geocodes only new/changed addresses
4. ✅ Updates documentation
5. ✅ **Automatically restarts Flask app with new data**
6. ✅ Website immediately shows updated data

**No manual intervention required!**

### Smart Change Detection

The update system detects **ALL** types of changes:

**🆕 New Facilities**
- Newly licensed facilities

**📍 Address Changes** (require re-geocoding)
- Facility moved to new location
- Address corrections

**👤 Ownership Changes**
- License First Date changed
- New management/ownership

**⚠️ Citation Changes**
- New regulatory citations added
- Shows count increase

**📋 Status Changes**
- PENDING → LICENSED
- LICENSED → ON PROBATION
- LICENSED → CLOSED
- etc.

**👥 Capacity Changes**
- Maximum resident capacity increased/decreased

**🗑️ Removed Facilities**
- Facilities no longer in dataset

### Efficient Geocoding

**Key Optimization:** Only geocodes facilities that actually need it!

- **New facilities**: Must be geocoded
- **Address changes**: Must be re-geocoded
- **Other changes**: Already have coordinates - no geocoding needed!

**Time Savings:**
- Full geocoding: ~3-4 hours for all 12,928 facilities
- Incremental update: Usually 5-30 minutes (only new/changed addresses)

---

## Manual Update (Recommended First Time)

Run a manual update to see what changed:

```bash
cd /Users/anneneville-bonilla/Documents/claude-test
python3 update_data.py
```

**What happens:**
1. Downloads latest data from DSS (2-3 minutes)
2. Compares with previous data
3. Shows detailed change summary
4. Geocodes only new/changed facilities
5. Updates README and statistics
6. Creates backup of current data

**Example Output:**
```
======================================================================
  STEP 2: Analyzing Data Changes
======================================================================

Current dataset: 12,928 facilities
Previous dataset: 12,900 facilities

📊 Changes Detected:

🆕 New Facilities: 35
📍 Address Changes: 8 (require re-geocoding)
👤 Ownership Changes: 142
⚠️  Citation Changes: 67
📋 Status Changes: 12
👥 Capacity Changes: 5
🗑️  Removed: 7

🗺️  Total to geocode: 43

👤 Sample Ownership Changes:
   SUNRISE SENIOR LIVING: 5/20/2020 → 1/15/2026
   GOLDEN YEARS RESIDENCE: 3/10/2019 → 1/2/2026
   ... and 140 more

⚠️  Sample Citation Changes:
   SUNSET MANOR: 12 → 15 (+3)
   VALLEY VIEW CARE: 3 → 8 (+5)
   ... and 65 more
```

---

## Automatic Updates (Scheduled)

### Setup Automatic Weekly Updates

1. **Test the update script first** (see Manual Update above)

2. **Create cron job** to run every Sunday at 2 AM:

```bash
crontab -e
```

Add this line:
```
0 2 * * 0 /Users/anneneville-bonilla/Documents/claude-test/schedule_updates.sh
```

**Cron schedule explained:**
- `0 2 * * 0` = 2:00 AM every Sunday
- Alternative schedules:
  - `0 2 1 * *` = 2 AM on 1st of each month
  - `0 2 * * 1` = 2 AM every Monday
  - `0 2 15 * *` = 2 AM on 15th of each month

3. **Verify cron job is installed:**

```bash
crontab -l
```

### Setup Automatic Monthly Updates

For monthly updates on the 1st at 3 AM:

```bash
crontab -e
```

Add:
```
0 3 1 * * /Users/anneneville-bonilla/Documents/claude-test/schedule_updates.sh
```

---

## Logs

All updates are logged with timestamps.

**Log location:** `/Users/anneneville-bonilla/Documents/claude-test/logs/`

**View latest log:**
```bash
cd /Users/anneneville-bonilla/Documents/claude-test/logs
ls -lt | head -5
cat update_YYYYMMDD_HHMMSS.log
```

**Logs are automatically cleaned up** - only last 30 days are kept.

---

## Automatic Flask Restart

The update script **automatically restarts the Flask app** after updating data!

**What happens:**
1. Script detects running Flask app
2. Gracefully stops Flask (SIGTERM)
3. Updates data and geocode cache
4. Starts Flask app with new data
5. Website immediately shows updated data

**If Flask was not running:**
- Script will start it automatically after update

**Manual restart (if needed):**
If automatic restart fails, you can manually restart:
```bash
python3 app.py
```

**Production environments:**
For systemd/supervisor deployments, you may want to customize the restart logic in `update_data.py`

---

## What Gets Updated

✅ **CSV Data** (`data/rcfe_data_latest.csv`)
- Complete fresh download from DSS

✅ **Geocode Cache** (`geocode_cache.json`)
- New facilities geocoded
- Changed addresses re-geocoded
- Removed facilities deleted from cache

✅ **README** (`static/README.md`)
- Updated statistics
- New date stamp
- Geocoding coverage percentages

✅ **Backup** (`data/rcfe_data_previous.csv`)
- Previous dataset saved for comparison

✅ **Change Logs** (`logs/update_*.log`)
- Detailed list of all changes
- Geocoding results
- Timestamps

---

## Troubleshooting

### Update Failed - Scraper Error

**Problem:** Website changed or is down

**Solution:**
1. Check if DSS website is accessible: https://www.ccld.dss.ca.gov/carefacilitysearch/
2. Check log file for specific error
3. May need to update `rcfe_scraper.py` if website structure changed

### Update Failed - Geocoding Error

**Problem:** Too many requests or API issue

**Solution:**
1. Wait 1 hour and try again
2. Check internet connection
3. Nominatim may have rate limit issues

### Cron Job Not Running

**Problem:** Scheduled update didn't run

**Solution:**
1. Check cron logs: `grep CRON /var/log/syslog`
2. Verify path is correct in crontab
3. Make sure script is executable: `chmod +x schedule_updates.sh`
4. Test script manually first

### Flask App Not Showing New Data

**Problem:** Updated data but app shows old data

**Solution:**
1. Check update logs - Flask should have restarted automatically
2. If automatic restart failed, manually restart: `python3 app.py`
3. Clear browser cache
4. Check that `data/rcfe_data_latest.csv` has new modified date

### Flask Restart Failed

**Problem:** Update script couldn't restart Flask

**Solution:**
1. Check Flask logs in `logs/flask_*.log`
2. Manually stop any Flask processes: `pkill -f app.py`
3. Manually start Flask: `python3 app.py`
4. Check for port conflicts (port 5001)

---

## Change Notifications

To get notified of updates, you can:

1. **Check log files** after scheduled run
2. **Add email notifications** to `schedule_updates.sh`:

```bash
# Add to schedule_updates.sh after the update runs:
if [ $? -eq 0 ]; then
    echo "Update completed successfully" | mail -s "RCFE Data Updated" your@email.com
fi
```

3. **Monitor log directory** for new files:

```bash
watch -n 3600 "ls -lt logs/ | head -5"
```

---

## Best Practices

1. **Run manual update first** to verify everything works
2. **Check logs weekly** even if automated
3. **Keep backups** of `geocode_cache.json` periodically
4. **Monitor DSS website** for structure changes that might break scraper
5. **Update documentation** if you find issues

---

## Update Frequency Recommendations

**Weekly updates** (Recommended):
- Catches new facilities quickly
- Shows recent citation changes
- Minimal geocoding time

**Monthly updates**:
- Less frequent maintenance
- Larger change sets
- Longer geocoding time

**Manual/on-demand updates**:
- When you know changes occurred
- Before important demos
- After DSS announces major data updates

---

## Performance

**Typical update times:**

| Scenario | Time | Geocoding |
|----------|------|-----------|
| No changes | 3-5 min | 0 facilities |
| 10 new facilities | 15-20 min | 10 facilities |
| 50 new facilities | 60-75 min | 50 facilities |
| 100 new + changed | 120-150 min | 100 facilities |
| First run (all) | 3-4 hours | ~12,000 facilities |

**Note:** Geocoding is 1 request/second due to Nominatim rate limit.

---

## Questions?

For issues with:
- **Data from DSS:** Contact California Department of Social Services
- **Update script:** Review logs and verify DSS website hasn't changed
- **Geocoding:** Check Nominatim service status

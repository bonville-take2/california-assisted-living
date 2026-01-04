"""
Automated RCFE Data Update Script
Updates facility data, geocodes new/changed facilities, and regenerates documentation.

Usage: python update_data.py
"""

import csv
import json
import subprocess
import sys
import time
import signal
import psutil
from datetime import datetime
from pathlib import Path

# File paths
DATA_DIR = Path('data')
CACHE_FILE = Path('geocode_cache.json')
README_FILE = Path('static/README.md')
CURRENT_CSV = DATA_DIR / 'rcfe_data_latest.csv'
PREVIOUS_CSV = DATA_DIR / 'rcfe_data_previous.csv'

def print_header(message):
    """Print a formatted header."""
    print('\n' + '=' * 70)
    print(f'  {message}')
    print('=' * 70 + '\n')

def run_scraper():
    """Run the web scraper to download latest data."""
    print_header('STEP 1: Downloading Latest Data from DSS Website')

    try:
        # Check if scraper exists
        if not Path('rcfe_scraper.py').exists():
            print('❌ Error: rcfe_scraper.py not found!')
            return False

        # Run the scraper
        print('Running web scraper...')
        result = subprocess.run(
            ['python3', 'rcfe_scraper.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            print('✅ Successfully downloaded latest data')
            return True
        else:
            print(f'❌ Scraper failed with error:\n{result.stderr}')
            return False

    except subprocess.TimeoutExpired:
        print('❌ Scraper timed out after 5 minutes')
        return False
    except Exception as e:
        print(f'❌ Error running scraper: {e}')
        return False

def compare_data():
    """Compare current and previous data to find changes."""
    print_header('STEP 2: Analyzing Data Changes')

    if not CURRENT_CSV.exists():
        print('❌ Error: Current data file not found!')
        return None

    # Load current data
    with open(CURRENT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        current_data = {row['Facility Number']: row for row in reader}

    print(f'Current dataset: {len(current_data):,} facilities')

    # Load previous data if it exists
    if PREVIOUS_CSV.exists():
        with open(PREVIOUS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            previous_data = {row['Facility Number']: row for row in reader}
        print(f'Previous dataset: {len(previous_data):,} facilities')
    else:
        print('No previous data found - treating all facilities as new')
        previous_data = {}

    # Track all types of changes
    new_facilities = []
    address_changes = []  # Require re-geocoding
    ownership_changes = []
    citation_changes = []
    status_changes = []
    capacity_changes = []
    other_changes = []

    for fac_num, fac_data in current_data.items():
        if fac_num not in previous_data:
            # New facility
            new_facilities.append(fac_num)
        else:
            prev = previous_data[fac_num]

            # Check address changes (require re-geocoding)
            prev_address = (
                prev.get('Facility Address', '') +
                prev.get('Facility City', '') +
                prev.get('Facility Zip', '')
            )
            curr_address = (
                fac_data.get('Facility Address', '') +
                fac_data.get('Facility City', '') +
                fac_data.get('Facility Zip', '')
            )

            if prev_address != curr_address:
                address_changes.append({
                    'number': fac_num,
                    'name': fac_data.get('Facility Name', 'Unknown'),
                    'old_address': prev.get('Facility Address', ''),
                    'new_address': fac_data.get('Facility Address', '')
                })

            # Check ownership changes (License First Date)
            if prev.get('License First Date') != fac_data.get('License First Date'):
                ownership_changes.append({
                    'number': fac_num,
                    'name': fac_data.get('Facility Name', 'Unknown'),
                    'old_date': prev.get('License First Date', 'N/A'),
                    'new_date': fac_data.get('License First Date', 'N/A')
                })

            # Check citation changes
            if prev.get('Citation Numbers') != fac_data.get('Citation Numbers'):
                prev_count = len([c.strip() for c in prev.get('Citation Numbers', '').split(',') if c.strip()])
                curr_count = len([c.strip() for c in fac_data.get('Citation Numbers', '').split(',') if c.strip()])
                citation_changes.append({
                    'number': fac_num,
                    'name': fac_data.get('Facility Name', 'Unknown'),
                    'old_count': prev_count,
                    'new_count': curr_count,
                    'change': curr_count - prev_count
                })

            # Check status changes
            if prev.get('Facility Status') != fac_data.get('Facility Status'):
                status_changes.append({
                    'number': fac_num,
                    'name': fac_data.get('Facility Name', 'Unknown'),
                    'old_status': prev.get('Facility Status', 'N/A'),
                    'new_status': fac_data.get('Facility Status', 'N/A')
                })

            # Check capacity changes
            if prev.get('Facility Capacity') != fac_data.get('Facility Capacity'):
                capacity_changes.append({
                    'number': fac_num,
                    'name': fac_data.get('Facility Name', 'Unknown'),
                    'old_capacity': prev.get('Facility Capacity', 'N/A'),
                    'new_capacity': fac_data.get('Facility Capacity', 'N/A')
                })

    # Find removed facilities
    removed_facilities = set(previous_data.keys()) - set(current_data.keys())

    # Print summary
    print(f'\n📊 Changes Detected:')
    print(f'\n🆕 New Facilities: {len(new_facilities):,}')
    print(f'📍 Address Changes: {len(address_changes):,} (require re-geocoding)')
    print(f'👤 Ownership Changes: {len(ownership_changes):,}')
    print(f'⚠️  Citation Changes: {len(citation_changes):,}')
    print(f'📋 Status Changes: {len(status_changes):,}')
    print(f'👥 Capacity Changes: {len(capacity_changes):,}')
    print(f'🗑️  Removed: {len(removed_facilities):,}')
    print(f'\n🗺️  Total to geocode: {len(new_facilities) + len(address_changes):,}')

    # Show examples of important changes
    if ownership_changes:
        print(f'\n👤 Sample Ownership Changes:')
        for change in ownership_changes[:5]:
            print(f'   {change["name"]}: {change["old_date"]} → {change["new_date"]}')
        if len(ownership_changes) > 5:
            print(f'   ... and {len(ownership_changes) - 5} more')

    if citation_changes:
        print(f'\n⚠️  Sample Citation Changes:')
        for change in citation_changes[:5]:
            if change['change'] > 0:
                print(f'   {change["name"]}: {change["old_count"]} → {change["new_count"]} (+{change["change"]})')
        if len(citation_changes) > 5:
            print(f'   ... and {len(citation_changes) - 5} more')

    if status_changes:
        print(f'\n📋 Status Changes:')
        for change in status_changes[:10]:
            print(f'   {change["name"]}: {change["old_status"]} → {change["new_status"]}')

    return {
        'current_data': current_data,
        'new_facilities': new_facilities,
        'changed_facilities': [c['number'] for c in address_changes],
        'removed_facilities': removed_facilities,
        'ownership_changes': ownership_changes,
        'citation_changes': citation_changes,
        'status_changes': status_changes,
        'capacity_changes': capacity_changes
    }

def update_geocode_cache(changes):
    """Update geocode cache with new/changed facilities."""
    print_header('STEP 3: Updating Geocode Cache')

    to_geocode = set(changes['new_facilities'] + changes['changed_facilities'])

    if len(to_geocode) == 0:
        print('✅ No new facilities to geocode - cache is up to date!')
        return True

    print(f'Need to geocode {len(to_geocode):,} facilities...')
    print('This will take approximately {:.1f} minutes'.format(len(to_geocode) / 60))

    # Create a temporary file with only facilities that need geocoding
    temp_csv = Path('data/temp_to_geocode.csv')

    with open(CURRENT_CSV, 'r', encoding='utf-8') as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames

        with open(temp_csv, 'w', encoding='utf-8', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                if row['Facility Number'] in to_geocode:
                    writer.writerow(row)

    print(f'Created temporary file with {len(to_geocode):,} facilities')
    print('Starting geocoding (this may take a while)...\n')

    # Run geocoding on just the new/changed facilities
    try:
        # Modify geocode_facilities.py to accept a custom CSV path
        # For now, we'll run it on the full dataset but it will skip cached ones
        result = subprocess.run(
            ['python3', 'geocode_facilities.py'],
            capture_output=True,
            text=True,
            timeout=7200  # 2 hour timeout
        )

        # Clean up temp file
        if temp_csv.exists():
            temp_csv.unlink()

        if result.returncode == 0:
            print('\n✅ Geocoding completed successfully')
            return True
        else:
            print(f'\n❌ Geocoding failed:\n{result.stderr}')
            return False

    except subprocess.TimeoutExpired:
        print('\n❌ Geocoding timed out after 2 hours')
        return False
    except Exception as e:
        print(f'\n❌ Error during geocoding: {e}')
        return False

def remove_old_facilities(changes):
    """Remove facilities from cache that no longer exist."""
    print_header('STEP 4: Cleaning Up Removed Facilities')

    removed = changes['removed_facilities']

    if len(removed) == 0:
        print('✅ No facilities to remove from cache')
        return

    print(f'Removing {len(removed):,} facilities from geocode cache...')

    # Load cache
    with open(CACHE_FILE, 'r') as f:
        cache = json.load(f)

    # Remove old facilities
    removed_count = 0
    for fac_num in removed:
        if fac_num in cache:
            del cache[fac_num]
            removed_count += 1

    # Save updated cache
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

    print(f'✅ Removed {removed_count:,} facilities from cache')

def generate_statistics():
    """Generate statistics for README."""
    print_header('STEP 5: Generating Statistics')

    # Load current data
    with open(CURRENT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        facilities = list(reader)

    # Load geocode cache
    with open(CACHE_FILE, 'r') as f:
        cache = json.load(f)

    # Calculate statistics
    total = len(facilities)
    licensed = sum(1 for f in facilities if f.get('Facility Status') == 'LICENSED')
    pending = sum(1 for f in facilities if f.get('Facility Status') == 'PENDING')
    probation = sum(1 for f in facilities if f.get('Facility Status') == 'ON PROBATION')
    closed = sum(1 for f in facilities if f.get('Facility Status') == 'CLOSED')

    active = [f for f in facilities if f.get('Facility Status') in ['LICENSED', 'PENDING', 'ON PROBATION']]

    licensed_geocoded = sum(1 for f in facilities if f.get('Facility Status') == 'LICENSED' and f.get('Facility Number') in cache)
    pending_geocoded = sum(1 for f in facilities if f.get('Facility Status') == 'PENDING' and f.get('Facility Number') in cache)
    probation_geocoded = sum(1 for f in facilities if f.get('Facility Status') == 'ON PROBATION' and f.get('Facility Number') in cache)

    total_geocoded = licensed_geocoded + pending_geocoded + probation_geocoded

    stats = {
        'total': total,
        'licensed': licensed,
        'pending': pending,
        'probation': probation,
        'closed': closed,
        'active_total': len(active),
        'licensed_geocoded': licensed_geocoded,
        'pending_geocoded': pending_geocoded,
        'probation_geocoded': probation_geocoded,
        'total_geocoded': total_geocoded,
        'date': datetime.now().strftime('%B %d, %Y')
    }

    print(f'📊 Statistics:')
    print(f'   Total facilities: {total:,}')
    print(f'   Active facilities: {len(active):,}')
    print(f'   Successfully geocoded: {total_geocoded:,}')
    print(f'   Coverage: {total_geocoded/len(active)*100:.1f}%')

    return stats

def update_readme(stats):
    """Update README with new statistics and date."""
    print_header('STEP 6: Updating README')

    print(f'Updating README with data from {stats["date"]}...')

    # Read current README
    with open(README_FILE, 'r') as f:
        readme = f.read()

    # Update statistics - this is a simplified version
    # You may want to regenerate the entire README instead
    readme = readme.replace('January 2, 2026', stats['date'])

    # Save updated README
    with open(README_FILE, 'w') as f:
        f.write(readme)

    print('✅ README updated')

def backup_current_data():
    """Backup current data as previous data."""
    print_header('STEP 7: Creating Backup')

    if CURRENT_CSV.exists():
        # Copy current to previous
        with open(CURRENT_CSV, 'r') as f_in:
            with open(PREVIOUS_CSV, 'w') as f_out:
                f_out.write(f_in.read())
        print('✅ Current data backed up as previous data')
    else:
        print('⚠️  No current data to backup')

def find_flask_process():
    """Find the running Flask app process."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'app.py' in ' '.join(cmdline):
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def stop_flask():
    """Stop the running Flask app."""
    print_header('STEP 8: Stopping Flask App')

    flask_proc = find_flask_process()

    if not flask_proc:
        print('⚠️  Flask app is not running')
        return None

    print(f'Found Flask app (PID: {flask_proc.pid})')
    print('Stopping Flask app gracefully...')

    try:
        # Try graceful shutdown first (SIGTERM)
        flask_proc.send_signal(signal.SIGTERM)

        # Wait up to 10 seconds for graceful shutdown
        for i in range(10):
            if not flask_proc.is_running():
                print('✅ Flask app stopped gracefully')
                return True
            time.sleep(1)

        # If still running, force kill (SIGKILL)
        print('Graceful shutdown timed out, forcing stop...')
        flask_proc.send_signal(signal.SIGKILL)
        time.sleep(2)

        if not flask_proc.is_running():
            print('✅ Flask app stopped (forced)')
            return True
        else:
            print('❌ Could not stop Flask app')
            return False

    except Exception as e:
        print(f'❌ Error stopping Flask: {e}')
        return False

def start_flask():
    """Start the Flask app."""
    print_header('STEP 9: Starting Flask App')

    print('Starting Flask app with updated data...')

    try:
        # Start Flask in background
        # Redirect output to a log file
        log_file = Path('logs') / f'flask_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        log_file.parent.mkdir(exist_ok=True)

        with open(log_file, 'w') as f:
            proc = subprocess.Popen(
                ['python3', 'app.py'],
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=str(Path.cwd())
            )

        # Wait a few seconds and check if it started
        time.sleep(5)

        # Check if process is still running
        if proc.poll() is None:
            print(f'✅ Flask app started successfully (PID: {proc.pid})')
            print(f'📝 Flask logs: {log_file}')
            print(f'🌐 Access at: http://localhost:5001')
            return True
        else:
            print(f'❌ Flask app failed to start')
            print(f'Check logs: {log_file}')
            return False

    except Exception as e:
        print(f'❌ Error starting Flask: {e}')
        return False

def restart_flask():
    """Stop and restart the Flask app."""
    print_header('RESTARTING FLASK APP')

    # Check if Flask is running
    was_running = find_flask_process() is not None

    if was_running:
        # Stop Flask
        if not stop_flask():
            print('⚠️  Warning: Could not stop Flask app')
            print('You may need to restart it manually')
            return False

    # Start Flask
    if not start_flask():
        print('❌ Failed to start Flask app')
        print('Please start it manually: python3 app.py')
        return False

    return True

def main():
    """Main update workflow."""
    print('\n' + '=' * 70)
    print('  RCFE DATA AUTOMATIC UPDATE')
    print('  California Assisted Living Finder')
    print('=' * 70)

    start_time = datetime.now()

    # Step 1: Download latest data
    if not run_scraper():
        print('\n❌ Update failed: Could not download data')
        sys.exit(1)

    # Step 2: Compare data
    changes = compare_data()
    if changes is None:
        print('\n❌ Update failed: Could not compare data')
        sys.exit(1)

    # Step 3: Update geocode cache if needed
    if len(changes['new_facilities']) > 0 or len(changes['changed_facilities']) > 0:
        if not update_geocode_cache(changes):
            print('\n❌ Update failed: Geocoding error')
            sys.exit(1)

    # Step 4: Remove old facilities from cache
    remove_old_facilities(changes)

    # Step 5: Generate statistics
    stats = generate_statistics()

    # Step 6: Update README
    update_readme(stats)

    # Step 7: Backup current data
    backup_current_data()

    # Step 8 & 9: Restart Flask app with new data
    flask_restarted = restart_flask()

    # Summary
    end_time = datetime.now()
    duration = end_time - start_time

    print_header('UPDATE COMPLETE')
    print(f'✅ All steps completed successfully!')
    print(f'⏱️  Total time: {duration}')
    print(f'📊 Data updated to: {stats["date"]}')
    print(f'🗺️  Searchable facilities: {stats["total_geocoded"]:,}')

    if flask_restarted:
        print(f'\n🌐 Flask app restarted - website now showing updated data!')
        print(f'   Access at: http://localhost:5001')
    else:
        print(f'\n⚠️  Flask app needs manual restart')
        print(f'   Run: python3 app.py')

    print('=' * 70 + '\n')

if __name__ == '__main__':
    main()

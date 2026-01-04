#!/bin/bash
# Automated RCFE Data Update Scheduler
# This script sets up automatic updates on a schedule

PROJECT_DIR="/Users/anneneville-bonilla/Documents/claude-test"
PYTHON="/usr/bin/python3"
LOG_DIR="$PROJECT_DIR/logs"
UPDATE_SCRIPT="$PROJECT_DIR/update_data.py"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log file with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/update_$TIMESTAMP.log"

echo "========================================" | tee -a "$LOG_FILE"
echo "RCFE Data Update" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Change to project directory
cd "$PROJECT_DIR" || exit 1

# Run the update script
$PYTHON "$UPDATE_SCRIPT" 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "Finished: $(date)" | tee -a "$LOG_FILE"
echo "Log saved to: $LOG_FILE" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# Keep only last 30 days of logs
find "$LOG_DIR" -name "update_*.log" -mtime +30 -delete

exit 0

# PythonAnywhere WSGI Configuration Template
#
# Instructions:
# 1. On PythonAnywhere, go to Web tab
# 2. Click on your WSGI configuration file link
# 3. Replace ALL contents with this file
# 4. Update "yourusername" and "california-assisted-living" to match your setup
# 5. Save and reload your web app

import sys
import os

# ============================================
# IMPORTANT: Update these paths!
# ============================================

# Replace 'yourusername' with your actual PythonAnywhere username
USERNAME = 'yourusername'

# Replace 'california-assisted-living' with your project directory name
PROJECT_DIR = 'california-assisted-living'

# ============================================
# Configuration (don't change below this line)
# ============================================

# Add your project directory to the sys.path
project_home = f'/home/{USERNAME}/{PROJECT_DIR}'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment to production (disables debug mode)
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from app import app as application

# WSGI application is ready

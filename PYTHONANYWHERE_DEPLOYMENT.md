# Deploying to PythonAnywhere

## Overview

This guide will walk you through deploying the California Assisted Living Finder to PythonAnywhere's free tier.

**What you'll get:**
- Live website accessible at `yourusername.pythonanywhere.com`
- Automatic weekly data updates
- Free hosting (with limitations)

**Time to deploy:** ~30 minutes

---

## Step 1: Sign Up for PythonAnywhere

1. Go to https://www.pythonanywhere.com/
2. Click **"Pricing & signup"**
3. Choose **"Create a Beginner account"** (FREE)
4. Complete the signup process

**Free tier includes:**
- 1 web app
- 512 MB disk space
- Daily scheduled tasks
- Good for personal projects!

---

## Step 2: Upload Your Files

### Option A: Using Git (Recommended)

1. **On your local machine**, create a GitHub repository:
```bash
cd /Users/anneneville-bonilla/Documents/claude-test
git init
git add .
git commit -m "Initial commit - California Assisted Living Finder"
```

2. Create a new repository on GitHub.com

3. Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

4. **On PythonAnywhere**, open a Bash console (from Dashboard)

5. Clone your repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### Option B: Upload Files Manually

1. On PythonAnywhere, go to **"Files"** tab
2. Create a new directory (e.g., `california-assisted-living`)
3. Upload all files:
   - `app.py`
   - `rcfe_scraper.py`
   - `update_data.py`
   - `requirements.txt`
   - `geocode_cache.json`
   - `data/` folder (with CSV files)
   - `templates/` folder (with index.html)
   - `static/` folder (with README.md, etc.)

---

## Step 3: Install Dependencies

1. Open a **Bash console** on PythonAnywhere

2. Navigate to your project:
```bash
cd california-assisted-living  # Or your directory name
```

3. Install required packages:
```bash
pip3.10 install --user -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install chromium
```

**Note:** If you get disk space errors, see "Troubleshooting" section.

---

## Step 4: Configure the Web App

1. Go to **"Web"** tab on PythonAnywhere

2. Click **"Add a new web app"**

3. Choose **"Manual configuration"** (not Flask)

4. Choose **Python 3.10**

5. Click through to finish setup

### Configure WSGI File

1. In the **"Web"** tab, scroll to **"Code"** section

2. Click on the **WSGI configuration file** link (looks like `/var/www/yourusername_pythonanywhere_com_wsgi.py`)

3. **Delete all existing content** and replace with:

```python
# WSGI configuration for California Assisted Living Finder

import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/california-assisted-living'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment to production
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from app import app as application
```

**IMPORTANT:** Replace `yourusername` with your actual PythonAnywhere username!

4. Click **"Save"**

### Set Working Directory

1. Still in the **"Web"** tab, scroll to **"Code"** section

2. In **"Working directory"**, enter:
```
/home/yourusername/california-assisted-living
```
(Replace `yourusername` with your actual username)

### Configure Static Files

1. In **"Web"** tab, scroll to **"Static files"** section

2. Add a new static file mapping:
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/california-assisted-living/static`

3. Click the checkmark to save

### Reload the Web App

1. Scroll to top of **"Web"** tab

2. Click the big green **"Reload yourusername.pythonanywhere.com"** button

3. Click the link to view your site!

---

## Step 5: Set Up Automatic Updates

PythonAnywhere's free tier allows **one daily scheduled task**.

1. Go to **"Tasks"** tab

2. Click **"Create a new scheduled task"**

3. Configure the task:
   - **Time (UTC):** Choose a time (e.g., `02:00` for 2 AM UTC)
   - **Command:**
   ```bash
   cd /home/yourusername/california-assisted-living && /usr/bin/python3.10 update_data.py >> logs/update_cron.log 2>&1
   ```
   (Replace `yourusername` with your actual username)

4. Click **"Create"**

**Note:** Free tier only allows daily tasks, not weekly. If you want weekly, you'll need to upgrade to a paid account.

### Manual Data Updates

You can also run updates manually anytime:

1. Open a **Bash console**
2. Run:
```bash
cd california-assisted-living
python3.10 update_data.py
```

3. After update completes, reload your web app in the **"Web"** tab

---

## Step 6: Test Your Live Site

1. Visit `https://yourusername.pythonanywhere.com`

2. Test the search functionality:
   - Enter an address
   - Check map displays
   - Check facility details
   - Try filters
   - Download CSV
   - View README and Data Dictionary

3. Verify everything works!

---

## Important Notes

### Free Tier Limitations

**✅ What works:**
- Your website is live and accessible
- All search functionality
- Map and filters
- Data updates (daily scheduled task)
- Download features

**⚠️ Limitations:**
- Only 1 daily scheduled task (not weekly)
- 512 MB disk space
- Slower performance than paid tiers
- Site sleeps after inactivity (wakes on first request)

### Upgrading Storage

If you run out of disk space (geocode cache is large):

**Option 1: Clean up old logs**
```bash
cd california-assisted-living/logs
rm update_*.log flask_*.log  # Keep recent ones
```

**Option 2: Upgrade to Hacker tier ($5/month)**
- 1 GB storage
- More CPU time
- Faster performance
- Multiple scheduled tasks (weekly updates!)

---

## Sharing Your Site

Your site is live at:
```
https://yourusername.pythonanywhere.com
```

Share this URL with anyone! No login required to use the site.

**For custom domain (optional):**
Upgrade to paid tier to use your own domain name (e.g., `californiaalfinder.com`)

---

## Troubleshooting

### Error: "No module named 'flask'"

**Solution:**
```bash
pip3.10 install --user flask requests playwright psutil
```

### Error: "Disk quota exceeded"

**Solution:**
1. Check disk usage:
```bash
du -sh *
```

2. Remove old logs:
```bash
cd logs
rm update_*.log flask_*.log
```

3. If still over limit, upgrade to Hacker tier

### Error: "Playwright browsers not found"

**Solution:**
```bash
playwright install chromium
```

If disk space is tight:
```bash
playwright install chromium --with-deps
```

### Web app shows "Something went wrong"

**Solution:**
1. Check error log in **"Web"** tab (click on error log path)
2. Common issues:
   - Wrong path in WSGI file
   - Missing dependencies
   - Wrong Python version

### Data update fails

**Solution:**
1. Check logs:
```bash
cat logs/update_cron.log
```

2. Test manually:
```bash
cd california-assisted-living
python3.10 update_data.py
```

3. Common issues:
   - Playwright not installed
   - Disk space full
   - Network timeout (DSS website slow)

### Flask restart not working in update script

**Solution:**
On PythonAnywhere, you need to reload the web app via API or manually.

**Option 1: Manual reload after updates**
After scheduled update runs, manually click "Reload" in Web tab

**Option 2: Use PythonAnywhere API (requires API token)**
Modify `update_data.py` to use PythonAnywhere's reload API instead of process management

---

## Monitoring Your Site

### View Logs

**Web app error log:**
1. Go to **"Web"** tab
2. Click on error log path
3. View recent errors

**Access log:**
1. Go to **"Web"** tab
2. Click on access log path
3. See who's visiting your site!

**Update logs:**
```bash
cd california-assisted-living/logs
tail -f update_cron.log
```

### Check Scheduled Task

1. Go to **"Tasks"** tab
2. See last run time
3. View task history

---

## Updating Your Code

### Using Git

1. Make changes locally
2. Commit and push:
```bash
git add .
git commit -m "Updated features"
git push
```

3. On PythonAnywhere Bash console:
```bash
cd california-assisted-living
git pull
```

4. Reload web app in **"Web"** tab

### Manual Upload

1. Upload changed files via **"Files"** tab
2. Reload web app in **"Web"** tab

---

## Next Steps

**After deployment:**

1. ✅ Test all functionality
2. ✅ Share the URL with friends/family
3. ✅ Monitor logs for errors
4. ✅ Check scheduled task is running
5. ✅ Consider upgrading if you hit storage limits

**Optional enhancements:**
- Custom domain name (requires paid tier)
- HTTPS (included free on PythonAnywhere)
- Analytics (add Google Analytics to index.html)
- Contact form (collect user feedback)

---

## Support

**PythonAnywhere Help:**
- Help pages: https://help.pythonanywhere.com/
- Forums: https://www.pythonanywhere.com/forums/
- Email: support@pythonanywhere.com

**App-Specific Issues:**
- Check logs first
- Test locally first
- Review troubleshooting section above

---

## Cost Summary

**Free tier:** $0/month
- Good for: Personal use, demos, low traffic
- Limitations: 1 daily task, 512 MB storage

**Hacker tier:** $5/month
- Good for: Regular use, shared with others
- Benefits: 1 GB storage, weekly tasks, faster

**Choose free to start, upgrade if needed!**

---

## Deployment Checklist

- [ ] PythonAnywhere account created
- [ ] Files uploaded (Git or manual)
- [ ] Dependencies installed
- [ ] WSGI file configured
- [ ] Web app reloaded
- [ ] Site tested and working
- [ ] Scheduled task created
- [ ] Manual update tested
- [ ] Logs checked
- [ ] URL shared!

**Congratulations! Your site is live! 🎉**

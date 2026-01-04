# PythonAnywhere Deployment - Quick Start

**Goal:** Get your site live in ~30 minutes

---

## Prerequisites

- [ ] PythonAnywhere free account: https://www.pythonanywhere.com/
- [ ] GitHub account (optional, but recommended)

---

## Quick Steps

### 1. Sign Up (5 minutes)
- Go to https://www.pythonanywhere.com/
- Create free "Beginner" account
- Confirm email

### 2. Upload Code (10 minutes)

**Option A: Via GitHub (Recommended)**
```bash
# On your local machine
cd /Users/anneneville-bonilla/Documents/claude-test
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# On PythonAnywhere Bash console
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

**Option B: Manual Upload**
- Use PythonAnywhere "Files" tab
- Upload all files

### 3. Install Dependencies (5 minutes)
```bash
# On PythonAnywhere Bash console
cd your-project-directory
pip3.10 install --user -r requirements.txt
playwright install chromium
```

### 4. Configure Web App (5 minutes)

1. Go to "Web" tab → "Add a new web app"
2. Choose "Manual configuration" → Python 3.10
3. Click WSGI file link
4. Replace contents with `pythonanywhere_wsgi.py` (update USERNAME)
5. Set Working Directory: `/home/yourusername/your-project-directory`
6. Add Static Files mapping:
   - URL: `/static/`
   - Directory: `/home/yourusername/your-project-directory/static`
7. Click "Reload" button

### 5. Test Your Site! (2 minutes)
- Visit `https://yourusername.pythonanywhere.com`
- Search for facilities
- Verify everything works

### 6. Set Up Auto-Updates (3 minutes)

1. Go to "Tasks" tab
2. Create new scheduled task:
   - Time: `02:00` (2 AM UTC)
   - Command:
   ```bash
   cd /home/yourusername/your-project-directory && /usr/bin/python3.10 update_data.py >> logs/update_cron.log 2>&1
   ```

---

## Your Site is Live! 🎉

**Share:** `https://yourusername.pythonanywhere.com`

**Next Steps:**
- Test all features
- Check logs regularly
- Run manual update to test: `python3.10 update_data.py`

---

## Need Help?

See detailed guide: `PYTHONANYWHERE_DEPLOYMENT.md`

**Common Issues:**

1. **"No module named 'flask'"**
   ```bash
   pip3.10 install --user flask requests playwright psutil
   ```

2. **Site shows error**
   - Check error log in Web tab
   - Verify WSGI file paths are correct

3. **Update fails**
   ```bash
   cat logs/update_cron.log
   ```

---

## Free Tier Limits

✅ **Included:**
- 1 web app
- 512 MB storage
- Daily scheduled task
- HTTPS included

⚠️ **Limitations:**
- Only daily tasks (not weekly)
- Site sleeps after inactivity

**Upgrade to $5/month "Hacker" tier for:**
- 1 GB storage
- Multiple scheduled tasks (weekly updates!)
- Better performance

---

## File Checklist for Deployment

Make sure these files are uploaded:
- [ ] `app.py`
- [ ] `rcfe_scraper.py`
- [ ] `update_data.py`
- [ ] `requirements.txt`
- [ ] `geocode_cache.json`
- [ ] `data/rcfe_data_latest.csv`
- [ ] `templates/index.html`
- [ ] `static/README.md`
- [ ] `static/DATA_DICTIONARY.md`
- [ ] `static/not_geocoded.txt`

---

## Updates After Deployment

**To update your live site:**

Via Git:
```bash
# Local machine
git add .
git commit -m "Update"
git push

# PythonAnywhere console
cd your-project-directory
git pull
# Then reload web app in Web tab
```

Manual:
- Upload changed files via Files tab
- Reload web app in Web tab

---

**Time Investment:**
- Initial setup: ~30 minutes
- After that: Automatic updates!
- You only use Claude if something breaks

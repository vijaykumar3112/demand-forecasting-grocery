# 🔧 Why Your API Goes Offline & How to Fix It Permanently

## 🚨 Common Reasons Why APIs Go Offline After Deployment

### 1. **Free Tier Inactivity Timeout** ⏰
**Most Common Issue!**

Free hosting platforms like Render.com, Railway, and Heroku **spin down** (sleep) your API after **15 minutes of inactivity** to save resources.

**What happens:**
- ✅ API deploys successfully
- ✅ Works fine initially
- ❌ After 15 minutes of no requests → **API goes to sleep**
- ❌ Next request takes 30-60 seconds to "wake up"
- ❌ Dashboard shows "API offline" or timeout errors

**Solution:**
- Use a **keep-alive service** (see solutions below)
- Upgrade to paid tier (always-on)
- Accept the cold start delay

---

### 2. **Missing Environment Variables** 🔐

Your API might crash on startup if required files or configurations are missing.

**Common issues:**
- Model files not included in deployment
- Wrong file paths in production
- Missing data files

**Solution:**
- Ensure all model files are committed to Git
- Use relative paths, not absolute paths
- Check deployment logs for errors

---

### 3. **Memory/Resource Limits Exceeded** 💾

Free tiers have strict memory limits (usually 512MB). Your API might crash if it uses too much memory.

**What causes this:**
- Large model files (LightGBM models can be 50-200MB)
- Loading too much data into memory
- Memory leaks

**Solution:**
- Optimize model size
- Use lazy loading
- Monitor memory usage

---

### 4. **Build/Start Command Failures** ⚙️

Your API might fail to start due to:
- Missing dependencies
- Wrong Python version
- Incorrect start command

**Solution:**
- Check deployment logs
- Verify `requirements.txt` is complete
- Test locally with same commands

---

### 5. **Health Check Failures** 🏥

Some platforms (like Render) check if your API is healthy. If health checks fail, they shut down the service.

**Solution:**
- Ensure `/health` endpoint works
- Return proper status codes
- Keep health checks lightweight

---

## ✅ PERMANENT SOLUTIONS

### Solution 1: **Keep-Alive Service** (Recommended for Free Tier)

Use a free service to ping your API every 10-14 minutes to prevent it from sleeping.

#### Option A: UptimeRobot (Free)
1. Go to https://uptimerobot.com
2. Sign up (free)
3. Click **"Add New Monitor"**
4. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Demand Forecasting API
   - **URL**: `https://your-api-url.onrender.com/health`
   - **Monitoring Interval**: 5 minutes
5. Save

**Result:** Your API will receive a request every 5 minutes and stay awake! 🎉

#### Option B: Cron-Job.org (Free)
1. Go to https://cron-job.org
2. Sign up (free)
3. Create new cron job:
   - **URL**: `https://your-api-url.onrender.com/health`
   - **Schedule**: Every 10 minutes
4. Enable the job

#### Option C: GitHub Actions (Free)
Add this file to your repository:

**`.github/workflows/keep-alive.yml`**
```yaml
name: Keep API Alive

on:
  schedule:
    # Run every 10 minutes
    - cron: '*/10 * * * *'
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping API Health Endpoint
        run: |
          curl -f https://your-api-url.onrender.com/health || echo "API is down"
      - name: Ping API Root
        run: |
          curl -f https://your-api-url.onrender.com/ || echo "API is down"
```

**Replace** `your-api-url.onrender.com` with your actual API URL.

---

### Solution 2: **Upgrade to Paid Tier** 💳

**Render.com Pricing:**
- Free: $0/month (sleeps after 15 min)
- Starter: $7/month (always-on, 512MB RAM)
- Standard: $25/month (always-on, 2GB RAM)

**Railway.app Pricing:**
- Free: $5 credit/month (runs out quickly)
- Hobby: $5/month (500 hours, ~16 hours/day)
- Pro: $20/month (unlimited)

**Recommendation:** If this is for production or a presentation, spend $7-20/month for reliability.

---

### Solution 3: **Optimize Your API for Cold Starts** ❄️

Make your API start faster so the "wake-up" delay is minimal.

**Add to `api/app.py`:**
```python
import os

# Lazy load models (only when needed)
_predictor = None

def get_predictor():
    global _predictor
    if _predictor is None:
        from api.predictor import DemandPredictor
        _predictor = DemandPredictor()
    return _predictor

# Add startup optimization
@app.on_event("startup")
async def startup_event():
    """Pre-load models on startup"""
    logger.info("🚀 Starting API...")
    # Pre-warm the predictor
    get_predictor()
    logger.info("✅ Ready!")
```

---

### Solution 4: **Use Multiple Free Services** 🔄

Deploy your API on **multiple platforms** and use the most reliable one:

1. **Primary**: Render.com (with UptimeRobot)
2. **Backup**: Railway.app
3. **Backup**: Fly.io

Update your dashboard to try multiple API URLs:

**In `frontend/app.py`:**
```python
import os
import requests

# Multiple API endpoints (fallback)
API_URLS = [
    os.getenv("API_URL", "http://localhost:8000"),
    "https://demand-api.onrender.com",
    "https://demand-api.railway.app",
]

def get_working_api():
    """Find the first working API"""
    for url in API_URLS:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                return url
        except:
            continue
    return API_URLS[0]  # Default to first

API_URL = get_working_api()
```

---

### Solution 5: **Self-Host on Always-On Server** 🖥️

If you have access to a server or VPS:

**Options:**
- AWS EC2 (free tier for 1 year)
- Google Cloud Compute Engine (free tier)
- DigitalOcean Droplet ($4/month)
- Your own computer (with ngrok for public access)

**Pros:**
- Always online
- Full control
- No cold starts

**Cons:**
- Requires server management
- More complex setup

---

## 🎯 RECOMMENDED SOLUTION FOR YOUR PROJECT

Based on your project being a **demand forecasting grocery platform**, here's what I recommend:

### For Development/Testing:
1. ✅ Deploy on **Render.com** (free)
2. ✅ Set up **UptimeRobot** to keep it alive
3. ✅ Accept 30-second cold start on first request after long idle

### For Presentation/Demo:
1. ✅ Upgrade to **Render Starter** ($7/month) for 1 month
2. ✅ Or use **Railway Hobby** ($5/month)
3. ✅ This ensures **zero downtime** during your demo

### For Production:
1. ✅ Use **Render Standard** ($25/month) or **Railway Pro** ($20/month)
2. ✅ Add monitoring (UptimeRobot + error tracking)
3. ✅ Set up auto-scaling if needed

---

## 🔍 How to Check Why Your API is Offline

### Step 1: Check Deployment Logs

**Render.com:**
1. Go to your service dashboard
2. Click **"Logs"** tab
3. Look for errors during startup

**Railway.app:**
1. Open your project
2. Click on the API service
3. View **"Deployments"** → **"Logs"**

### Step 2: Test Health Endpoint

```bash
curl https://your-api-url.com/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "api_version": "1.2.0",
  "model_loaded": true,
  "features_count": 15,
  "uptime_seconds": 123.45
}
```

### Step 3: Check API Documentation

```bash
# Visit in browser
https://your-api-url.com/docs
```

If this loads, your API is online!

---

## 📊 Monitoring Your API

### Add Uptime Monitoring

**UptimeRobot Dashboard:**
- Shows uptime percentage (aim for 99%+)
- Alerts you via email when API goes down
- Historical uptime data

### Add Error Tracking

**Option 1: Sentry (Free tier available)**
```python
# Add to api/app.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

**Option 2: Simple Logging**
```python
# Already in your code
logger.error(f"Error: {e}")
```

---

## 🚀 QUICK FIX RIGHT NOW

### Immediate Action (5 minutes):

1. **Set up UptimeRobot:**
   - Go to https://uptimerobot.com
   - Add monitor for your API
   - Set interval to 5 minutes

2. **Verify API is running:**
   ```bash
   curl https://your-api-url.onrender.com/health
   ```

3. **Check Render logs:**
   - Look for any errors
   - Verify model loaded successfully

4. **Test from dashboard:**
   - Open your Streamlit dashboard
   - Try generating a forecast
   - First request might be slow (cold start)

---

## 📝 Summary

### Why APIs Go Offline:
1. ⏰ **Inactivity timeout** (most common)
2. 💾 **Memory limits exceeded**
3. ❌ **Build/startup failures**
4. 🔐 **Missing configurations**

### Permanent Fix:
1. ✅ **Use UptimeRobot** (free, 5 minutes to set up)
2. ✅ **Or upgrade to paid tier** ($7-20/month)
3. ✅ **Or deploy on multiple platforms** (redundancy)

### Best Practice:
- **Free tier + UptimeRobot** = 95% uptime
- **Paid tier** = 99.9% uptime
- **Multiple deployments** = Maximum reliability

---

## 🎉 Next Steps

1. Choose a solution from above
2. Implement it (5-30 minutes)
3. Test your API
4. Monitor uptime
5. Enjoy a reliable API! 🚀

---

**Need help?** Check the deployment logs first, then review this guide.

**Created:** November 24, 2025  
**Status:** ✅ COMPLETE GUIDE  
**Recommended:** UptimeRobot + Render.com Free Tier

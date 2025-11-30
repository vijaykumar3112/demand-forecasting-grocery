# 🚀 Quick Setup: Keep Your API Online 24/7

## ⚡ 5-Minute Setup (Recommended)

### Step 1: Set Up UptimeRobot (FREE - Takes 3 minutes)

1. **Go to UptimeRobot:**
   - Visit: https://uptimerobot.com
   - Click **"Sign Up Free"**
   - Use your email or sign up with Google

2. **Add Your API Monitor:**
   - Click **"+ Add New Monitor"**
   - Fill in the form:
     ```
     Monitor Type: HTTP(s)
     Friendly Name: Demand Forecasting API
     URL: https://your-api-url.onrender.com/health
     Monitoring Interval: 5 minutes
     ```
   - Click **"Create Monitor"**

3. **Add Dashboard Monitor (Optional):**
   - Click **"+ Add New Monitor"** again
   - Fill in:
     ```
     Monitor Type: HTTP(s)
     Friendly Name: Demand Forecasting Dashboard
     URL: https://your-dashboard-url.onrender.com
     Monitoring Interval: 5 minutes
     ```
   - Click **"Create Monitor"**

4. **Done!** ✅
   - Your API will now receive a ping every 5 minutes
   - It will NEVER go to sleep
   - You'll get email alerts if it goes down

---

## 🔧 Alternative: Enable GitHub Actions (Takes 2 minutes)

If you prefer automated pings from GitHub:

1. **File Already Created:**
   - `.github/workflows/keep-alive.yml` ✅

2. **Update the API URL:**
   - Open `.github/workflows/keep-alive.yml`
   - Replace `https://demand-forecasting-api.onrender.com` with your actual API URL

3. **Commit and Push:**
   ```bash
   git add .github/workflows/keep-alive.yml
   git commit -m "Add keep-alive workflow"
   git push origin main
   ```

4. **Enable the Workflow:**
   - Go to your GitHub repository
   - Click **"Actions"** tab
   - Enable workflows if prompted
   - The workflow will run every 10 minutes automatically

---

## 📊 Verify It's Working

### Test 1: Check UptimeRobot Dashboard
- Go to https://uptimerobot.com/dashboard
- You should see your monitors with **green status**
- Uptime should show **100%** after a few hours

### Test 2: Check API Directly
```bash
curl https://your-api-url.onrender.com/health
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

### Test 3: Check GitHub Actions (if using)
- Go to your repository → **Actions** tab
- You should see the "Keep API Alive" workflow running every 10 minutes
- All runs should show **green checkmarks** ✅

---

## 🎯 What You Get

### With UptimeRobot:
- ✅ API stays online 24/7
- ✅ No cold starts (instant responses)
- ✅ Email alerts if API goes down
- ✅ Uptime statistics and reports
- ✅ 100% FREE for up to 50 monitors

### With GitHub Actions:
- ✅ API stays online 24/7
- ✅ No external dependencies
- ✅ Runs automatically every 10 minutes
- ✅ 100% FREE (GitHub Actions free tier)

### Best Practice:
**Use BOTH** for maximum reliability! 🚀

---

## 🔍 Troubleshooting

### Issue: UptimeRobot shows "Down"
**Solution:**
1. Check your API URL is correct
2. Verify API is deployed on Render
3. Check Render logs for errors
4. Try accessing the URL in your browser

### Issue: GitHub Actions failing
**Solution:**
1. Check the workflow file has correct API URL
2. Verify the repository has Actions enabled
3. Check the Actions tab for error logs

### Issue: API still goes to sleep
**Solution:**
1. Verify monitoring interval is 5-10 minutes (not longer)
2. Check that health endpoint `/health` works
3. Ensure Render service is not paused manually

---

## 💡 Pro Tips

### Tip 1: Monitor Multiple Endpoints
Add monitors for:
- `/health` - Health check
- `/` - Root endpoint
- `/docs` - API documentation

### Tip 2: Set Up Alerts
In UptimeRobot:
- Go to **"My Settings"** → **"Alert Contacts"**
- Add your email
- Get notified instantly if API goes down

### Tip 3: Check Uptime Reports
- View daily/weekly/monthly uptime
- Aim for 99%+ uptime
- Identify patterns if API goes down

---

## 📈 Expected Results

### Before Setup:
- ❌ API goes to sleep after 15 minutes
- ❌ First request takes 30-60 seconds (cold start)
- ❌ Dashboard shows "API offline" errors
- ❌ Poor user experience

### After Setup:
- ✅ API stays online 24/7
- ✅ All requests are instant (< 1 second)
- ✅ Dashboard always works
- ✅ Professional, reliable service

---

## 🎉 You're Done!

Your API will now stay online permanently! 🚀

**Time invested:** 5 minutes  
**Cost:** $0 (FREE)  
**Benefit:** 24/7 uptime, instant responses, professional service

---

## 📞 Need Help?

1. **Check the main guide:** `API_OFFLINE_FIX.md`
2. **Check deployment logs:** Render.com dashboard → Logs
3. **Test health endpoint:** `curl https://your-api-url/health`

---

**Created:** November 24, 2025  
**Status:** ✅ READY TO USE  
**Recommended:** UptimeRobot (5 minutes to set up)

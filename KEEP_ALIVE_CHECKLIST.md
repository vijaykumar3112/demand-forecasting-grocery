# ✅ API Keep-Alive Checklist

## 🎯 Goal: Keep Your API Online 24/7

---

## 📋 Quick Setup (5 Minutes)

### Step 1: Set Up UptimeRobot
- [ ] Go to https://uptimerobot.com
- [ ] Click "Sign Up Free"
- [ ] Verify your email
- [ ] Click "+ Add New Monitor"
- [ ] Configure monitor:
  - [ ] Monitor Type: **HTTP(s)**
  - [ ] Friendly Name: **Demand Forecasting API**
  - [ ] URL: **https://your-api-url.onrender.com/health**
  - [ ] Monitoring Interval: **5 minutes**
- [ ] Click "Create Monitor"
- [ ] ✅ Done!

### Step 2: Verify It's Working
- [ ] Check UptimeRobot dashboard (should show green status)
- [ ] Test API: `curl https://your-api-url/health`
- [ ] Wait 15 minutes
- [ ] Test API again (should still be instant, no delay)
- [ ] ✅ API is now online 24/7!

---

## 🔧 Optional: GitHub Actions Backup

### Enable Automated Pings
- [ ] Open `.github/workflows/keep-alive.yml`
- [ ] Replace `https://demand-forecasting-api.onrender.com` with your actual API URL
- [ ] Save the file
- [ ] Commit changes:
  ```bash
  git add .github/workflows/keep-alive.yml
  git commit -m "Enable keep-alive workflow"
  git push origin main
  ```
- [ ] Go to GitHub → Your repo → Actions tab
- [ ] Verify workflow is enabled
- [ ] ✅ Automated pings active!

---

## 📊 Monitoring Checklist

### Daily (First Week)
- [ ] Check UptimeRobot dashboard
- [ ] Verify uptime is 100%
- [ ] Test API manually
- [ ] Check for any downtime alerts

### Weekly (Ongoing)
- [ ] Review uptime statistics
- [ ] Check response times
- [ ] Verify no errors in Render logs

### Monthly
- [ ] Review overall uptime (should be 99%+)
- [ ] Consider upgrading to paid tier if needed
- [ ] Update monitoring settings if needed

---

## 🚨 Troubleshooting Checklist

### If API Shows "Down" in UptimeRobot:
- [ ] Check Render dashboard (is service running?)
- [ ] Check Render logs for errors
- [ ] Test health endpoint manually: `curl https://your-api-url/health`
- [ ] Verify API URL is correct in UptimeRobot
- [ ] Check if Render service is paused

### If API is Slow:
- [ ] Check Render logs for memory issues
- [ ] Verify model files are loading correctly
- [ ] Consider optimizing model size
- [ ] Consider upgrading to paid tier

### If Dashboard Can't Connect:
- [ ] Verify `API_URL` environment variable is set
- [ ] Check CORS settings in `api/app.py`
- [ ] Test API directly (not through dashboard)
- [ ] Check dashboard logs in Render

---

## 💡 Best Practices

### Do This:
- [x] Use UptimeRobot (free, reliable)
- [x] Set monitoring interval to 5-10 minutes
- [x] Enable email alerts
- [x] Monitor uptime statistics
- [x] Keep model files in Git repository
- [x] Use relative paths in code

### Don't Do This:
- [ ] ❌ Set monitoring interval > 15 minutes (API will sleep)
- [ ] ❌ Ignore downtime alerts
- [ ] ❌ Use absolute paths in code
- [ ] ❌ Forget to commit model files
- [ ] ❌ Disable health checks

---

## 🎯 Success Criteria

Your setup is successful when:
- ✅ UptimeRobot shows 99%+ uptime
- ✅ API responds instantly (< 1 second)
- ✅ No cold start delays
- ✅ Dashboard always works
- ✅ No "API offline" errors

---

## 📈 Upgrade Checklist (Optional)

### When to Upgrade to Paid Tier:
- [ ] You need 99.9% uptime guarantee
- [ ] You're presenting to stakeholders
- [ ] You're deploying to production
- [ ] You need faster response times
- [ ] You need more memory (> 512MB)

### Recommended Paid Plans:
- [ ] **Render Starter** ($7/month) - Good for demos/presentations
- [ ] **Render Standard** ($25/month) - Good for production
- [ ] **Railway Hobby** ($5/month) - Budget option
- [ ] **Railway Pro** ($20/month) - Production option

---

## 📞 Resources

### Documentation:
- [ ] Read `API_SOLUTION_SUMMARY.md` (overview)
- [ ] Read `API_OFFLINE_FIX.md` (detailed guide)
- [ ] Read `KEEP_ALIVE_SETUP.md` (setup instructions)
- [ ] Read `DEPLOYMENT_GUIDE.md` (deployment help)

### Tools:
- [ ] UptimeRobot: https://uptimerobot.com
- [ ] Render Dashboard: https://dashboard.render.com
- [ ] GitHub Actions: Your repo → Actions tab

### Testing:
```bash
# Health check
curl https://your-api-url/health

# Full test
curl -X POST https://your-api-url/predict \
  -H "Content-Type: application/json" \
  -d '{"item_id": 1, "store_id": 1, "date": "2025-11-24", "on_promotion": false}'
```

---

## ✅ Final Checklist

Before you're done:
- [ ] UptimeRobot is set up and monitoring
- [ ] API health endpoint returns 200 OK
- [ ] Dashboard can connect to API
- [ ] You've tested making a prediction
- [ ] You've verified no cold start delays
- [ ] You've set up email alerts
- [ ] You've bookmarked UptimeRobot dashboard

---

## 🎉 Congratulations!

If all items are checked, your API is now:
- ✅ Online 24/7
- ✅ Fast and reliable
- ✅ Production-ready
- ✅ Professionally monitored

**Time invested:** 5 minutes  
**Cost:** $0  
**Result:** Permanent solution

---

**Created:** November 24, 2025  
**Status:** ✅ READY TO USE  
**Next Step:** Set up UptimeRobot now!

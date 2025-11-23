# 🚀 Deployment Guide - Demand Forecasting Platform

## ✅ Local Testing Completed

Your application is **fully functional** and tested locally:

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501

---

## 🌐 Deploying Online (Multiple Options)

### Option 1: **Render.com** (Recommended - Free Tier Available)

#### Step 1: Prepare Your Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### Step 2: Deploy API on Render
1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `vijaykumar3112/demand-forecasting-grocery`
4. Configure:
   - **Name**: `demand-forecasting-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free
5. Click **"Create Web Service"**
6. Wait for deployment (5-10 minutes)
7. Copy your API URL (e.g., `https://demand-forecasting-api.onrender.com`)

#### Step 3: Deploy Dashboard on Render
1. Click **"New +"** → **"Web Service"** again
2. Connect the same repository
3. Configure:
   - **Name**: `demand-forecasting-dashboard`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0`
   - **Environment Variables**:
     - `API_URL` = `https://demand-forecasting-api.onrender.com` (from Step 2)
   - **Instance Type**: Free
4. Click **"Create Web Service"**
5. Your dashboard will be live at `https://demand-forecasting-dashboard.onrender.com`

---

### Option 2: **Railway.app** (Easy Deployment)

#### Deploy Both Services
1. Go to [railway.app](https://railway.app) and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway will auto-detect the services from `docker-compose.yml`
5. Set environment variables:
   - For dashboard service: `API_URL` = `https://<your-api-service>.railway.app`
6. Deploy and get your public URLs

---

### Option 3: **Streamlit Community Cloud** (Dashboard Only - Easiest)

#### For Dashboard Only (Free)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select:
   - Repository: `vijaykumar3112/demand-forecasting-grocery`
   - Branch: `main`
   - Main file path: `frontend/app.py`
5. **Advanced settings** → Add secrets:
   ```toml
   API_URL = "http://localhost:8000"  # Or your deployed API URL
   ```
6. Click **"Deploy"**
7. Your dashboard will be live at `https://share.streamlit.io/vijaykumar3112/demand-forecasting-grocery`

**Note**: You'll still need to deploy the API separately (use Render or Railway for API)

---

### Option 4: **Heroku** (Classic Choice)

#### Deploy API
```bash
# Install Heroku CLI
# Create Procfile for API
echo "web: uvicorn api.app:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
heroku login
heroku create demand-forecasting-api
git push heroku main
```

#### Deploy Dashboard
```bash
# Create separate Procfile for dashboard
echo "web: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0" > Procfile.dashboard

# Deploy
heroku create demand-forecasting-dashboard
heroku config:set API_URL=https://demand-forecasting-api.herokuapp.com
git push heroku main
```

---

### Option 5: **Docker + Cloud Run (Google Cloud)**

#### Build and Deploy
```bash
# Build Docker images
docker build -t gcr.io/YOUR_PROJECT/demand-api -f Dockerfile .
docker build -t gcr.io/YOUR_PROJECT/demand-dashboard -f Dockerfile.streamlit .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT/demand-api
docker push gcr.io/YOUR_PROJECT/demand-dashboard

# Deploy to Cloud Run
gcloud run deploy demand-api --image gcr.io/YOUR_PROJECT/demand-api --platform managed
gcloud run deploy demand-dashboard --image gcr.io/YOUR_PROJECT/demand-dashboard --platform managed
```

---

## 🔧 Required File Updates for Deployment

### 1. Update `frontend/app.py` to use environment variable for API URL

The file already has this, but make sure line 23 is:
```python
API_URL = os.getenv("API_URL", "http://localhost:8000")
```

### 2. Create `render.yaml` (Optional - for Render Blueprint)

```yaml
services:
  - type: web
    name: demand-forecasting-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api.app:app --host 0.0.0.0 --port $PORT
    
  - type: web
    name: demand-forecasting-dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: API_URL
        fromService:
          name: demand-forecasting-api
          type: web
          property: host
```

---

## 📊 Testing Your Deployment

Once deployed, test these endpoints:

### API Tests
```bash
# Health check
curl https://your-api-url.com/health

# Get valid ranges
curl https://your-api-url.com/items/valid-ranges

# Make a prediction
curl -X POST https://your-api-url.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "store_id": 1,
    "date": "2025-11-24",
    "on_promotion": false
  }'
```

### Dashboard Test
1. Open your dashboard URL
2. Navigate to "Demand Forecaster"
3. Fill in the form and generate a forecast
4. Verify the results appear correctly

---

## 🎯 Recommended Deployment Strategy

**For Quick Demo (Free)**:
1. Deploy API on **Render.com** (Free tier)
2. Deploy Dashboard on **Streamlit Community Cloud** (Free)

**For Production (Scalable)**:
1. Use **Railway.app** or **Google Cloud Run**
2. Set up custom domain
3. Enable HTTPS
4. Add monitoring and logging

---

## 🔐 Security Considerations

1. **API Keys**: Add authentication to your API endpoints
2. **CORS**: Update CORS settings in `api/app.py` for production
3. **Environment Variables**: Never commit sensitive data
4. **Rate Limiting**: Add rate limiting to prevent abuse

---

## 📝 Next Steps

1. Choose a deployment platform from above
2. Follow the specific instructions for that platform
3. Update the `API_URL` in your dashboard configuration
4. Test thoroughly
5. Share your live links!

---

## 🆘 Troubleshooting

### API won't start
- Check logs for missing dependencies
- Verify model files are included in deployment
- Ensure `LIGHTGBM_MODEL_PATH` points to correct location

### Dashboard can't connect to API
- Verify `API_URL` environment variable is set correctly
- Check CORS settings in API
- Ensure API is publicly accessible

### Slow performance
- Use caching (already implemented)
- Consider upgrading to paid tier
- Optimize model loading

---

## 📞 Support

For issues, check:
- Platform-specific documentation
- Application logs
- GitHub Issues

---

**Your application is production-ready and tested! 🎉**

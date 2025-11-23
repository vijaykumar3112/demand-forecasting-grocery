#!/bin/bash

# 🚀 Quick Deployment Script for Demand Forecasting Platform
# This script helps you deploy to various cloud platforms

echo "🚀 Demand Forecasting Platform - Deployment Helper"
echo "=================================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized!"
    echo "Run: git init"
    exit 1
fi

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "📝 You have uncommitted changes. Committing now..."
    git add .
    git commit -m "Prepare for deployment - $(date +%Y-%m-%d)"
    echo "✅ Changes committed"
else
    echo "✅ No uncommitted changes"
fi

echo ""
echo "Select deployment platform:"
echo "1. Render.com (Recommended - Free)"
echo "2. Railway.app (Easy - Free tier)"
echo "3. Streamlit Cloud (Dashboard only - Free)"
echo "4. Heroku (Classic)"
echo "5. Manual deployment (show instructions)"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "📦 Deploying to Render.com..."
        echo ""
        echo "Steps:"
        echo "1. Go to https://render.com and sign up"
        echo "2. Click 'New +' → 'Blueprint'"
        echo "3. Connect your GitHub repository"
        echo "4. Render will use the render.yaml file automatically"
        echo "5. Wait for deployment to complete"
        echo ""
        echo "Your render.yaml is ready! ✅"
        echo ""
        read -p "Press Enter to open Render.com..." 
        if command -v xdg-open &> /dev/null; then
            xdg-open "https://render.com"
        elif command -v open &> /dev/null; then
            open "https://render.com"
        else
            echo "Please open: https://render.com"
        fi
        ;;
    2)
        echo ""
        echo "🚂 Deploying to Railway.app..."
        echo ""
        echo "Steps:"
        echo "1. Go to https://railway.app and sign up"
        echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
        echo "3. Select your repository"
        echo "4. Railway will auto-detect services"
        echo "5. Set API_URL environment variable for dashboard"
        echo ""
        read -p "Press Enter to open Railway.app..." 
        if command -v xdg-open &> /dev/null; then
            xdg-open "https://railway.app"
        elif command -v open &> /dev/null; then
            open "https://railway.app"
        else
            echo "Please open: https://railway.app"
        fi
        ;;
    3)
        echo ""
        echo "☁️ Deploying to Streamlit Cloud..."
        echo ""
        echo "Steps:"
        echo "1. Go to https://share.streamlit.io"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New app'"
        echo "4. Select your repository and branch"
        echo "5. Set main file: frontend/app.py"
        echo "6. Deploy!"
        echo ""
        echo "⚠️ Note: You'll need to deploy the API separately"
        echo ""
        read -p "Press Enter to open Streamlit Cloud..." 
        if command -v xdg-open &> /dev/null; then
            xdg-open "https://share.streamlit.io"
        elif command -v open &> /dev/null; then
            open "https://share.streamlit.io"
        else
            echo "Please open: https://share.streamlit.io"
        fi
        ;;
    4)
        echo ""
        echo "🔷 Deploying to Heroku..."
        echo ""
        if ! command -v heroku &> /dev/null; then
            echo "❌ Heroku CLI not installed"
            echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        echo "Deploying API..."
        heroku create demand-forecasting-api-$(date +%s)
        git push heroku main
        
        echo ""
        echo "✅ API deployed!"
        echo "Now deploying dashboard..."
        
        heroku create demand-forecasting-dashboard-$(date +%s)
        heroku config:set API_URL=$(heroku info -s | grep web_url | cut -d= -f2)
        git push heroku main
        
        echo ""
        echo "✅ Dashboard deployed!"
        ;;
    5)
        echo ""
        echo "📖 Manual Deployment Instructions"
        echo ""
        echo "Please refer to DEPLOYMENT_GUIDE.md for detailed instructions"
        echo ""
        if [ -f "DEPLOYMENT_GUIDE.md" ]; then
            cat DEPLOYMENT_GUIDE.md
        fi
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment process initiated!"
echo ""
echo "📚 For more details, see:"
echo "   - DEPLOYMENT_GUIDE.md"
echo "   - TESTING_SUMMARY.md"
echo ""
echo "🎉 Good luck with your deployment!"

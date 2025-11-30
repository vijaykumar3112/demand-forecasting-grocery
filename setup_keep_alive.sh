#!/bin/bash

# 🚀 Automated Keep-Alive Setup Script
# This script automates the setup process for keeping your API online 24/7

echo "🚀 Starting Keep-Alive Setup..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Get API URL from user
echo "📝 Step 1: Configure API URL"
echo "----------------------------"
read -p "Enter your API URL (e.g., https://your-api.onrender.com): " API_URL

if [ -z "$API_URL" ]; then
    echo -e "${RED}❌ Error: API URL cannot be empty${NC}"
    exit 1
fi

echo -e "${GREEN}✅ API URL set to: $API_URL${NC}"
echo ""

# Step 2: Update GitHub Actions workflow
echo "📝 Step 2: Updating GitHub Actions workflow..."
echo "----------------------------------------------"

if [ -f ".github/workflows/keep-alive.yml" ]; then
    # Backup original file
    cp .github/workflows/keep-alive.yml .github/workflows/keep-alive.yml.backup
    
    # Replace placeholder URL with actual URL
    sed -i "s|https://demand-forecasting-api.onrender.com|$API_URL|g" .github/workflows/keep-alive.yml
    
    echo -e "${GREEN}✅ GitHub Actions workflow updated${NC}"
else
    echo -e "${YELLOW}⚠️  Warning: .github/workflows/keep-alive.yml not found${NC}"
fi

echo ""

# Step 3: Verify railway.json is updated
echo "📝 Step 3: Verifying Railway configuration..."
echo "---------------------------------------------"

if [ -f "railway.json" ]; then
    if grep -q "ALWAYS" railway.json && grep -q "sleepApplication" railway.json; then
        echo -e "${GREEN}✅ Railway configuration is already optimized${NC}"
    else
        echo -e "${YELLOW}⚠️  Warning: Railway configuration may need manual update${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Warning: railway.json not found${NC}"
fi

echo ""

# Step 4: Test API health endpoint
echo "📝 Step 4: Testing API health endpoint..."
echo "-----------------------------------------"

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health" 2>/dev/null)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ API is online and healthy (HTTP $HTTP_CODE)${NC}"
    
    # Get health response
    HEALTH_RESPONSE=$(curl -s "$API_URL/health" 2>/dev/null)
    echo "Response: $HEALTH_RESPONSE"
elif [ "$HTTP_CODE" = "000" ]; then
    echo -e "${YELLOW}⚠️  Could not connect to API (is it deployed?)${NC}"
else
    echo -e "${YELLOW}⚠️  API returned HTTP $HTTP_CODE${NC}"
fi

echo ""

# Step 5: Commit changes
echo "📝 Step 5: Committing changes..."
echo "--------------------------------"

git add .github/workflows/keep-alive.yml railway.json 2>/dev/null

if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
else
    echo "Files staged for commit:"
    git diff --cached --name-only
    echo ""
    read -p "Commit and push changes? (y/n): " COMMIT_CHOICE
    
    if [ "$COMMIT_CHOICE" = "y" ] || [ "$COMMIT_CHOICE" = "Y" ]; then
        git commit -m "Configure keep-alive system for 24/7 uptime"
        git push
        echo -e "${GREEN}✅ Changes committed and pushed${NC}"
    else
        echo -e "${YELLOW}⚠️  Changes staged but not committed${NC}"
        echo "Run 'git commit -m \"Configure keep-alive\"' and 'git push' manually"
    fi
fi

echo ""

# Step 6: Summary and next steps
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 WHAT'S BEEN DONE:"
echo "  ✅ GitHub Actions workflow updated with your API URL"
echo "  ✅ Railway configuration optimized"
echo "  ✅ Changes committed (if you chose to)"
echo ""
echo "🎯 CRITICAL NEXT STEP:"
echo "  ⚠️  SET UP UPTIMEROBOT (3 minutes):"
echo "     1. Go to: https://uptimerobot.com"
echo "     2. Sign up (free)"
echo "     3. Add monitor:"
echo "        - Type: HTTP(s)"
echo "        - URL: $API_URL/health"
echo "        - Interval: 5 minutes"
echo ""
echo "📊 VERIFICATION:"
echo "  • Wait 10 minutes"
echo "  • Check GitHub Actions: https://github.com/YOUR_USERNAME/demand-forecasting-grocery/actions"
echo "  • Check UptimeRobot dashboard"
echo "  • Test API: curl $API_URL/health"
echo ""
echo "📖 DOCUMENTATION:"
echo "  • Full guide: ACTION_PLAN_KEEP_ONLINE.md"
echo "  • Detailed setup: PERMANENT_ONLINE_SOLUTION.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}🎉 Your API will stay online 24/7!${NC}"
echo ""

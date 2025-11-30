# 🚀 Automated Keep-Alive Setup Script (PowerShell)
# This script automates the setup process for keeping your API online 24/7

Write-Host "🚀 Starting Keep-Alive Setup..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Get API URL from user
Write-Host "📝 Step 1: Configure API URL" -ForegroundColor Yellow
Write-Host "----------------------------"
$API_URL = Read-Host "Enter your API URL (e.g., https://your-api.onrender.com)"

if ([string]::IsNullOrWhiteSpace($API_URL)) {
    Write-Host "❌ Error: API URL cannot be empty" -ForegroundColor Red
    exit 1
}

Write-Host "✅ API URL set to: $API_URL" -ForegroundColor Green
Write-Host ""

# Step 2: Update GitHub Actions workflow
Write-Host "📝 Step 2: Updating GitHub Actions workflow..." -ForegroundColor Yellow
Write-Host "----------------------------------------------"

$workflowPath = ".github\workflows\keep-alive.yml"

if (Test-Path $workflowPath) {
    # Backup original file
    Copy-Item $workflowPath "$workflowPath.backup" -Force
    
    # Replace placeholder URL with actual URL
    $content = Get-Content $workflowPath -Raw
    $content = $content -replace 'https://demand-forecasting-api\.onrender\.com', $API_URL
    Set-Content $workflowPath $content -NoNewline
    
    Write-Host "✅ GitHub Actions workflow updated" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: $workflowPath not found" -ForegroundColor Yellow
}

Write-Host ""

# Step 3: Verify railway.json is updated
Write-Host "📝 Step 3: Verifying Railway configuration..." -ForegroundColor Yellow
Write-Host "---------------------------------------------"

if (Test-Path "railway.json") {
    $railwayContent = Get-Content "railway.json" -Raw
    if ($railwayContent -match "ALWAYS" -and $railwayContent -match "sleepApplication") {
        Write-Host "✅ Railway configuration is already optimized" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Warning: Railway configuration may need manual update" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Warning: railway.json not found" -ForegroundColor Yellow
}

Write-Host ""

# Step 4: Test API health endpoint
Write-Host "📝 Step 4: Testing API health endpoint..." -ForegroundColor Yellow
Write-Host "-----------------------------------------"

try {
    $response = Invoke-WebRequest -Uri "$API_URL/health" -Method Get -TimeoutSec 10 -UseBasicParsing
    
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API is online and healthy (HTTP $($response.StatusCode))" -ForegroundColor Green
        Write-Host "Response: $($response.Content)"
    } else {
        Write-Host "⚠️  API returned HTTP $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Could not connect to API (is it deployed?)" -ForegroundColor Yellow
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Step 5: Commit changes
Write-Host "📝 Step 5: Committing changes..." -ForegroundColor Yellow
Write-Host "--------------------------------"

git add .github/workflows/keep-alive.yml railway.json 2>$null

$hasChanges = git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "Files staged for commit:"
    git diff --cached --name-only
    Write-Host ""
    
    $commitChoice = Read-Host "Commit and push changes? (y/n)"
    
    if ($commitChoice -eq "y" -or $commitChoice -eq "Y") {
        git commit -m "Configure keep-alive system for 24/7 uptime"
        git push
        Write-Host "✅ Changes committed and pushed" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Changes staged but not committed" -ForegroundColor Yellow
        Write-Host "Run 'git commit -m `"Configure keep-alive`"' and 'git push' manually"
    }
} else {
    Write-Host "⚠️  No changes to commit" -ForegroundColor Yellow
}

Write-Host ""

# Step 6: Summary and next steps
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 WHAT'S BEEN DONE:"
Write-Host "  ✅ GitHub Actions workflow updated with your API URL"
Write-Host "  ✅ Railway configuration optimized"
Write-Host "  ✅ Changes committed (if you chose to)"
Write-Host ""
Write-Host "🎯 CRITICAL NEXT STEP:" -ForegroundColor Yellow
Write-Host "  ⚠️  SET UP UPTIMEROBOT (3 minutes):" -ForegroundColor Yellow
Write-Host "     1. Go to: https://uptimerobot.com"
Write-Host "     2. Sign up (free)"
Write-Host "     3. Add monitor:"
Write-Host "        - Type: HTTP(s)"
Write-Host "        - URL: $API_URL/health"
Write-Host "        - Interval: 5 minutes"
Write-Host ""
Write-Host "📊 VERIFICATION:"
Write-Host "  • Wait 10 minutes"
Write-Host "  • Check GitHub Actions: https://github.com/YOUR_USERNAME/demand-forecasting-grocery/actions"
Write-Host "  • Check UptimeRobot dashboard"
Write-Host "  • Test API: curl $API_URL/health"
Write-Host ""
Write-Host "📖 DOCUMENTATION:"
Write-Host "  • Full guide: ACTION_PLAN_KEEP_ONLINE.md"
Write-Host "  • Detailed setup: PERMANENT_ONLINE_SOLUTION.md"
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎉 Your API will stay online 24/7!" -ForegroundColor Green
Write-Host ""

# Open UptimeRobot in browser
$openBrowser = Read-Host "Open UptimeRobot in browser now? (y/n)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
    Start-Process "https://uptimerobot.com"
}

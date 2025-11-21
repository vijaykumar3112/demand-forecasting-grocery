# ============================================================================
# PROJECT CLEANUP SCRIPT
# ============================================================================

Write-Host "🧹 Starting Project Cleanup..." -ForegroundColor Cyan
Write-Host ""

# Create backup directory
$backupDir = "cleanup_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
Write-Host "✅ Created backup directory: $backupDir" -ForegroundColor Green

# ============================================================================
# PHASE 1: Remove Debug/Test Scripts from Root
# ============================================================================

Write-Host ""
Write-Host "📂 Phase 1: Removing debug and test scripts..." -ForegroundColor Yellow

$debugTestFiles = @(
    "check_features.py",
    "debug_import.py",
    "debug_predictor.py",
    "test_api.py",
    "test_api_debug.py",
    "test_api_detailed.py",
    "test_features.py",
    "test_predictor_direct.py",
    "test_setup.py",
    "test_simple.py",
    "tunnel.py"
)

foreach ($file in $debugTestFiles) {
    if (Test-Path $file) {
        Copy-Item $file -Destination "$backupDir\" -Force
        Remove-Item $file -Force
        Write-Host "  ❌ Removed: $file" -ForegroundColor Red
    }
}

# ============================================================================
# PHASE 2: Remove Temporary/Log Files
# ============================================================================

Write-Host ""
Write-Host "📂 Phase 2: Removing temporary and log files..." -ForegroundColor Yellow

$tempFiles = @(
    "error_log.txt",
    "feat_out.txt",
    "my_changes.txt"
)

foreach ($file in $tempFiles) {
    if (Test-Path $file) {
        Copy-Item $file -Destination "$backupDir\" -Force
        Remove-Item $file -Force
        Write-Host "  ❌ Removed: $file" -ForegroundColor Red
    }
}

# ============================================================================
# PHASE 3: Remove Backup Files
# ============================================================================

Write-Host ""
Write-Host "📂 Phase 3: Removing backup files..." -ForegroundColor Yellow

$backupFiles = @(
    "frontend\app.py.backup",
    "frontend\styles\theme.css.bak"
)

foreach ($file in $backupFiles) {
    if (Test-Path $file) {
        Copy-Item $file -Destination "$backupDir\" -Force
        Remove-Item $file -Force
        Write-Host "  ❌ Removed: $file" -ForegroundColor Red
    }
}

# ============================================================================
# PHASE 4: Remove Duplicate Directory
# ============================================================================

Write-Host ""
Write-Host "📂 Phase 4: Checking for duplicate directory..." -ForegroundColor Yellow

if (Test-Path "demand-forecasting-grocery") {
    Write-Host "  ⚠️  Found duplicate directory: demand-forecasting-grocery\" -ForegroundColor Magenta
    Write-Host "  ⚠️  This is a LARGE directory. Skipping backup..." -ForegroundColor Magenta
    
    $confirm = Read-Host "  Remove duplicate directory? (yes/no)"
    if ($confirm -eq "yes") {
        Remove-Item "demand-forecasting-grocery" -Recurse -Force
        Write-Host "  ❌ Removed: demand-forecasting-grocery\" -ForegroundColor Red
    } else {
        Write-Host "  ⏭️  Skipped: demand-forecasting-grocery\" -ForegroundColor Gray
    }
}

# ============================================================================
# PHASE 5: Remove Empty Directories
# ============================================================================

Write-Host ""
Write-Host "📂 Phase 5: Checking empty directories..." -ForegroundColor Yellow

$emptyDirs = @("deployment", "tests")

foreach ($dir in $emptyDirs) {
    if (Test-Path $dir) {
        $itemCount = (Get-ChildItem $dir -Force | Measure-Object).Count
        if ($itemCount -eq 0) {
            Remove-Item $dir -Force
            Write-Host "  ❌ Removed empty directory: $dir\" -ForegroundColor Red
        } else {
            Write-Host "  ⏭️  Skipped (not empty): $dir\" -ForegroundColor Gray
        }
    }
}

# ============================================================================
# PHASE 6: Remove Redundant Model Files
# ============================================================================

Write-Host ""
Write-Host "📂 Phase 6: Checking for redundant model files..." -ForegroundColor Yellow

if ((Test-Path "models\feature_names.pkl") -and (Test-Path "models\feature_names_correct.pkl")) {
    Write-Host "  ⚠️  Found duplicate: feature_names_correct.pkl" -ForegroundColor Magenta
    $confirm = Read-Host "  Remove models\feature_names_correct.pkl? (yes/no)"
    if ($confirm -eq "yes") {
        Copy-Item "models\feature_names_correct.pkl" -Destination "$backupDir\" -Force
        Remove-Item "models\feature_names_correct.pkl" -Force
        Write-Host "  ❌ Removed: models\feature_names_correct.pkl" -ForegroundColor Red
    }
}

# ============================================================================
# PHASE 7: Clean Python Cache
# ============================================================================

Write-Host ""
Write-Host "📂 Phase 7: Cleaning Python cache files..." -ForegroundColor Yellow

Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force
Get-ChildItem -Path . -Include *.pyo -Recurse -Force | Remove-Item -Force

Write-Host "  ✅ Cleaned all __pycache__ directories and .pyc files" -ForegroundColor Green

# ============================================================================
# SUMMARY
# ============================================================================

Write-Host ""
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host "✅ CLEANUP COMPLETE!" -ForegroundColor Green
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📦 Backup Location: $backupDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Review the changes with: git status" -ForegroundColor White
Write-Host "  2. Read PROJECT_CLEANUP_RECOMMENDATIONS.md for full action plan" -ForegroundColor White
Write-Host "  3. Commit the cleanup: git add . && git commit -m 'chore: project cleanup'" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Your project is now cleaner and more professional!" -ForegroundColor Green
Write-Host ""

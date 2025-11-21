@echo off
REM ============================================================================
REM PROJECT CLEANUP SCRIPT (Windows Batch)
REM ============================================================================

echo.
echo ============================================================
echo 🧹 Starting Project Cleanup...
echo ============================================================
echo.

REM Create backup directory
set BACKUP_DIR=cleanup_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_DIR=%BACKUP_DIR: =0%
mkdir "%BACKUP_DIR%" 2>nul
echo ✅ Created backup directory: %BACKUP_DIR%
echo.

REM ============================================================================
REM PHASE 1: Remove Debug/Test Scripts
REM ============================================================================

echo.
echo 📂 Phase 1: Removing debug and test scripts...
echo.

if exist "check_features.py" (
    copy "check_features.py" "%BACKUP_DIR%\" >nul 2>&1
    del "check_features.py"
    echo   ❌ Removed: check_features.py
)

if exist "debug_import.py" (
    copy "debug_import.py" "%BACKUP_DIR%\" >nul 2>&1
    del "debug_import.py"
    echo   ❌ Removed: debug_import.py
)

if exist "debug_predictor.py" (
    copy "debug_predictor.py" "%BACKUP_DIR%\" >nul 2>&1
    del "debug_predictor.py"
    echo   ❌ Removed: debug_predictor.py
)

if exist "test_api.py" (
    copy "test_api.py" "%BACKUP_DIR%\" >nul 2>&1
    del "test_api.py"
    echo   ❌ Removed: test_api.py
)

if exist "test_api_debug.py" (
    copy "test_api_debug.py" "%BACKUP_DIR%\" >nul 2>&1
    del "test_api_debug.py"
    echo   ❌ Removed: test_api_debug.py
)

if exist "test_api_detailed.py" (
    copy "test_api_detailed.py" "%BACKUP_DIR%\" >nul 2>&1
    del "test_api_detailed.py"
    echo   ❌ Removed: test_api_detailed.py
)

if exist "test_features.py" (
    copy "test_features.py" "%BACKUP_DIR%\" >nul 2>&1
    del "test_features.py"
    echo   ❌ Removed: test_features.py
)

if exist "test_predictor_direct.py" (
    copy "test_predictor_direct.py" "%BACKUP_DIR%\" >nul 2>&1
    del "test_predictor_direct.py"
    echo   ❌ Removed: test_predictor_direct.py
)

if exist "test_setup.py" (
    copy "test_setup.py" "%BACKUP_DIR%\" >nul 2>&1
    del "test_setup.py"
    echo   ❌ Removed: test_setup.py
)

if exist "test_simple.py" (
    copy "test_simple.py" "%BACKUP_DIR%\" >nul 2>&1
    del "test_simple.py"
    echo   ❌ Removed: test_simple.py
)

if exist "tunnel.py" (
    copy "tunnel.py" "%BACKUP_DIR%\" >nul 2>&1
    del "tunnel.py"
    echo   ❌ Removed: tunnel.py
)

REM ============================================================================
REM PHASE 2: Remove Temporary/Log Files
REM ============================================================================

echo.
echo 📂 Phase 2: Removing temporary and log files...
echo.

if exist "error_log.txt" (
    copy "error_log.txt" "%BACKUP_DIR%\" >nul 2>&1
    del "error_log.txt"
    echo   ❌ Removed: error_log.txt
)

if exist "feat_out.txt" (
    copy "feat_out.txt" "%BACKUP_DIR%\" >nul 2>&1
    del "feat_out.txt"
    echo   ❌ Removed: feat_out.txt
)

if exist "my_changes.txt" (
    copy "my_changes.txt" "%BACKUP_DIR%\" >nul 2>&1
    del "my_changes.txt"
    echo   ❌ Removed: my_changes.txt (1.1MB saved!)
)

REM ============================================================================
REM PHASE 3: Remove Backup Files
REM ============================================================================

echo.
echo 📂 Phase 3: Removing backup files...
echo.

if exist "frontend\app.py.backup" (
    copy "frontend\app.py.backup" "%BACKUP_DIR%\" >nul 2>&1
    del "frontend\app.py.backup"
    echo   ❌ Removed: frontend\app.py.backup
)

if exist "frontend\styles\theme.css.bak" (
    copy "frontend\styles\theme.css.bak" "%BACKUP_DIR%\" >nul 2>&1
    del "frontend\styles\theme.css.bak"
    echo   ❌ Removed: frontend\styles\theme.css.bak
)

REM ============================================================================
REM PHASE 4: Remove TODO.md (if issues are fixed)
REM ============================================================================

echo.
echo 📂 Phase 4: Checking TODO.md...
echo.

if exist "TODO.md" (
    echo   ⚠️  Found TODO.md - Review and delete manually if all issues are fixed
)

REM ============================================================================
REM PHASE 5: Clean Python Cache
REM ============================================================================

echo.
echo 📂 Phase 5: Cleaning Python cache files...
echo.

for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc >nul 2>&1
del /s /q *.pyo >nul 2>&1

echo   ✅ Cleaned all __pycache__ directories and .pyc files

REM ============================================================================
REM SUMMARY
REM ============================================================================

echo.
echo =============================================================
echo ✅ CLEANUP COMPLETE!
echo =============================================================
echo.
echo 📦 Backup Location: %BACKUP_DIR%
echo.
echo Next Steps:
echo   1. Review the changes with: git status
echo   2. Read PROJECT_CLEANUP_RECOMMENDATIONS.md for full action plan
echo   3. Commit the cleanup: git add . ^&^& git commit -m "chore: project cleanup"
echo.
echo 🚀 Your project is now cleaner and more professional!
echo.
echo NOTE: The duplicate 'demand-forecasting-grocery' directory was NOT removed.
echo       Delete it manually if needed: rmdir /s demand-forecasting-grocery
echo.

pause

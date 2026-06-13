@echo off
title Roller Compaction Study
echo ========================================
echo   Roller Compaction Parametric Study
echo ========================================
echo.
echo Checking environment...

REM Try to find Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

REM Install dependencies if missing
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install streamlit numpy pandas matplotlib
)

echo Starting application...
echo.
echo A browser window will open shortly.
echo Close the browser to exit.

start "" http://localhost:8501
python -m streamlit run roller_app.py --server.headless true --server.port 8501 --browser.gatherUsageStats false

pause

@echo off
echo ========================================
echo    CIT LOSS PREDICTION SYSTEM
echo ========================================
echo.

REM Check if running in conda environment
where conda >nul 2>&1
if errorlevel 1 (
    echo WARNING: Conda not found in PATH
    echo.
    echo Please run this from your Anaconda Prompt or
    echo activate your environment first.
    echo.
    echo For Anaconda users:
    echo 1. Open Anaconda Prompt
    echo 2. Navigate to this folder
    echo 3. Run: python app.py
    echo.
    pause
    exit /b 1
)

echo Checking dependencies...
pip install -r requirements_simple.txt

echo.
echo ========================================
echo STARTING CIT SYSTEM...
echo ========================================
echo.
echo Open your browser and visit:
echo     http://localhost:5000
echo.
echo To stop, press: Ctrl+C
echo.
echo ========================================
python app.py
pause

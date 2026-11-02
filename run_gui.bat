@echo off
title Sign Language App - Loading...
cd /d "%~dp0"
echo ============================================
echo  Sign Language To Text and Speech Conversion
echo ============================================
echo.
echo  [Step 1] Checking Python environment...
if not exist ".\.venv\Scripts\python.exe" (
    echo  ERROR: Virtual environment not found!
    echo  Please make sure .venv folder exists.
    pause
    exit /b 1
)
echo  [Step 1] OK - Python found

echo  [Step 2] Checking model file...
if not exist "cnn8grps_rad1_model.h5" (
    echo  ERROR: Model file not found!
    pause
    exit /b 1
)
echo  [Step 2] OK - Model found

echo.
echo  [Step 3] Starting application...
echo  *** PLEASE WAIT 20-30 SECONDS for the window to appear ***
echo  *** Do NOT close this window while app is running ***
echo.

.\.venv\Scripts\python.exe final_pred.py

echo.
if %errorlevel% neq 0 (
    echo  !! App crashed with error code: %errorlevel%
    echo  Scroll up to read the error message.
) else (
    echo  App closed normally.
)
echo.
pause

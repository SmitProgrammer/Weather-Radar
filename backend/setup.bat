@echo off
echo ========================================
echo Weather Radar Backend Setup
echo ========================================
echo.

REM Check if in correct directory
if not exist "app.py" (
    echo ERROR: app.py not found!
    echo Please run this script from the backend directory
    pause
    exit /b 1
)

echo Step 1: Creating Python virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python 3.9+ is installed: python --version
    pause
    exit /b 1
)
echo   [OK] Virtual environment created

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo   [OK] Virtual environment activated

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo   [OK] pip upgraded

echo.
echo Step 4: Installing dependencies...
echo   This may take a few minutes...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo WARNING: Some packages may have failed to install
    echo.
    echo Common issue: cfgrib/eccodes on Windows
    echo Solution: Use Docker instead (see QUICKSTART.md)
    echo.
    echo Docker command:
    echo   docker build -t weather-radar-backend .
    echo   docker run -p 5000:5000 weather-radar-backend
    echo.
    pause
    exit /b 1
)
echo   [OK] Dependencies installed

echo.
echo Step 5: Creating cache directory...
if not exist "cache" (
    mkdir cache
)
echo   [OK] Cache directory ready

echo.
echo Step 6: Creating .env file...
if not exist ".env" (
    copy .env.example .env
    echo   [OK] .env file created from template
) else (
    echo   [OK] .env file already exists
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Test MRMS connectivity:
echo    python test_mrms.py
echo.
echo 2. Start the server:
echo    python app.py
echo.
echo 3. Backend will be available at:
echo    http://localhost:5000
echo.
echo Note: If you encountered errors installing cfgrib/eccodes,
echo       use Docker instead (see QUICKSTART.md)
echo.
pause

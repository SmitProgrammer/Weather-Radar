@echo off
echo ========================================
echo Weather Radar Backend Server
echo ========================================
echo.

REM Check if in correct directory
if not exist "app.py" (
    echo ERROR: app.py not found!
    echo Please run this script from the backend directory
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found!
    echo.
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python 3.9+ is installed
        pause
        exit /b 1
    )
    
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    
    echo Installing dependencies...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo WARNING: Some dependencies may have failed to install
        echo If eccodes/cfgrib failed, consider using Docker instead
        echo See QUICKSTART.md for details
        pause
    )
)

REM Create cache directory if it doesn't exist
if not exist "cache" (
    echo Creating cache directory...
    mkdir cache
)

echo.
echo Starting Flask server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause

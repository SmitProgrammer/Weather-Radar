@echo off
echo ========================================
echo Weather Radar Frontend Setup
echo ========================================
echo.

REM Check if in correct directory
if not exist "package.json" (
    echo ERROR: package.json not found!
    echo Please run this script from the frontend directory
    pause
    exit /b 1
)


echo Checking Node.js installation...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed!
    echo Please download and install from: https://nodejs.org/
    pause
    exit /b 1
)

node --version
echo   [OK] Node.js is installed

echo.
echo Installing dependencies...
echo This may take a few minutes...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo   [OK] Dependencies installed

echo.
echo Creating .env file...
if not exist ".env" (
    copy .env.example .env
    echo   [OK] .env file created from template
    echo.
    echo IMPORTANT: Update REACT_APP_API_URL in .env if needed
    echo   Default: http://localhost:5000/api
) else (
    echo   [OK] .env file already exists
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure backend is running on port 5000
echo.
echo 2. Start the frontend:
echo    npm start
echo.
echo 3. Open browser to:
echo    http://localhost:3000
echo.
pause

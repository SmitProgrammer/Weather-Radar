@echo off
echo ========================================
echo Weather Radar Frontend
echo ========================================
echo.

REM Check if in correct directory
if not exist "package.json" (
    echo ERROR: package.json not found!
    echo Please run this script from the frontend directory
    pause
    exit /b 1
)

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Make sure Node.js and npm are installed
        pause
        exit /b 1
    )
)

echo.
echo Starting React development server...
echo Frontend will be available at: http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

npm start

pause

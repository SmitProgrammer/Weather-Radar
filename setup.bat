@echo off
echo ========================================
echo Weather Radar - Complete Setup
echo ========================================
echo.
echo This script will set up both backend and frontend
echo.
pause

echo.
echo ========================================
echo Setting up BACKEND...
echo ========================================
cd backend
call setup.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Backend setup encountered errors.
    echo Please check the messages above.
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo Setting up FRONTEND...
echo ========================================
cd frontend
call setup.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Frontend setup encountered errors.
    echo Please check the messages above.
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo Setup Complete for Both Components!
echo ========================================
echo.
echo To start the application:
echo.
echo 1. Start backend (in one terminal):
echo    cd backend
echo    start.bat
echo.
echo 2. Start frontend (in another terminal):
echo    cd frontend  
echo    start.bat
echo.
echo 3. Open browser to: http://localhost:3000
echo.
echo See QUICKSTART.md for more details
echo.
pause

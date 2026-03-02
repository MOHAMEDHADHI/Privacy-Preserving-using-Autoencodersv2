@echo off
echo ========================================
echo Privacy-Preserving ML Dashboard
echo ========================================
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "python backend/main.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend Dashboard...
cd frontend
start "Frontend Dashboard" cmd /k "npm start"

echo.
echo ========================================
echo Dashboard Starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to stop all servers...
pause >nul

taskkill /FI "WINDOWTITLE eq Backend Server*" /T /F
taskkill /FI "WINDOWTITLE eq Frontend Dashboard*" /T /F

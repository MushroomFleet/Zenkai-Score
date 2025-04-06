@echo off
echo ===================================
echo       Zenkai-Score Launcher
echo ===================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Running Zenkai-Score...
python test.py
echo.

echo ===================================
echo       Zenkai-Score Complete
echo ===================================
echo.
pause

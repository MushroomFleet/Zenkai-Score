@echo off
echo ===================================
echo       Zenkai-Score Launcher
echo ===================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Running Zenkai-Score...
python -m zenkai_score %*
echo.

echo ===================================
echo       Zenkai-Score Complete
echo ===================================
echo.
pause

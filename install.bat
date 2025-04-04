@echo off
echo ===================================
echo    Zenkai-Score Setup Installer
echo ===================================
echo.

echo Creating virtual environment...
python -m venv venv
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Running first-time setup to download model weights...
python -m zenkai_score --setup
echo.

echo ===================================
echo Setup complete! You can now run Zenkai-Score.bat to start the program.
echo ===================================
echo.
pause
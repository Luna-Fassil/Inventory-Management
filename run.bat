@echo off
echo ==========================================
echo Running the Inventory System...
echo ==========================================

:: Step 1: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate


:: Step 2: Start the Flask application
echo Starting Flask server...
python inventory.py

:: Keep the terminal open
echo ==========================================
echo Server is running! Open http://127.0.0.1:5000/ in your browser.
echo Press CTRL+C to stop the server.
echo ==========================================
pause

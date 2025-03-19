@echo off
echo ==========================================
echo Setting up the Inventory System...
echo ==========================================

:: Step 1: Create a virtual environment
echo Creating virtual environment...
python -m venv venv

:: Step 2: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Step 3: Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

:: Step 4: Build complete message
echo ==========================================
echo Build Complete! Run 'run.bat' to start the application.
echo ==========================================
pause

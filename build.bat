@echo off
echo ==========================================
echo Cleaning up old build files...
echo ==========================================

:: Step 1: Remove old virtual environment if it exists
if exist venv (
    echo Deleting existing virtual environment...
    rmdir /s /q venv
)

:: Step 2: Remove any __pycache__ directories
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

:: Step 3: Set up a new virtual environment
echo ==========================================
echo Setting up the Inventory System...
echo ==========================================
python -m venv venv

:: Step 4: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Step 5: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo ==========================================
echo Build Complete! Run 'run.bat' to start the application.
echo ==========================================
pause


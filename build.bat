@echo off
echo Setting up the Inventory System...
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
echo Build Complete. Run `run.bat` to start the app.
pause

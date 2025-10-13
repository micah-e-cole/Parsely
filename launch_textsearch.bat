@echo off
cd /d "%~dp0"
echo Launching TextSearch with local virtual environment...
"%~dp0.venv\Scripts\python.exe" "%~dp0run.py"
pause
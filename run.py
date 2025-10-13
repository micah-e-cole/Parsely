"""
run.py — Entry launcher for TextSearch
Safely runs gui.pyw (creates venv and installs dependencies if missing)
"""

import os
import sys
import subprocess
import venv

# Path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, ".venv")
PYTHON_EXE = os.path.join(VENV_DIR, "Scripts", "python.exe") if os.name == "nt" else os.path.join(VENV_DIR, "bin", "python")
GUI_SCRIPT = os.path.join(BASE_DIR, "main\gui.pyw")

# --- Step 1: Create virtual environment if missing ---
if not os.path.exists(VENV_DIR):
    print("Creating local virtual environment...")
    venv.create(VENV_DIR, with_pip=True)

# --- Step 2: Ensure dependencies are installed ---
# Optional: specify your dependencies inline OR read from requirements.txt
if os.path.exists(os.path.join(BASE_DIR, "requirements.txt")):
    subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", "-r", "requirements.txt"])

# --- Step 3: Launch gui.pyw inside the venv ---
print("Launching TextSearch...")
os.execv(PYTHON_EXE, [PYTHON_EXE, GUI_SCRIPT])
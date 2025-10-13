"""
run.py — Entry launcher for Parsely
Safely runs gui.pyw (creates venv and installs dependencies if missing),
with a loading splash screen.
"""

import os
import sys
import subprocess
import venv
import threading
import time
from main.splash import show_splash_then


# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, ".venv")
PYTHON_EXE = (
    os.path.join(VENV_DIR, "Scripts", "python.exe")
    if os.name == "nt"
    else os.path.join(VENV_DIR, "bin", "python")
)
GUI_SCRIPT = os.path.join(BASE_DIR, "main", "gui.pyw")
REQUIREMENTS_FILE = os.path.join(BASE_DIR, "requirements.txt")

sys.path.append(os.path.join(BASE_DIR, "main"))


# -----------------------------------------------------
# Helper: ensure environment and dependencies
# -----------------------------------------------------
def setup_environment():
    """Creates venv and installs dependencies if missing."""
    if not os.path.exists(VENV_DIR):
        print("Creating local virtual environment...")
        venv.create(VENV_DIR, with_pip=True)

    # Ensure pip itself is up to date
    subprocess.run([PYTHON_EXE, "-m", "pip", "install", "--upgrade", "pip"], check=False)

    if os.path.exists(REQUIREMENTS_FILE):
        print("Installing dependencies...")
        subprocess.run([PYTHON_EXE, "-m", "pip", "install", "-r", REQUIREMENTS_FILE], check=False)

    time.sleep(1)  # Small delay for visual smoothness


# -----------------------------------------------------
# Main launcher logic
# -----------------------------------------------------
def launch_gui():
    """Launch GUI once environment is ready."""
    print("Launching Parsely GUI...")
    os.execv(PYTHON_EXE, [PYTHON_EXE, GUI_SCRIPT])


if __name__ == "__main__":
    # Run environment setup in background while splash screen shows
    setup_thread = threading.Thread(target=setup_environment)
    setup_thread.start()

    # Show splash screen while setup runs, then launch GUI
    show_splash_then(launch_gui, duration=60)

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
VENV = ROOT / ".venv"
REQ = ROOT / "requirements.txt"
ENTRY = ROOT / "main_entry.py"

def run(cmd):
    subprocess.check_call(cmd)

def venv_python():
    if os.name == "nt":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"

def ensure_venv():
    if not VENV.exists():
        print("Creating virtual environment...")
        run([sys.executable, "-m", "venv", str(VENV)])

def install_deps():
    print("Installing dependencies...")
    run([str(venv_python()), "-m", "pip", "install", "--upgrade", "pip"])
    run([str(venv_python()), "-m", "pip", "install", "-r", str(REQ)])

def launch():
    run([str(venv_python()), str(ENTRY)])

if __name__ == "__main__":
    ensure_venv()
    install_deps()
    launch()

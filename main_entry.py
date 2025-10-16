"""
main_entry.py — PyInstaller entry point for Parsely
"""

from main.gui import launch_gui
from main.splash import show_splash_then

if __name__ == "__main__":
    show_splash_then(launch_gui, duration=30)

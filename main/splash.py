# splash.py
"""
Cross-platform splash screen for Parsely.
Runs safely on macOS (Tkinter only on main thread).
"""

import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk


class SplashScreen(ttk.Window):
    def __init__(self, duration=3):
        super().__init__(themename="darkly")
        self.title("Loading Parsely...")
        self.geometry("500x300")
        self.resizable(False, False)

        # Center on screen
        try:
            self.eval('tk::PlaceWindow . center')
        except Exception:
            pass  # In case window manager doesn't support centering

        # --- Load image robustly ---
        self.logo = None
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "assets", "parsely.png")

            if not os.path.exists(image_path):
                image_path = os.path.join(os.getcwd(), "main", "assets", "parsely.png")

            print(f"[Splash] Loading image from: {image_path}")

            img = Image.open(image_path).resize((100, 100))
            self.logo = ImageTk.PhotoImage(img)
            ttk.Label(self, image=self.logo).pack(pady=(30, 10))
        except Exception as e:
            ttk.Label(self, text=f"Image load failed:\n{e}", font=("Roboto", 10)).pack(pady=40)

        # Title and progress
        ttk.Label(
            self,
            text="Loading Parsely...",
            font=("Roboto", 16, "bold"),
            anchor="center"
        ).pack(pady=10)

        pb = ttk.Progressbar(self, mode="indeterminate", bootstyle="success-striped")
        pb.pack(fill=X, padx=50, pady=10)
        pb.start(10)

        self.pb = pb


def show_splash_then(callback, wait_thread=None, duration=30):
    """
    Displays splash screen while `wait_thread` runs in background.
    When the thread finishes or duration expires, splash closes and callback runs.
    - callback: function to run after splash closes
    - wait_thread: optional background thread to monitor
    - duration: max time (seconds) to keep splash open
    """
    app = SplashScreen(duration)

    def check_done():
        # Called periodically from main thread
        if wait_thread and not wait_thread.is_alive():
            app.destroy()
            callback()
        else:
            app.after(100, check_done)

    # Safety timeout in case of setup hang
    app.after(int(duration * 1000), lambda: (app.destroy(), callback()))
    app.after(100, check_done)

    app.mainloop()
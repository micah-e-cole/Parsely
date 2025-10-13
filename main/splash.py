# splash.py
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import threading

print("[DEBUG] cwd =", os.getcwd())
print("[DEBUG] file =", os.path.abspath(__file__))

class SplashScreen(ttk.Window):
    def __init__(self, duration=3):
        super().__init__(themename="darkly")
        self.title("Loading Parsely...")
        self.geometry("500x300")
        self.resizable(False, False)

        # Center on screen
        self.eval('tk::PlaceWindow . center')

        # --- Determine image path robustly ---
        try:
            # Resolve path relative to *this script’s* directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "assets", "parsely.png")

            # As a fallback, check if being launched from project root (e.g., run.py)
            if not os.path.exists(image_path):
                image_path = os.path.join(os.getcwd(), "main", "assets", "parsely.png")

            # Debugging (optional): print to verify
            print(f"[Splash] Loading image from: {image_path}")

            img = Image.open(image_path)
            img = img.resize((100, 100))
            self.logo = ImageTk.PhotoImage(img)
            ttk.Label(self, image=self.logo).pack(pady=(30, 10))
        except Exception as e:
            ttk.Label(self, text=f"Image load failed:\n{e}", font=("Roboto", 10)).pack(pady=40)

        ttk.Label(
            self,
            text="Loading Parsely...",
            font=("Roboto", 16, "bold"),
            anchor="center"
        ).pack(pady=10)

        pb = ttk.Progressbar(self, mode="indeterminate", bootstyle="success-striped")
        pb.pack(fill=X, padx=50, pady=10)
        pb.start(10)

        # Auto-close after duration seconds
        self.after(duration * 40, self.destroy)


def show_splash_then(main_func, duration=3):
    """Show splash, then launch main GUI."""
    def run():
        splash = SplashScreen(duration)
        splash.mainloop()
        main_func()

    threading.Thread(target=run).start()

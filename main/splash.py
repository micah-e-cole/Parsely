# splash.py
"""
Cross-platform splash screen for Parsely.
Uses Tk root (not ttkbootstrap) for maximum compatibility.
Main GUI applies ttkbootstrap theming after splash.
"""

from tkinter import ttk as tk_ttk
from queue import Empty
import sys
import ttkbootstrap as ttk
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk


def _resource_path(filename):
    """
    Normalize asset path for normal runs and PyInstaller bundles.
    """
    if getattr(sys, "frozen", False):
        # Running inside a PyInstaller bundle
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent

    return base / "assets" / filename


def show_splash_then(callback, wait_thread=None, progress_queue=None, duration=3):
    """
    Displays a splash using a Toplevel window.
    Creates ONE Tk root, keeps it hidden,
    and then calls callback(root) after splash closes.

    progress_queue (optional):
        queue.Queue emitting tuples:
        ("status", "Text to show")
        ("progress", int 0–100)
    """

    # -------------------------------------
    # Create main Tk root (hidden)
    # -------------------------------------
    root = tk.Tk()
    root.withdraw()
    
    from ttkbootstrap import Style

    style = Style("darkly")
    # -------------------------------------
    # Create splash
    # -------------------------------------
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.configure(bg="#1e1e1e")

    w, h = 500, 300
    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    x = int((sw - w) // 2)
    y = int((sh - h) // 2)
    splash.geometry(f"{w}x{h}+{x}+{y}")

    # -------------------------------------
    # Load splash image
    # -------------------------------------
    try:
        img_path = _resource_path("parsely.png")
        if not getattr(sys, "frozen", False):
            print(f"[Splash] Loading image from: {img_path}")

        img = Image.open(img_path).resize((110, 110))
        logo = ImageTk.PhotoImage(img)

        lbl = tk.Label(splash, image=logo, bg="#1e1e1e")
        lbl.image = logo
        lbl.pack(pady=25)

    except Exception as e:
        tk.Label(
            splash,
            text=f"Image load failed:\n{e}",
            bg="#1e1e1e",
            fg="white",
            font=("Segoe UI", 12),
        ).pack(pady=40)

    # -------------------------------------
    # Title text
    # -------------------------------------
    tk.Label(
        splash,
        text="Loading Parsely...",
        bg="#1e1e1e",
        fg="white",
        font=("Segoe UI", 16, "bold"),
    ).pack(pady=(10, 5))

    # -------------------------------------
    # Status text (dynamic)
    # -------------------------------------
    status_var = tk.StringVar(value="Starting...")
    status_label = tk.Label(
        splash,
        textvariable=status_var,
        bg="#1e1e1e",
        fg="#cccccc",
        font=("Segoe UI", 11),
    )
    status_label.pack(pady=(5, 5))

    # -------------------------------------
    # Progress bar
    # -------------------------------------
    progress = tk_ttk.Progressbar(
        splash,
        orient="horizontal",
        length=320,
        mode="determinate",
        maximum=100,
    )
    progress.pack(pady=(5, 15))

    # -------------------------------------
    # Finishing logic
    # -------------------------------------
    finished = False

    def finish():
        nonlocal finished
        if finished:
            return
        finished = True

        try:
            splash.destroy()
        except:
            pass

        root.deiconify()
        callback(root)

    # -------------------------------------
    # Poll progress queue (UI-safe)
    # -------------------------------------
    def poll_progress():
        if progress_queue is not None:
            try:
                while True:
                    kind, value = progress_queue.get_nowait()

                    if kind == "status":
                        status_var.set(value)
                    elif kind == "progress":
                        progress["value"] = value

            except Empty:
                pass

        splash.after(100, poll_progress)

    poll_progress()

    # -------------------------------------
    # Exit conditions (Improvement #3)
    # -------------------------------------
    def check_done():
        if wait_thread and not wait_thread.is_alive():
            finish()
        else:
            splash.after(100, check_done)

    if wait_thread:
        splash.after(100, check_done)
    else:
        splash.after(int(duration * 1000), finish)

    # -------------------------------------
    # Tk mainloop
    # -------------------------------------
    root.mainloop()

    # -------------------------------------
    # Finishing logic
    # -------------------------------------
    finished = False

    def finish():
        nonlocal finished
        if finished:
            return
        finished = True

        try:
            splash.destroy()
        except:
            pass

        root.deiconify()
        callback(root)

    def check_done():
        if wait_thread and not wait_thread.is_alive():
            finish()
        else:
            splash.after(100, check_done)

    if wait_thread:
        splash.after(100, check_done)
    else:
        splash.after(int(duration * 1000), finish)

    # -------------------------------------
    # Tk mainloop
    # -------------------------------------
    root.mainloop()

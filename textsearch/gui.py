# gui.py
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import tkinter.font as tkFont
import threading
import re
from pathlib import Path
from search import run as search_run


class TextSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TextSearch")
        self.root.geometry("900x600")
        self.root.minsize(700, 400)
        self.root.resizable(True, True)

        # Configure grid layout for resizing
        for i in range(6):
            self.root.rowconfigure(i, weight=0)
        self.root.rowconfigure(4, weight=1)
        self.root.columnconfigure(1, weight=1)

        # --- Search Term ---
        tk.Label(root, text="Search Term:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.search_var = tk.StringVar()
        self.entry_pattern = tk.Entry(root, textvariable=self.search_var)
        self.entry_pattern.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- Search Mode (File or Directory) ---
        self.mode_var = tk.StringVar(value="directory")
        frame_mode = tk.Frame(root)
        frame_mode.grid(row=1, column=0, columnspan=3, sticky="w", padx=10)
        tk.Radiobutton(frame_mode, text="Search Directory", variable=self.mode_var, value="directory").pack(side="left")
        tk.Radiobutton(frame_mode, text="Search Single File", variable=self.mode_var, value="file").pack(side="left")

        # --- Path Selection ---
        tk.Label(root, text="Path:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.path_var = tk.StringVar()
        self.entry_path = tk.Entry(root, textvariable=self.path_var)
        self.entry_path.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(root, text="Browse", command=self.browse_path).grid(row=2, column=2, padx=5, pady=10, sticky="e")

        # --- Extension Filter ---
        tk.Label(root, text="Extension Filter:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.ext_var = tk.StringVar()
        ttk.Combobox(root, textvariable=self.ext_var, values=["", ".txt", ".log", ".csv", ".py"], width=10).grid(
            row=3, column=1, padx=10, pady=5, sticky="w"
        )

        # --- Output Box ---
        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.output.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # --- Search Button ---
        tk.Button(root, text="Search", command=self.run_search).grid(row=5, column=1, pady=10)

        # --- Monospace font for alignment ---
        font_mono = tkFont.Font(family="Consolas", size=10)
        self.output.configure(font=font_mono)

        # --- Dark theme ---
        self.output.configure(bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff")

        # --- Text styles ---
        self.output.tag_configure("match", foreground="#ff0000", background="#222222")   # yellow highlight
        self.output.tag_configure("index", foreground="#8b0097")                         # light blue index
        self.output.tag_configure("linenum", foreground="#2bff00")                       # dim gray line numbers
        self.output.tag_configure("info", foreground="#FFFFFF")                          # for headers & totals

    # -------------------------------
    #  Utility Methods
    # -------------------------------

    def browse_path(self):
        """Open file or directory picker."""
        mode = self.mode_var.get()
        chosen = filedialog.askopenfilename() if mode == "file" else filedialog.askdirectory()
        if chosen:
            self.path_var.set(chosen)

    def run_search(self):
        """Run search in background thread."""
        pattern = self.search_var.get().strip()
        target = self.path_var.get().strip()
        ext = self.ext_var.get().strip()

        if not pattern:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return
        if not target:
            messagebox.showwarning("Input Error", "Please select a directory or file.")
            return

        # Clear previous results
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Searching for '{pattern}' in {target}\n\n", "info")

        threading.Thread(target=self.perform_search, args=(pattern, target, ext), daemon=True).start()

    def perform_search(self, pattern, target, ext):
        """Perform search and show aligned, colorized output."""
        regex = re.compile(pattern, re.IGNORECASE)
        results = search_run(pattern, target, ignore_case=True, extension=ext)

        found = False
        index = 1

        for result in results:
            found = True
            try:
                # split line: "47 some text"
                line_number, line_rest = result.split(" ", 1)
            except ValueError:
                line_number, line_rest = "?", result

            # --- Aligned column formatting ---
            self.output.insert(tk.END, f"[{index:03}] (line {int(line_number):>4})  ", "linenum")

            # --- Highlight matches ---
            start_idx = 0
            for match in regex.finditer(line_rest):
                mstart, mend = match.span()
                self.output.insert(tk.END, line_rest[start_idx:mstart])
                self.output.insert(tk.END, line_rest[mstart:mend], "match")
                start_idx = mend
            self.output.insert(tk.END, line_rest[start_idx:] + "\n")

            index += 1

        if not found:
            self.output.insert(tk.END, "\nNo matches found.\n", "info")
        else:
            self.output.insert(tk.END, f"\nTotal results: {index - 1}\n", "info")


if __name__ == "__main__":
    root = tk.Tk()
    app = TextSearchGUI(root)
    root.mainloop()

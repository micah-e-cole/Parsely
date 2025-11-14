import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog, scrolledtext
import tkinter.font as tkFont
import threading, re, openpyxl
from main.search import run as search_run


class TextSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Parsely")
        self.root.geometry("1000x650")
        self.root.minsize(850, 450)
        self.root.resizable(True, True)

        # Force ttkbootstrap to apply its styles correctly on macOS
        style = ttk.Style(theme='darkly')
        self.root.style = style

        # Configure overall theme colors and font
        self.font_base = tkFont.Font(family="Segoe UI", size=10)

        # Grid layout setup
        for i in range(8):
            self.root.rowconfigure(i, weight=0)
        self.root.rowconfigure(7, weight=1)
        self.root.columnconfigure(1, weight=1)

        # --- Search Term 1 (required) ---
        ttk.Label(root, text="Search Term 1 *:", font=self.font_base).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        self.search_var1 = ttk.StringVar()
        self.entry_pattern1 = ttk.Entry(root, textvariable=self.search_var1, width=20)
        self.entry_pattern1.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- Search Term 2 (optional) ---
        ttk.Label(root, text="Search Term 2 (optional):", font=self.font_base).grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )
        self.search_var2 = ttk.StringVar()
        self.entry_pattern2 = ttk.Entry(root, textvariable=self.search_var2, width=20)
        self.entry_pattern2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # --- Target Type (File or Folder) ---
        ttk.Label(root, text="Search Target *:", font=self.font_base).grid(
            row=2, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.target_type = ttk.StringVar(value="file")
        frame_target = ttk.Frame(root)
        frame_target.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="w")

        ttk.Radiobutton(
            frame_target,
            text="File",
            variable=self.target_type,
            value="file",
            bootstyle="secondary",
            command=self.update_filter_visibility
        ).pack(side="left", padx=(0, 10))

        ttk.Radiobutton(
            frame_target,
            text="Folder",
            variable=self.target_type,
            value="folder",
            bootstyle="secondary",
            command=self.update_filter_visibility
        ).pack(side="left")

        # --- Path Selection (always visible) ---
        ttk.Label(root, text="Path *:", font=self.font_base).grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.path_var = ttk.StringVar()
        self.entry_path = ttk.Entry(root, textvariable=self.path_var, width=40)
        self.entry_path.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ttk.Button(
            root, text="Browse", command=self.browse_path, bootstyle="info-outline"
        ).grid(row=3, column=2, padx=5, pady=5, sticky="e")

        # --- Extension Filter (only for File) ---
        self.ext_label = ttk.Label(root, text="Extension Filter:", font=self.font_base)
        self.ext_var = ttk.StringVar()
        self.ext_combo = ttk.Combobox(
            root,
            textvariable=self.ext_var,
            values=["", ".csv", ".docx", ".log", ".pdf", ".txt", ".xlsx"],
            width=10,
            bootstyle="dark"
        )
        self.ext_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.ext_combo.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # --- Search Button ---
        ttk.Button(
            root,
            text="Search",
            command=self.run_search,
            bootstyle="success-outline"
        ).grid(row=0, column=2, padx=10, pady=(10, 0), sticky="e")

        # --- Output Frames for Each Search ---
        frame_output = ttk.Frame(root, padding=10, bootstyle="dark")
        frame_output.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        frame_output.columnconfigure(0, weight=1)
        frame_output.columnconfigure(1, weight=1)
        frame_output.rowconfigure(0, weight=1)

        # Output box for term 1
        self.output1 = scrolledtext.ScrolledText(
            frame_output, wrap="word", bg="#101010", fg="#e8e8e8", insertbackground="white"
        )
        self.output1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Output box for term 2 (optional)
        self.output2 = scrolledtext.ScrolledText(
            frame_output, wrap="word", bg="#101010", fg="#e8e8e8", insertbackground="white"
        )
        self.output2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # --- Tag styles for highlighting ---
        font_mono = tkFont.Font(family="Consolas", size=10)
        for output in (self.output1, self.output2):
            output.configure(font=font_mono)
            output.tag_configure("match", foreground="#00FFAA", background="#003333")
            output.tag_configure("linenum", foreground="#FFA500")
            output.tag_configure("info", foreground="#DDDDDD")

        # Initialize visibility state
        self.update_filter_visibility()

    # -------------------------------
    #  Utility Methods
    # -------------------------------

    def update_filter_visibility(self):
        """Show Extension Filter only when 'File' is selected."""
        if self.target_type.get() == "file":
            self.ext_label.grid()
            self.ext_combo.grid()
        else:
            self.ext_label.grid_remove()
            self.ext_combo.grid_remove()

    def browse_path(self):
        """Open a file or folder picker depending on user selection."""
        if self.target_type.get() == "folder":
            chosen = filedialog.askdirectory(title="Select a folder to search")
        else:
            chosen = filedialog.askopenfilename(title="Select a file to search")

        if chosen:
            self.path_var.set(chosen)

    def run_search(self):
        """Run one or two searches in background threads."""
        pattern1 = self.search_var1.get().strip()
        pattern2 = self.search_var2.get().strip()
        target = self.path_var.get().strip()
        ext = self.ext_var.get().strip()

        # Validation
        if not pattern1:
            Messagebox.show_warning("Please enter at least the first search term.", "Input Error")
            return
        if not target:
            Messagebox.show_warning("Please select a file or folder.", "Input Error")
            return

        # Clear previous results
        self.output1.delete(1.0, "end")
        self.output2.delete(1.0, "end")

        # Always run first term
        self.output1.insert("end", f"🔍 Searching for '{pattern1}' in {target}\n\n", "info")
        threading.Thread(
            target=self.perform_search, args=(pattern1, target, ext, self.output1), daemon=True
        ).start()

        # Run second term only if provided
        if pattern2:
            self.output2.insert("end", f"🔍 Searching for '{pattern2}' in {target}\n\n", "info")
            threading.Thread(
                target=self.perform_search, args=(pattern2, target, ext, self.output2), daemon=True
            ).start()
        else:
            self.output2.insert("end", "No second term provided.\n", "info")

    def perform_search(self, pattern, target, ext, output_widget):
        """Perform search and show aligned, colorized output with match counts."""
        regex = re.compile(pattern, re.IGNORECASE)
        results = search_run(pattern, target, ignore_case=True, extension=ext)

        found_lines = 0
        total_matches = 0
        index = 1

        for result in results:
            try:
                line_number, line_rest = result.split(" ", 1)
            except ValueError:
                line_number, line_rest = "?", result

        matches = list(regex.finditer(line_rest))
        if matches:
            found_lines += 1

            # Always use the FIRST match in the line
            m = matches[0]
            start, end = m.span()

            # Slice from the match start
            extracted = line_rest[start:]

            # Stop at the first period AFTER the match
            period_index = extracted.find(".")
            if period_index != -1:
                extracted = extracted[:period_index + 1]

            # Insert line header (still showing match index + line number)
            output_widget.insert("end", f"[{index:03}] (line {line_number:>4})  ", "linenum")

            # Show the extracted substring with highlight on the match
            # Recalculate match position within 'extracted'
            local_match_start = 0
            local_match_end = end - start

            # Insert text up to match
            output_widget.insert("end", extracted[:local_match_start])

            # Insert highlighted match
            output_widget.insert("end", extracted[local_match_start:local_match_end], "match")

            # Insert remainder
            output_widget.insert("end", extracted[local_match_end:] + "\n")

            total_matches += 1
            index += 1

        if total_matches == 0:
            output_widget.insert("end", "\nNo matches found.\n", "info")
        else:
            output_widget.insert("end", f"\nTotal lines with matches: {found_lines}\n", "info")
            output_widget.insert("end", f"Total match occurrences: {total_matches}\n", "info")


def launch_gui():
    """Start the Parsely main application window."""
    app = ttk.Window(themename="darkly")
    TextSearchGUI(app)
    app.mainloop()


if __name__ == "__main__":
    launch_gui()

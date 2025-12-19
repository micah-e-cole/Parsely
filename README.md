<p align="center">
  <img src="assets/parsely.png" alt="Parsely Logo" width="160">
</p>

<h1 align="center">Parsely</h1>

<p align="center">
  <em>A fast, intuitive text-search utility built with Python, tkinter, and ttkbootstrap.</em>
</p>

---

## Contents

- [About](#-purpose)
- [Getting Started](#-getting-started)
- [Features](#-features)
- [Future Enhancements](#-future-enhancements)
- [Future Improvements (Full Roadmap)](TODO.md)

---

## About

This project began from a need for a better way to search through multiple types of documents for specific error messages.  
Given the constraints of managed corporate devices, traditional tools such as **grep**, **awk**, or **sed** were unavailable — as Linux subsystems and virtual machines were not permitted under company policy.

To remain compliant, I needed a solution that could run **entirely on a managed Windows device** that already included Python.

**Parsely** provides a graphical, Python-based text search utility that allows users to search local files of various formats through a simple and intuitive GUI (powered by `tkinter` and `ttkbootstrap`).  
Instead of relying on unreliable dashboard filters or manual scanning, users can download reports or logs and search seamlessly through them via this interface.

---

## Getting Started

Right now, Parsely can be launched by running `py bootstrap.py` from within the root directory of the application once you have downloaded the project onto your device with an existing Python installation.

```parsely/
|-- main/
    |-- gui.pyw
    |-- search.py
    |-- splash.py
|-- assets/
|-- main_entry.py
|-- requirements.txt
|-- README.md
```

---

## Features

- **Multi-format search support** – Find text in `.txt`, `.csv`, `.log`, `.pdf`, `.docx`, and `.xlsx` files.
- **Dual-term search** – Compare or search for two keywords side-by-side, with color-coded results.
- **Modern GUI** – Built with `ttkbootstrap` for a clean, responsive interface and dark theme.
- **Match counts and highlights** – See total occurrences, line numbers, and highlighted matches instantly.
- **No admin rights required** – Runs in a self-contained environment created by `run.py`.
- **Auto dependency setup** – Automatically installs required Python libraries if missing.
- **Lightweight and portable** – Runs directly from any folder without installation.
- **Splash screen with logo** – Branded loading experience on startup.
- **Simple path selection** – Browse to files via GUI, no typing required.
- **Expandable architecture** – Modular design for adding new file types or search logic easily.

---

## Future Enhancements

Some of the improvements and features that are planned for future versions of **Parsely**:

- [ ] **Package the application into a standalone executable using PyInstaller**
- [ ] Add drag-and-drop file support
- [ ] Implement user preferences for theme and search behavior
- [ ] Implement a settings panel for default themes and filters
- [ ] Add file-type icons and visual status indicators
- [ ] Improve PDF scanning accuracy with OCR fallback (tesserect required and at least for Windows environments there is no way to implement this without admin rights to download.)
- [ ] Export search results tp CSV, JSON, etc.

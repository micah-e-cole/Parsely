<p align="center">
  <img src="main/assets/parsely.png" alt="Parsely Logo" width="160">
</p>

<h1 align="center">Parsely</h1>

<p align="center">
  <em>A fast, intuitive text-search utility built with Python, tkinter, and ttkbootstrap.</em>
</p>

---

## Purpose

This project began from a need for a better way to search through multiple types of documents for specific error messages.  
Given the constraints of managed corporate devices, traditional tools such as **grep**, **awk**, or **sed** were unavailable — as Linux subsystems and virtual machines were not permitted under company policy.

To remain compliant, I needed a solution that could run **entirely on a managed Windows device** that already included Python.

**Parsely** provides a graphical, Python-based text search utility that allows users to search local files of various formats through a simple and intuitive GUI (powered by `tkinter` and `ttkbootstrap`).  
Instead of relying on unreliable dashboard filters or manual scanning, users can download reports or logs and search seamlessly through them via this interface.

---

## Getting Started

Right now, Parsely can be launched by running `py run.py` from within the root directory of the application.

```parsely/
|-- main/
    |-- assets/
    |-- gui.pyw
    |-- search.py
    |-- cli.py
    |-- splash.py
|-- run.py
|-- requirements.txt
|-- README.md
|-- launch_textsearch.bat
```

---

## Future Enhancements

Some of the improvements and features that are planned for future versions of **Parsely**:

- [ ] **Package the application into a standalone executable using PyInstaller**
- [ ] Add drag-and-drop file support
- [ ] Add cross-platform builds (Windows `.exe`, macOS `.app`)
- [ ] Implement user preferences for theme and search behavior
- [ ] Implement a settings panel for default themes and filters
- [ ] Add file-type icons and visual status indicators
- [ ] Improve PDF scanning accuracy with OCR fallback (tesserect required and at least for Windows environments there is no way to implement this without admin rights to download.)
- [ ] Export search results tp CSV, JSON, etc.

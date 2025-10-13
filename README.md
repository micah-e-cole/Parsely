<p align="center">
  <img src="main/assets/parsely.png" alt="Parsely Logo" width="160">
</p>

<h1 align="center">Parsely</h1>

<p align="center">
  <em>A fast, intuitive text-search utility built with Python and ttkbootstrap.</em>
</p>

---

## Purpose

This project began as a need for a better way of searching through multiple types of documents for specific error messages. Given the constraints of managed devices within an organization, tools that would ordinarily be used (such as `grep`, `awk`, or `sed`) were unavailable as Linux subsystems and Virtual Machines were not an approved company policy. To remain in compliance, I needed a tool that could be developed on my managed device which already conveniently had Python installed.

This tool allows a user to interact with files stored on their device by using a Graphical User Interface (gui) powered by Python/tkinter. Instead of usinig a search filter (which sometimes proved unreliable) on the canvas UI of a reporting dashboard, files are able to be downloaded and searched seamlessly via this visual search tool.

## Getting Started

Can be run either by launching via the command line and entering `py run.py` OR by double-clicking the launch_textsearch.bat file
Here is some text.

parsely/
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

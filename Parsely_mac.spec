# Parsely_mac.spec — macOS .app bundle with Tkinter included

import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.build_main import Analysis, PYZ, EXE, BUNDLE

# __file__ is not defined in PyInstaller spec runtime — use current working directory instead
BASE_DIR = Path(os.getcwd())
MAIN_SCRIPT = BASE_DIR / "main_entry.py"
ICON_FILE = BASE_DIR / "main" / "assets" / "parsely.icns"
APP_NAME = "Parsely"

# collect assets
datas = collect_data_files("main", includes=["assets/*", "*.png", "*.ico", "*.jpg"])

a = Analysis(
    [str(MAIN_SCRIPT)],
    pathex=[str(BASE_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "tkinter",
        "ttkbootstrap",
        "PIL._tkinter_finder",   # ensure Tk is included
        "pdfplumber",
        "openpyxl",
        "python_docx",
        "typer",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=APP_NAME,
    debug=False,
    strip=False,
    upx=True,
    console=False,
)

app = BUNDLE(
    exe,
    name=f"{APP_NAME}.app",
    icon=str(ICON_FILE),
    bundle_identifier="com.micahbraun.parsely",
    info_plist={
        "CFBundleDisplayName": APP_NAME,
        "CFBundleName": APP_NAME,
        "CFBundleVersion": "1.0",
        "CFBundleShortVersionString": "1.0.0",
        "CFBundleIdentifier": "com.micahbraun.parsely",
        "CFBundleExecutable": APP_NAME,
        "CFBundlePackageType": "APPL",
        "LSMinimumSystemVersion": "13.0",
        "NSHighResolutionCapable": True,
        "NSPrincipalClass": "NSApplication",
    },
)

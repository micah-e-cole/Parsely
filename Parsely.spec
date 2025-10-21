# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_entry.py'],
    pathex=[],
    binaries=[],
    datas=[('main/assets/parsely.png', 'main/assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Parsely',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['main/assets/parsely.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Parsely',
)
app = BUNDLE(
    coll,
    name='Parsely.app',
    icon='main/assets/parsely.icns',
    bundle_identifier=None,
)

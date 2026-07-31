# -*- mode: python ; coding: utf-8 -*-
# PyInstaller onedir build — output: ../../distributions/portable/
# Rebuild: powershell -File release\packaging\build_windows.ps1

from pathlib import Path

PACKAGING = Path(SPECPATH).resolve().parent
RELEASE = PACKAGING.parent
REPO_ROOT = RELEASE.parent
APP_ROOT = REPO_ROOT / "app"
ASSETS = APP_ROOT / "assets"

a = Analysis(
    [str(APP_ROOT / "main.py")],
    pathex=[str(APP_ROOT / "src")],
    binaries=[],
    datas=[(str(ASSETS), "assets")],
    hiddenimports=[
        "PIL._tkinter_finder",
        "customtkinter",
        "cv2",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib",
        "scipy",
        "pandas",
        "pytest",
        "IPython",
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="NetDefenseOpsConsole",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=str(PACKAGING / "version_info.txt"),
    icon=str(PACKAGING / "app_icon.ico"),
    uac_admin=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="NetDefenseOpsConsole",
)

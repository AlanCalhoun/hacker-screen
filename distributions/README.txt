Hacker Screen - distribution folders
=====================================

Each subfolder is one way to run or share the app.

  dev\        Run from source - see app\ folder
  pip\        Python wheel / pip install package
  portable\   Windows folder - zip and run, no install
  installer\  Windows Setup .exe - standard install

Build Windows releases:
  powershell -ExecutionPolicy Bypass -File release\packaging\build_windows.ps1

Build pip wheel:
  powershell -ExecutionPolicy Bypass -File release\packaging\build_pip.ps1

Visual simulation only. No real network activity.

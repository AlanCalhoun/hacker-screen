INSTALLER - Windows Setup .exe
================================

After building, this folder contains:

  NetDefenseOpsConsole-Setup-VERSION.exe

Give this single file to end users. It installs to:
  %LOCALAPPDATA%\Programs\NetDefenseOpsConsole

Per-user install (no admin). Uninstall via Settings -> Apps.

Build:
  powershell -ExecutionPolicy Bypass -File release\packaging\build_windows.ps1

Nothing here until you run the build script.

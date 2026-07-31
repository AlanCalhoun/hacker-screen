PORTABLE - Windows folder (no install)
======================================

After building, this folder contains:

  NetDefenseOpsConsole\
    NetDefenseOpsConsole.exe   <- double-click to run
    _internal\                 <- runtime + assets (do not delete)

Zip the entire NetDefenseOpsConsole folder to share on USB or network.

Build:
  powershell -ExecutionPolicy Bypass -File release\packaging\build_windows.ps1

Nothing here until you run the build script.

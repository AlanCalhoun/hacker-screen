# Installing Hacker Screen (Windows)

## Option A — GitHub Release (recommended)

1. Open [Releases](https://github.com/AlanCalhoun/hacker-screen/releases).
2. Download **NetDefenseOpsConsole-Setup-1.1.0.exe** (or latest).
3. Run the installer. No administrator rights required.
4. Launch **Net Defense Ops Console** from the Start Menu.

Install location: `%LOCALAPPDATA%\Programs\NetDefenseOpsConsole`

Uninstall via **Settings → Apps**.

## Option B — Portable folder

1. Download the **portable** zip from Releases (or build locally — see [RELEASING.md](RELEASING.md)).
2. Extract the folder.
3. Run `NetDefenseOpsConsole.exe`.

Do not delete the `_internal` folder — it contains the runtime and assets.

## Option C — Python (developers)

Requires Python 3.10+.

```powershell
git clone https://github.com/AlanCalhoun/hacker-screen.git
cd hacker-screen/app
python -m pip install -r requirements.txt
python main.py
```

## Option D — pip

```powershell
cd release
python -m pip install -e .
net-defense-console
```

## Antivirus notes

The Windows installer is built with PyInstaller and Inno Setup (onedir layout, no UPX). Some scanners flag unsigned executables. Rebuild locally from source if needed:

```powershell
powershell -ExecutionPolicy Bypass -File release\packaging\build_windows.ps1
```

## Disclaimer

Visual simulation only. No real network activity.

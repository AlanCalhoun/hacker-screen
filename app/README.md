# Application source

Run the five ops consoles from here during development.

## Quick start

```powershell
cd "E:\github\Hacker Screen\app"
python -m pip install -r requirements.txt
python main.py
```

Or double-click **run.bat**.

Requires **Python 3.10+**.

## Layout

```text
app/
  main.py           Entry point
  run.bat           Windows launcher
  requirements.txt  Dependencies
  src/hacker_screen/  Python package
  assets/           Maps, videos, images
```

## Fetch optional map assets

```powershell
set PYTHONPATH=src
python -m hacker_screen.fetch_ledger_map
python -m hacker_screen.fetch_orbital_map
python -m hacker_screen.generate_videos
```

## Build executables

From repo root (not this folder):

```powershell
powershell -ExecutionPolicy Bypass -File release\packaging\build_windows.ps1
```

Built files go to `../distributions/`.

# Net Defense Ops Console — Release / Install

Build tooling lives here. **Built outputs go to `../distributions/`**.

App source: `../app/` (`main.py`, `src/`, `assets/`)

## Repo layout

```text
Hacker Screen/
  README.md
  app/                 Application source + assets
  distributions/       Built installers, portable, wheels
  release/             Build scripts + pip metadata (you are here)
    packaging/
    pyproject.toml
    setup.py
    LICENSE
  build/               PyInstaller cache (gitignored)
```

## Build commands

From repo root:

```powershell
powershell -ExecutionPolicy Bypass -File release\packaging\build_windows.ps1
powershell -ExecutionPolicy Bypass -File release\packaging\build_pip.ps1
powershell -ExecutionPolicy Bypass -File release\packaging\build_installer.ps1
```

## Disclaimer

Visual simulation only. No real network activity.

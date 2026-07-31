# Contributing

Thanks for your interest in Hacker Screen. This project is a **visual simulation** for entertainment and demos — not a security tool.

## Development setup

1. Clone the repository.
2. Install Python **3.10+**.
3. From the repo root:

```powershell
cd app
python -m pip install -r requirements.txt
python main.py
```

## Project layout

| Path | Purpose |
|------|---------|
| `app/` | Application source and bundled assets |
| `distributions/` | Built installers and portable builds (generated) |
| `release/` | PyInstaller / Inno Setup scripts and pip metadata |
| `Screenshots/` | README gallery images |

## Pull requests

1. Fork and create a feature branch from `main`.
2. Keep changes focused — match existing code style and naming.
3. Test locally: `python main.py` and, if touching packaging, run `release\packaging\build_windows.ps1`.
4. Do not commit built `.exe` files or `distributions/portable/` output.

## Optional map assets

If street or orbital maps are missing after clone:

```powershell
cd app
set PYTHONPATH=src
python -m hacker_screen.fetch_ledger_map
python -m hacker_screen.fetch_orbital_map
python -m hacker_screen.generate_videos
```

## Code of conduct

Be respectful. This is a hobby / demo project.

# First-time GitHub upload

Hacker Screen should be its **own repository** (not the parent `E:\github` monorepo).

## 1. Create the repo on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Name: `hacker-screen` (or your preference)
3. Description: *Multi-console ops dashboard simulation for Windows*
4. Public, **no** README/license/gitignore (this repo already has them)
5. Create repository

## 2. Initialize and push (from this folder)

```powershell
cd "E:\github\Hacker Screen"

git init
git add .
git status
git commit -m "Initial release v1.1.0 — five ops consoles and Windows installer build"
git branch -M main
git remote add origin https://github.com/AlanCalhoun/hacker-screen.git
git push -u origin main
```

Repository: https://github.com/AlanCalhoun/hacker-screen

## 3. Build and publish the installer

The Setup `.exe` is **~135 MB** — too large to commit. Use **GitHub Releases**:

```powershell
powershell -ExecutionPolicy Bypass -File release\packaging\build_windows.ps1

gh release create v1.1.0 `
  --title "v1.1.0" `
  --notes-file CHANGELOG.md `
  "distributions/installer/NetDefenseOpsConsole-Setup-1.1.0.exe"
```

Or tag push triggers the workflow in `.github/workflows/release.yml`:

```powershell
git tag v1.1.0
git push origin v1.1.0
```

## 4. What gets committed

| Included | Excluded (gitignore) |
|----------|----------------------|
| Source (`app/`) | `distributions/installer/*.exe` |
| Assets (maps, videos) | `distributions/portable/` |
| Screenshots | `release/build/` |
| Build scripts | `*.egg-info/` |

## 5. Optional: build before first push

Verify the project runs:

```powershell
cd app
python -m pip install -r requirements.txt
python main.py
```

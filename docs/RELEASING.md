# Publishing a release

Built Windows installers exceed GitHub's **100 MB per-file** limit (~135 MB). Publish them as **GitHub Release assets**, not as committed files.

## 1. Build locally

From repo root:

```powershell
powershell -ExecutionPolicy Bypass -File release\packaging\build_windows.ps1
```

Outputs:

| Artifact | Path |
|----------|------|
| Installer | `distributions/installer/NetDefenseOpsConsole-Setup-1.1.0.exe` |
| Portable | `distributions/portable/NetDefenseOpsConsole/` |

Version is read from `release/packaging/VERSION`.

## 2. Zip portable (optional)

```powershell
Compress-Archive -Path "distributions\portable\NetDefenseOpsConsole" `
  -DestinationPath "distributions\portable\NetDefenseOpsConsole-1.1.0-portable.zip"
```

## 3. Create GitHub Release

Using [GitHub CLI](https://cli.github.com/):

```powershell
gh release create v1.1.0 `
  --title "v1.1.0" `
  --notes-file CHANGELOG.md `
  "distributions/installer/NetDefenseOpsConsole-Setup-1.1.0.exe" `
  "distributions/portable/NetDefenseOpsConsole-1.1.0-portable.zip"
```

Or upload the `.exe` and zip manually on the GitHub **Releases** page.

## 4. Update CHANGELOG

Edit `CHANGELOG.md` for each release.

## Pip wheel (optional)

```powershell
powershell -ExecutionPolicy Bypass -File release\packaging\build_pip.ps1
```

Attach `distributions/pip/*.whl` to the release if desired.

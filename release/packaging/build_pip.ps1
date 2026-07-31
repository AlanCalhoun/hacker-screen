#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$PackagingDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ReleaseRoot = Split-Path -Parent $PackagingDir
$AppRoot = Split-Path -Parent $ReleaseRoot
$Version = (Get-Content (Join-Path $PackagingDir "VERSION") -Raw).Trim()
$OutDir = Join-Path $AppRoot "distributions\pip"

Set-Location $ReleaseRoot

Write-Host "== Building pip wheel v$Version ==" -ForegroundColor Cyan
Write-Host "Output: $OutDir"

if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
}

Get-ChildItem $OutDir -Filter "*.whl" -File -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem $OutDir -Filter "*.tar.gz" -File -ErrorAction SilentlyContinue | Remove-Item -Force

python -m pip install build --quiet
python -m pip wheel . --no-deps -w $OutDir

Write-Host ""
Write-Host "Wheel(s) in distributions\pip\:" -ForegroundColor Green
Get-ChildItem $OutDir -Filter "*.whl" | ForEach-Object { Write-Host "  $($_.Name)" }
Write-Host ""
Write-Host "Install: python -m pip install distributions\pip\*.whl"

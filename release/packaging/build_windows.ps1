#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$PackagingDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ReleaseRoot = Split-Path -Parent $PackagingDir
$RepoRoot = Split-Path -Parent $ReleaseRoot
$AppRoot = Join-Path $RepoRoot "app"
$Version = (Get-Content (Join-Path $PackagingDir "VERSION") -Raw).Trim()

$DistRoot = Join-Path $RepoRoot "distributions"
$PortableDir = Join-Path $DistRoot "portable\NetDefenseOpsConsole"
$InstallerDir = Join-Path $DistRoot "installer"
$StagingDist = Join-Path $ReleaseRoot "build\_pyinstaller"

Set-Location $ReleaseRoot

Write-Host "== Hacker Screen - Windows build v$Version ==" -ForegroundColor Cyan
Write-Host "Repo root:   $RepoRoot"
Write-Host "App source:  $AppRoot"
Write-Host "Portable:    $PortableDir"
Write-Host "Installer:   $InstallerDir"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python not found on PATH."
}

Write-Host ""
Write-Host "Preparing distribution folders..."
foreach ($dir in @($DistRoot, (Split-Path $PortableDir), $InstallerDir)) {
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
}
if (Test-Path $PortableDir) { Remove-Item $PortableDir -Recurse -Force }
if (Test-Path $StagingDist) { Remove-Item $StagingDist -Recurse -Force }
Get-ChildItem $InstallerDir -Filter "NetDefenseOpsConsole-Setup-*.exe" -File -ErrorAction SilentlyContinue |
    Remove-Item -Force

Write-Host "Installing build dependencies..."
python -m pip install -r "$AppRoot\requirements.txt" "pyinstaller>=6.0" --quiet

Write-Host "Ensuring video assets exist..."
$env:PYTHONPATH = Join-Path $AppRoot "src"
python -m hacker_screen.generate_videos

Write-Host "Building onedir executable (UPX off, no admin UAC)..."
python -m PyInstaller packaging\NetDefenseOpsConsole.spec `
    --noconfirm --clean `
    --distpath $StagingDist `
    --workpath build

$built = Join-Path $StagingDist "NetDefenseOpsConsole"
if (-not (Test-Path (Join-Path $built "NetDefenseOpsConsole.exe"))) {
    throw "Build failed - executable not found in $built"
}

Write-Host "Moving bundle to distributions\portable\NetDefenseOpsConsole\ ..."
Move-Item $built $PortableDir
if (Test-Path $StagingDist) { Remove-Item $StagingDist -Recurse -Force -ErrorAction SilentlyContinue }

Write-Host ""
Write-Host "Portable app ready:" -ForegroundColor Green
Write-Host "  $PortableDir"

Write-Host ""
Write-Host "Building Windows installer..."
& (Join-Path $PackagingDir "build_installer.ps1") -Version $Version

Write-Host ""
Write-Host "== Build complete (v$Version) ==" -ForegroundColor Green
Write-Host ""
Write-Host "  INSTALLER:  distributions\installer\NetDefenseOpsConsole-Setup-$Version.exe"
Write-Host "  PORTABLE:   zip distributions\portable\NetDefenseOpsConsole\"
Write-Host "  GUIDE:      distributions\README.txt"

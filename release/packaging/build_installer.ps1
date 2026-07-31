#Requires -Version 5.1
param(
    [string]$Version = ""
)

$ErrorActionPreference = "Stop"

function Get-InnoSetupCompiler {
    $candidates = @(
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
    )
    foreach ($path in $candidates) {
        if (Test-Path $path) { return $path }
    }
    $cmd = Get-Command iscc -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    return $null
}

$PackagingDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ReleaseRoot = Split-Path -Parent $PackagingDir
$AppRoot = Split-Path -Parent $ReleaseRoot
if (-not $Version) {
    $Version = (Get-Content (Join-Path $PackagingDir "VERSION") -Raw).Trim()
}

$AppBundle = Join-Path $AppRoot "distributions\portable\NetDefenseOpsConsole"
$InstallerDir = Join-Path $AppRoot "distributions\installer"
$IssFile = Join-Path $PackagingDir "installer.iss"

if (-not (Test-Path (Join-Path $AppBundle "NetDefenseOpsConsole.exe"))) {
    throw @"
Portable app bundle not found. Run build_windows.ps1 first.
  Expected: $AppBundle
"@
}

if (-not (Test-Path $InstallerDir)) {
    New-Item -ItemType Directory -Path $InstallerDir -Force | Out-Null
}

$iscc = Get-InnoSetupCompiler
if (-not $iscc) {
    Write-Host "Inno Setup not found." -ForegroundColor Yellow
    Write-Host "Install it, then re-run this script:"
    Write-Host "  winget install --id JRSoftware.InnoSetup -e"
    throw "ISCC.exe not found."
}

Write-Host "== Building Windows installer v$Version ==" -ForegroundColor Cyan
Write-Host "Source:   $AppBundle"
Write-Host "Output:   $InstallerDir"
Write-Host "Compiler: $iscc"

& $iscc "/DMyAppVersion=$Version" $IssFile

$setup = Get-ChildItem $InstallerDir -Filter "NetDefenseOpsConsole-Setup-*.exe" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $setup) {
    throw "Installer build failed - setup exe not found in $InstallerDir"
}

Write-Host ""
Write-Host "Installer ready:" -ForegroundColor Green
Write-Host "  $($setup.FullName)"
Write-Host "  $([math]::Round($setup.Length / 1MB, 1)) MB"

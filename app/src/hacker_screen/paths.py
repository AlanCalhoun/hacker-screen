"""Resolve project, asset, and user-data paths for dev, pip, and frozen builds."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def project_root() -> Path:
    """App folder (dev) or install folder (frozen)."""
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[2]


def repo_root() -> Path:
    """Hacker Screen repo root (dev only)."""
    return Path(__file__).resolve().parents[3]


def bundle_root() -> Path | None:
    """PyInstaller one-file/one-dir extract root, if running frozen."""
    meipass = getattr(sys, "_MEIPASS", None)
    return Path(meipass) if meipass else None


def assets_dir() -> Path:
    pkg_assets = Path(__file__).resolve().parent / "assets"
    if pkg_assets.is_dir():
        return pkg_assets
    if is_frozen():
        bundled = (bundle_root() or project_root()) / "assets"
        if bundled.is_dir():
            return bundled
    return project_root() / "assets"


def user_data_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    path = base / "NetDefenseOpsConsole"
    path.mkdir(parents=True, exist_ok=True)
    return path


def videos_dir() -> Path:
    """Writable video root; seeded from bundled assets on first frozen run."""
    if is_frozen():
        target = user_data_dir() / "videos"
        target.mkdir(parents=True, exist_ok=True)
        bundled = assets_dir() / "videos"
        if bundled.is_dir():
            for src in bundled.rglob("*.mp4"):
                rel = src.relative_to(bundled)
                dst = target / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                if not dst.exists() or dst.stat().st_size != src.stat().st_size:
                    shutil.copy2(src, dst)
        return target
    path = project_root() / "assets" / "videos"
    path.mkdir(parents=True, exist_ok=True)
    return path


def theme_videos_dir(theme_id: str) -> Path:
    path = videos_dir() / theme_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def app_icon_path() -> Path | None:
    for candidate in (
        assets_dir() / "images" / "app_icon.ico",
        repo_root() / "release" / "packaging" / "app_icon.ico",
    ):
        if candidate.exists():
            return candidate
    return None


def apply_window_icon(window) -> None:
    icon = app_icon_path()
    if not icon:
        return
    try:
        window.iconbitmap(default=str(icon))
    except Exception:
        pass

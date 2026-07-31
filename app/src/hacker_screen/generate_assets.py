"""Verify bundled assets exist."""

from __future__ import annotations

from hacker_screen.paths import assets_dir

MAP_FILE = assets_dir() / "map" / "world_map.png"
LEDGER_MAP = assets_dir() / "map" / "ledger_street_osm.png"
ORBITAL_MAP = assets_dir() / "map" / "orbital_earth_strip.png"
KALI_LOGO = assets_dir() / "images" / "kali_logo.png"
SEALS_DIR = assets_dir() / "images" / "seals"
LAUNCHER_BG = assets_dir() / "images" / "launcher_bg.png"


def ensure_assets() -> None:
    missing = [
        name for name, path in (
            ("world map", MAP_FILE),
            ("Kali logo", KALI_LOGO),
            ("launcher background", LAUNCHER_BG),
        )
        if not path.exists()
    ]
    if not ORBITAL_MAP.exists():
        missing.append("orbital earth strip (run: python -m hacker_screen.fetch_orbital_map)")
    if not LEDGER_MAP.exists():
        missing.append("ledger street map (run: python -m hacker_screen.fetch_ledger_map)")
    if not any(SEALS_DIR.glob("seal_*.png")):
        missing.append("agency seals")
    if missing:
        print(f"Warning: missing assets: {', '.join(missing)}")

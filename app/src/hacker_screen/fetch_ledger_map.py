"""Download real OpenStreetMap imagery for the Financial Intel street map."""

from __future__ import annotations

import math
import urllib.request
from pathlib import Path

from PIL import Image

from hacker_screen.paths import assets_dir, project_root

# Portland OR — SE Hawthorne / Ladd's Addition
LAT, LON, ZOOM = 45.5122, -122.6536, 16
TILE = 256
COLS, ROWS = 5, 4
OUT_W, OUT_H = 1280, 960
USER_AGENT = "NetDefenseOpsConsole/1.0 (local asset fetch)"


def _latlon_to_tile(lat: float, lon: float, z: int) -> tuple[int, int]:
    n = 2**z
    x = int((lon + 180.0) / 360.0 * n)
    lat_r = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_r)) / math.pi) / 2.0 * n)
    return x, y


def _fetch_tile(z: int, x: int, y: int) -> Image.Image:
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return Image.open(resp).convert("RGB")


def fetch_ledger_street_map(dest: Path | None = None) -> Path:
    """Stitch OSM tiles and save the bundled ledger map PNG."""
    dest = dest or assets_dir() / "map" / "ledger_street_osm.png"
    dest.parent.mkdir(parents=True, exist_ok=True)

    cx, cy = _latlon_to_tile(LAT, LON, ZOOM)
    x0, y0 = cx - COLS // 2, cy - ROWS // 2
    mosaic = Image.new("RGB", (COLS * TILE, ROWS * TILE))
    for j in range(ROWS):
        for i in range(COLS):
            tile = _fetch_tile(ZOOM, x0 + i, y0 + j)
            mosaic.paste(tile, (i * TILE, j * TILE))

    w, h = mosaic.size
    left = (w - OUT_W) // 2
    top = (h - OUT_H) // 2
    crop = mosaic.crop((left, top, left + OUT_W, top + OUT_H))
    crop.save(dest)
    return dest


def main() -> None:
    path = fetch_ledger_street_map()
    print(f"Saved ledger street map: {path}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(project_root() / "src"))
    main()

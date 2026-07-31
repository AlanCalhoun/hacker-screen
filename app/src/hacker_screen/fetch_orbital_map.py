"""Download OSM equirectangular strip for orbital ground-track display."""

from __future__ import annotations

import math
import urllib.request
from pathlib import Path

from PIL import Image

from hacker_screen.paths import assets_dir, project_root

ZOOM = 2  # world = 4×4 tiles
TILE = 256
USER_AGENT = "NetDefenseOpsConsole/1.0 (local asset fetch)"


def _fetch_tile(z: int, x: int, y: int) -> Image.Image:
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return Image.open(resp).convert("RGB")


def fetch_orbital_earth_strip(dest: Path | None = None) -> Path:
    """Stitch zoom-2 OSM world tiles into a mid-latitude strip (tileable east-west)."""
    dest = dest or assets_dir() / "map" / "orbital_earth_strip.png"
    dest.parent.mkdir(parents=True, exist_ok=True)

    n = 2 ** ZOOM
    mosaic = Image.new("RGB", (n * TILE, n * TILE))
    for ty in range(n):
        for tx in range(n):
            mosaic.paste(_fetch_tile(ZOOM, tx, ty), (tx * TILE, ty * TILE))

    # Mid-latitude band (~30°N–55°N on equirectangular)
    y0 = int(n * TILE * 0.28)
    y1 = int(n * TILE * 0.52)
    strip = mosaic.crop((0, y0, n * TILE, y1))
    # Scale up for smoother scroll
    strip = strip.resize((2048, 360), Image.Resampling.LANCZOS)
    strip.save(dest)
    return dest


def main() -> None:
    path = fetch_orbital_earth_strip()
    print(f"Saved orbital earth strip: {path}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(project_root() / "src"))
    main()

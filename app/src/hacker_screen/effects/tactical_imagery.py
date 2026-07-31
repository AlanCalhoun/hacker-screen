"""Procedural / real street map imagery for Financial Intel console."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from hacker_screen.effects.perf import clamp_dims, fast_resize

from hacker_screen.paths import assets_dir

# Real OSM capture — Portland OR, Hawthorne / Ladd's Addition (zoom 16)
LEDGER_MAP_FILE = assets_dir() / "map" / "ledger_street_osm.png"

LEDGER_CITY = {
    "name": "Portland, OR",
    "lat": 45.5122,
    "lon": -122.6536,
    "zoom": 16,
}


@dataclass(frozen=True)
class StreetMapTarget:
    address: str
    city_line: str
    street_name: str
    nx: float  # pin position 0..1 on source image
    ny: float


DEFAULT_TARGET = StreetMapTarget(
    address="2847 SE Hawthorne Blvd",
    city_line="Portland, OR 97214",
    street_name="SE Hawthorne Blvd",
    nx=0.5187,
    ny=0.6279,
)


def _font(size: int = 11, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ["consolab.ttf", "consola.ttf", "cour.ttf", "arial.ttf"] if bold else ["consola.ttf", "cour.ttf", "arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def apply_console_map_theme(img: Image.Image) -> Image.Image:
    """Grade a real map tile capture to match the ops-console green aesthetic."""
    arr = np.array(img.convert("RGB"), dtype=np.float32)
    lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    arr = arr * 0.28 + lum[:, :, np.newaxis] * 0.72
    arr[:, :, 0] *= 0.42
    arr[:, :, 1] *= 1.08
    arr[:, :, 2] *= 0.68
    arr *= 0.78
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    out = Image.fromarray(arr, mode="RGB")
    out = ImageEnhance.Contrast(out).enhance(1.22)
    out = ImageEnhance.Sharpness(out).enhance(1.15)
    # Soft vignette
    w, h = out.size
    vignette = Image.new("L", (w, h), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse([-w * 0.15, -h * 0.15, w * 1.15, h * 1.15], fill=220)
    vd.rectangle([0, 0, w, h], fill=0)
    vig = np.array(vignette, dtype=np.float32) / 255.0
    vig = np.clip(0.55 + vig * 0.45, 0, 1)
    a2 = np.array(out, dtype=np.float32)
    a2 *= vig[:, :, np.newaxis]
    return Image.fromarray(np.clip(a2, 0, 255).astype(np.uint8))


def _load_source_map() -> Image.Image | None:
    if LEDGER_MAP_FILE.exists():
        return Image.open(LEDGER_MAP_FILE).convert("RGB")
    return None


def _draw_pin_overlay(
    img: Image.Image,
    target: StreetMapTarget,
) -> Image.Image:
    w, h = img.size
    tx = int(target.nx * w)
    ty = int(target.ny * h)
    draw = ImageDraw.Draw(img)
    f_sm = _font(10)
    f_md = _font(12, bold=True)

    # Target reticle
    for r in (22, 34):
        draw.ellipse([tx - r, ty - r, tx + r, ty + r], outline=(0, 220, 150), width=1)
    draw.line([(tx - 18, ty), (tx - 6, ty)], fill=(0, 255, 170), width=2)
    draw.line([(tx + 6, ty), (tx + 18, ty)], fill=(0, 255, 170), width=2)
    draw.line([(tx, ty - 18), (tx, ty - 6)], fill=(0, 255, 170), width=2)
    draw.line([(tx, ty + 6), (tx, ty + 18)], fill=(0, 255, 170), width=2)
    draw.ellipse([tx - 5, ty - 5, tx + 5, ty + 5], fill=(0, 255, 180))

    # Pin
    draw.ellipse([tx - 9, ty - 28, tx + 9, ty - 12], fill=(0, 240, 160))
    draw.polygon([tx, ty - 10, tx - 11, ty - 24, tx + 11, ty - 24], fill=(0, 240, 160))

    line1 = target.address.upper()
    line2 = target.city_line.upper()
    box_w = max(len(line1), len(line2)) * 8 + 28
    box_h = 46
    bx1 = min(max(10, tx - box_w // 2), w - box_w - 10)
    by1 = max(8, ty - 58 - box_h)
    draw.rectangle([bx1, by1, bx1 + box_w, by1 + box_h], fill=(4, 12, 10), outline=(0, 200, 130), width=2)
    draw.text((bx1 + 12, by1 + 8), line1, fill=(0, 255, 180), font=f_md)
    draw.text((bx1 + 12, by1 + 26), line2, fill=(120, 180, 160), font=f_sm)

    # OSM credit (required by license)
    draw.text((8, h - 14), "© OpenStreetMap contributors", fill=(80, 120, 100), font=f_sm)
    return img


def _crop_pin_position(
    sw: int, sh: int, w: int, h: int, target: StreetMapTarget,
) -> tuple[float, float]:
    """Normalized pin location after cover-crop centered on target."""
    pin_x = int(target.nx * sw)
    pin_y = int(target.ny * sh)
    target_ratio = w / h
    src_ratio = sw / sh
    if src_ratio > target_ratio:
        crop_h = sh
        crop_w = int(sh * target_ratio)
    else:
        crop_w = sw
        crop_h = int(sw / target_ratio)
    left = max(0, min(pin_x - crop_w // 2, sw - crop_w))
    top = max(0, min(pin_y - crop_h // 2, sh - crop_h))
    return (pin_x - left) / crop_w, (pin_y - top) / crop_h


def street_map_pin_fraction(
    width: int, height: int, *, target: StreetMapTarget = DEFAULT_TARGET,
) -> tuple[float, float]:
    """Pin position (0..1) on the themed street map at the given size."""
    source = _load_source_map()
    if source is None:
        return target.nx, target.ny
    sw, sh = source.size
    return _crop_pin_position(sw, sh, max(width, 320), max(height, 200), target)


def render_street_map(
    width: int,
    height: int,
    seed: int = 742,
    *,
    target: StreetMapTarget = DEFAULT_TARGET,
) -> Image.Image:
    """Real city map (OSM) resized and themed; procedural fallback if missing."""
    w, h = max(width, 320), max(height, 200)
    w, h = clamp_dims(w, h)
    source = _load_source_map()
    if source is not None:
        sw, sh = source.size
        pin_x = int(target.nx * sw)
        pin_y = int(target.ny * sh)
        target_ratio = w / h
        src_ratio = sw / sh
        if src_ratio > target_ratio:
            crop_h = sh
            crop_w = int(sh * target_ratio)
        else:
            crop_w = sw
            crop_h = int(sw / target_ratio)
        left = max(0, min(pin_x - crop_w // 2, sw - crop_w))
        top = max(0, min(pin_y - crop_h // 2, sh - crop_h))
        cropped = source.crop((left, top, left + crop_w, top + crop_h))
        pin_on_crop = StreetMapTarget(
            address=target.address,
            city_line=target.city_line,
            street_name=target.street_name,
            nx=(pin_x - left) / crop_w,
            ny=(pin_y - top) / crop_h,
        )
        img = fast_resize(cropped, w, h)
        img = apply_console_map_theme(img)
        return _draw_pin_overlay(img, pin_on_crop)

    return _render_procedural_fallback(w, h, seed, target=target)


def _render_procedural_fallback(
    w: int,
    h: int,
    seed: int,
    *,
    target: StreetMapTarget,
) -> Image.Image:
    """Minimal fallback when bundled OSM asset is absent."""
    rng = np.random.default_rng(seed)
    img = Image.new("RGB", (w, h), (24, 32, 38))
    draw = ImageDraw.Draw(img)
    for x in range(0, w, 28):
        draw.line([(x, 0), (x, h)], fill=(58, 72, 82), width=2)
    for y in range(0, h, 28):
        draw.line([(0, y), (w, y)], fill=(58, 72, 82), width=2)
    img = apply_console_map_theme(img)
    return _draw_pin_overlay(img, target)

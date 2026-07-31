"""Shared limits and helpers for smooth fullscreen animation."""

from __future__ import annotations

from PIL import Image

MAX_MAP_W = 1600
MAX_MAP_H = 900
MAX_VIDEO_W = 1280
MAX_VIDEO_H = 720


def clamp_dims(
    w: int, h: int, *, max_w: int = MAX_MAP_W, max_h: int = MAX_MAP_H, min_w: int = 320, min_h: int = 200,
) -> tuple[int, int]:
    w, h = max(min_w, w), max(min_h, h)
    if w <= max_w and h <= max_h:
        return w, h
    scale = min(max_w / w, max_h / h)
    return max(min_w, int(w * scale)), max(min_h, int(h * scale))


def fast_resize(img: Image.Image, w: int, h: int) -> Image.Image:
    if img.size == (w, h):
        return img
    return img.resize((w, h), Image.Resampling.BILINEAR)

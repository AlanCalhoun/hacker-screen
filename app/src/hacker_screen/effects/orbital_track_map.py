"""Orbital ground-track — scrolling Earth map, optimized for fullscreen."""

from __future__ import annotations

import math
import tkinter as tk

import numpy as np
from PIL import Image, ImageDraw, ImageTk

from hacker_screen.data.console_themes import ConsoleTheme
from hacker_screen.effects.perf import fast_resize
from hacker_screen.effects.tactical_imagery import apply_console_map_theme
from hacker_screen.paths import assets_dir

STRIP_FILE = assets_dir() / "map" / "orbital_earth_strip.png"
SCROLL_PX_PER_SEC = 38.0
TRACK_Y_BASE = 0.48
TRACK_Y_AMP = 0.14
TRACK_WAVES = 5.5


def track_y_fraction(map_x: float, strip_w: float) -> float:
    mx = map_x % strip_w
    return TRACK_Y_BASE + TRACK_Y_AMP * math.sin(mx / strip_w * math.pi * TRACK_WAVES)


def _load_themed_strip() -> Image.Image | None:
    if not STRIP_FILE.exists():
        return None
    return apply_console_map_theme(Image.open(STRIP_FILE).convert("RGB"))


class OrbitalTrackPanel(tk.Frame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        bg = theme.inner_bg
        super().__init__(master, bg=bg, **kwargs)
        self._theme = theme
        self._running = False
        self._time = 0.0
        self._sat_name = "NOAA-21"
        self._pass_id = 4821
        self._strip: Image.Image | None = None
        self._strip_photo: ImageTk.PhotoImage | None = None
        self._strip_display_h = 0
        self._strip_w = 2048
        self._strip_h = 360
        self._sky_photo: ImageTk.PhotoImage | None = None
        self._sky_size: tuple[int, int] = (0, 0)
        self._layout_size: tuple[int, int, int, int, int] = (0, 0, 0, 0, 0)
        self._footer_id: int | None = None
        self._strip_ids: list[tuple[int, int]] = []
        self._stations = [
            ("Goldstone DSN-14", 0.178),
            ("Svalbard GS", 0.544),
            ("Canberra DSN-43", 0.913),
        ]

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_resize)

        self._strip = _load_themed_strip()
        if self._strip:
            self._strip_w, self._strip_h = self._strip.size

    def _layout(self, w: int, h: int) -> tuple[int, int, int, int, int]:
        top, bot = 34, h - 34
        sky_h = max(28, int((bot - top) * 0.10))
        map_top = top + sky_h
        map_h = bot - map_top
        return top, bot, map_top, map_h, sky_h

    def _ensure_sky(self, w: int, sky_h: int) -> None:
        if (w, sky_h) == self._sky_size and self._sky_photo:
            return
        self._sky_size = (w, sky_h)
        img = Image.new("RGB", (w, sky_h), (2, 6, 14))
        rng = np.random.default_rng(42)
        draw = ImageDraw.Draw(img)
        for _ in range(80):
            sx = int(rng.integers(0, w))
            sy = int(rng.integers(0, sky_h))
            c = 28 + int(rng.integers(2, 6)) * 16
            draw.point((sx, sy), fill=(c, c + 18, c + 32))
        self._sky_photo = ImageTk.PhotoImage(img)

    def _ensure_strip_photo(self, display_h: int) -> None:
        if not self._strip or display_h < 40:
            return
        if self._strip_photo and self._strip_display_h == display_h:
            return
        self._strip_display_h = display_h
        scaled = fast_resize(self._strip, self._strip_w, display_h)
        self._strip_photo = ImageTk.PhotoImage(scaled)
        self._strip_h = display_h

    def _track_screen_y(self, map_x: float, map_top: int) -> float:
        return map_top + track_y_fraction(map_x, self._strip_w) * self._strip_h

    def _map_x_under_screen(self, scroll: float, screen_x: float) -> float:
        return (scroll + screen_x) % self._strip_w

    def _scroll(self) -> float:
        return (self._time * SCROLL_PX_PER_SEC) % self._strip_w

    def _rebuild_static(self, w: int, h: int, top: int, bot: int, map_top: int, sky_h: int) -> None:
        th = self._theme
        self.canvas.delete("all")
        self._strip_ids = []
        self._ensure_sky(w, sky_h)
        if self._sky_photo:
            self.canvas.create_image(0, top, anchor="nw", image=self._sky_photo, tags="static")
        self.canvas.create_rectangle(0, map_top, w, bot, fill="#061018", outline="", tags="static")
        if self._strip_photo:
            n_tiles = max(3, int(w / self._strip_w) + 3)
            for i in range(-1, -1 + n_tiles):
                iid = self.canvas.create_image(0, map_top, anchor="nw", image=self._strip_photo, tags="map")
                self._strip_ids.append((i, iid))
        else:
            pass  # fallback fill already drawn
        self.canvas.create_rectangle(0, 0, w, top, fill="#000000", outline="", tags="static")
        self.canvas.create_line(0, top, w, top, fill=th.map_border, width=1, tags="static")
        self.canvas.create_text(
            10, 17, anchor="w",
            text=f"GROUND TRACK  │  {self._sat_name}  │  PASS {self._pass_id}  │  INCL 98.7°",
            fill=th.map_hud, font=("Consolas", 10, "bold"), tags="static",
        )
        self.canvas.create_text(
            w - 10, 17, anchor="e", text="LIVE SCROLL  │  OSM TERRAIN",
            fill=th.label_muted, font=("Consolas", 9), tags="static",
        )
        self.canvas.create_rectangle(0, bot, w, h, fill="#000000", outline="", tags="static")
        self.canvas.create_line(0, bot, w, bot, fill=th.map_border, width=1, tags="static")
        self.canvas.create_text(
            10, map_top + (bot - map_top) + 2, anchor="nw",
            text="© OpenStreetMap contributors", fill="#3a6050", font=("Consolas", 8), tags="static",
        )
        self.canvas.create_rectangle(0, 0, w, h, fill="", outline=th.map_border, width=2, tags="static")
        self._footer_id = self.canvas.create_text(
            10, bot + 17, anchor="w", tags="static",
            text="", fill=th.map_hud, font=("Consolas", 9),
        )
        self._layout_size = (w, h, top, bot, map_top)

    def start(self) -> None:
        self._running = True
        self._animate()

    def stop(self) -> None:
        self._running = False

    def _on_resize(self, _event=None) -> None:
        self._sky_size = (0, 0)
        self._strip_photo = None
        self._strip_display_h = 0
        self._layout_size = (0, 0, 0, 0, 0)

    def _draw_anim(self, w: int, top: int, bot: int, map_top: int, scroll: float) -> None:
        th = self._theme
        self.canvas.delete("anim")
        sat_cx = w * 0.5
        sat_map_x = self._map_x_under_screen(scroll, sat_cx)
        sat_cy = self._track_screen_y(sat_map_x, map_top)

        if self._strip_ids:
            x0 = -scroll
            for i, iid in self._strip_ids:
                self.canvas.coords(iid, x0 + i * self._strip_w, map_top)

        step = 8 if w > 1000 else 5
        pts: list[float] = []
        for sx in range(0, w + 1, step):
            mx = self._map_x_under_screen(scroll, sx)
            pts.extend([sx, self._track_screen_y(mx, map_top)])
        if len(pts) >= 4:
            self.canvas.create_line(*pts, fill="#0a3028", width=5, smooth=True, tags="anim")
            self.canvas.create_line(
                *pts, fill=th.accent, width=2, dash=(10, 8),
                dashoffset=int(scroll) % 18, smooth=True, tags="anim",
            )

        linked = False
        for name, lon_frac in self._stations:
            map_x = lon_frac * self._strip_w
            gy = self._track_screen_y(map_x, map_top)
            for ox in (-self._strip_w, 0, self._strip_w):
                sx = map_x - scroll + ox
                if not (-80 <= sx <= w + 80):
                    continue
                near = abs(sx - sat_cx) < 75
                if near:
                    linked = True
                col = th.accent2 if near else th.map_node
                self.canvas.create_oval(sx - 5, gy - 5, sx + 5, gy + 5, fill=th.map_node_fill, outline=col, width=2, tags="anim")
                self.canvas.create_text(sx + 10, gy - 5, text=name, anchor="w", fill=th.label_muted, font=("Consolas", 8), tags="anim")
                if near:
                    self.canvas.create_line(sat_cx, sat_cy, sx, gy, fill=th.accent, width=1, dash=(5, 4), tags="anim")

        trail: list[float] = []
        for k in range(10):
            sx = sat_cx - k * 8
            mx = self._map_x_under_screen(scroll, sx)
            trail.extend([sx, self._track_screen_y(mx, map_top)])
        if len(trail) >= 4:
            self.canvas.create_line(*trail, fill=th.map_scan, width=2, smooth=True, tags="anim")

        eps = 2.0
        y0 = track_y_fraction(sat_map_x - eps, self._strip_w) * self._strip_h
        y1 = track_y_fraction(sat_map_x + eps, self._strip_w) * self._strip_h
        tdx, tdy = 2 * eps, y1 - y0
        length = math.hypot(tdx, tdy) or 1.0
        fx, fy = tdx / length, tdy / length
        px, py = -fy, fx
        pulse = 0.88 + 0.12 * math.sin(self._time * 1.7)
        reach, half = 75 * pulse, 18 * pulse
        swath = [
            sat_cx + px * half, sat_cy + py * half,
            sat_cx - px * half, sat_cy - py * half,
            sat_cx - px * half * 1.6 + fx * reach, sat_cy - py * half * 1.6 + fy * reach,
            sat_cx + px * half * 1.6 + fx * reach, sat_cy + py * half * 1.6 + fy * reach,
        ]
        self.canvas.create_polygon(*swath, fill="", outline=th.map_scan, width=1, dash=(4, 3), tags="anim")

        pw = 22
        self.canvas.create_line(sat_cx - pw, sat_cy, sat_cx + pw, sat_cy, fill=th.map_hud, width=3, tags="anim")
        self.canvas.create_oval(sat_cx - 4, sat_cy - 4, sat_cx + 4, sat_cy + 4, fill=th.map_node_fill, outline=th.accent2, tags="anim")
        self.canvas.create_polygon(
            sat_cx, sat_cy - 14, sat_cx - 9, sat_cy + 5, sat_cx + 9, sat_cy + 5,
            fill=th.accent2, outline=th.map_node, tags="anim",
        )
        self.canvas.create_text(sat_cx, sat_cy - 24, text=self._sat_name, fill=th.map_label, font=("Consolas", 10, "bold"), tags="anim")

        el = 48 + 20 * math.sin(self._time * 0.35)
        dl = "DOWNLINK LOCKED" if linked else "ACQUIRING SIGNAL"
        if self._footer_id is not None:
            self.canvas.itemconfigure(
                self._footer_id,
                text=f"AOS 14:22:08Z  LOS 14:31:44Z  │  EL {el:.1f}°  │  SWATH 2800 km  │  {dl}",
            )

    def _paint(self) -> None:
        w = max(self.canvas.winfo_width(), 480)
        h = max(self.canvas.winfo_height(), 320)
        top, bot, map_top, map_h, sky_h = self._layout(w, h)
        if self._strip:
            self._ensure_strip_photo(map_h)
        layout_key = (w, h, top, bot, map_top)
        if layout_key != self._layout_size:
            self._rebuild_static(w, h, top, bot, map_top, sky_h)
        self._draw_anim(w, top, bot, map_top, self._scroll())

    def _animate(self) -> None:
        if not self._running:
            return
        self._time += 0.05
        self._paint()
        self.after(66, self._animate)

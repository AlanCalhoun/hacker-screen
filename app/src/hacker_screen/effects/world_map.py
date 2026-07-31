"""Animated world map with connection arcs over AI-generated geography."""

from __future__ import annotations

import math
import random
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageTk

from hacker_screen.data.cities import CITIES
from hacker_screen.data.console_themes import ConsoleTheme
from hacker_screen.effects.perf import clamp_dims, fast_resize
from hacker_screen.paths import assets_dir

MAP_CANDIDATES = [
    assets_dir() / "map" / "world_map.png",
]


def _resolve_map() -> Path | None:
    for p in MAP_CANDIDATES:
        if p.exists():
            return p
    return None


class WorldMapPanel(tk.Frame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        bg = theme.inner_bg
        super().__init__(master, bg=bg, **kwargs)
        self._theme = theme
        self._running = False
        self._map_photo: ImageTk.PhotoImage | None = None
        self._base_map: Image.Image | None = None
        self._map_cache_size: tuple[int, int] = (0, 0)
        self._static_size: tuple[int, int] = (0, 0)
        self._connections: list[dict] = []
        self._pulse = 0.0
        self._dash_offset = 0
        self._scan_y = 0
        self._map_path = _resolve_map()

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_resize)

    def _city_to_xy(self, city: dict, w: int, h: int) -> tuple[int, int]:
        if "map_x" in city and "map_y" in city:
            return int(city["map_x"] * w), int(city["map_y"] * h)
        x = (city["lon"] + 180) / 360 * w
        y = (90 - city["lat"]) / 180 * h
        return int(x), int(y)

    def _build_map_image(self, w: int, h: int) -> Image.Image:
        if self._map_path is None:
            return Image.new("RGB", (w, h), (4, 12, 10))
        if self._base_map is None:
            self._base_map = Image.open(self._map_path).convert("RGB")
        img = fast_resize(self._base_map, w, h)
        img = ImageEnhance.Contrast(img).enhance(1.15)
        img = ImageEnhance.Color(img).enhance(1.2)
        return img.filter(ImageFilter.GaussianBlur(radius=0.4))

    def _ensure_map_photo(self, w: int, h: int) -> None:
        if (w, h) == self._map_cache_size and self._map_photo is not None:
            return
        self._map_cache_size = (w, h)
        self._map_photo = ImageTk.PhotoImage(self._build_map_image(w, h))

    def _make_connections(self) -> None:
        self._connections = []
        hubs = [c for c in CITIES if c["name"] in {
            "New York", "London", "Tokyo", "Moscow", "Singapore", "Dubai", "Sydney", "São Paulo",
        }]
        others = [c for c in CITIES if c not in hubs]
        random.shuffle(hubs)
        for i in range(len(hubs) - 1):
            self._add_connection(hubs[i], hubs[i + 1])
        for _ in range(8):
            a = random.choice(hubs)
            b = random.choice(others)
            if a != b:
                self._add_connection(a, b)

    def _add_connection(self, a: dict, b: dict) -> None:
        self._connections.append({
            "from": a,
            "to": b,
            "color": random.choice(self._theme.map_arc_colors),
            "progress": random.random(),
            "speed": random.uniform(0.006, 0.018),
            "packets": [{"t": random.random()} for _ in range(3)],
        })

    def start(self) -> None:
        self._running = True
        self._make_connections()
        self._animate()

    def stop(self) -> None:
        self._running = False

    def _on_resize(self, _event=None) -> None:
        self._map_cache_size = (0, 0)
        self._static_size = (0, 0)
        if self._running:
            self._draw()

    def _curve_points(self, x1: int, y1: int, x2: int, y2: int, steps: int = 30) -> list[tuple[int, int]]:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dist = math.hypot(x2 - x1, y2 - y1)
        lift = min(dist * 0.28, 100)
        cx, cy = mx, my - lift
        return [
            (int((1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t**2 * x2),
             int((1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t**2 * y2))
            for i in range(steps + 1)
            for t in [i / steps]
        ]

    def _rebuild_static(self, w: int, h: int) -> None:
        t = self._theme
        self.canvas.delete("static")
        self._ensure_map_photo(w, h)
        if self._map_photo:
            self.canvas.create_image(0, 0, anchor="nw", image=self._map_photo, tags="static")
        self.canvas.create_rectangle(0, 0, w, h, fill="", outline=t.map_border, width=2, tags="static")
        self.canvas.create_rectangle(0, h - 32, w, h, fill="#000000", outline="", tags="static")
        self.canvas.create_text(
            12, h - 10,
            text=f"NODES {len(CITIES)}  │  LINKS {len(self._connections)}  │  LATENCY 12ms avg  │  STATUS: MONITORING",
            fill=t.map_hud, font=("Consolas", 10), anchor="w", tags="static",
        )
        self._static_size = (w, h)

    def _draw_anim(self, w: int, h: int) -> None:
        self.canvas.delete("anim")
        t = self._theme
        self._scan_y = (self._scan_y + 3) % h
        self.canvas.create_line(0, self._scan_y, w, self._scan_y, fill=t.map_scan, width=2, tags="anim")

        major = {"New York", "London", "Tokyo", "Moscow", "Beijing", "Sydney", "Dubai", "Singapore"}
        pulse_r = 8 + int(4 * math.sin(self._pulse))
        steps = 24 if w > 1200 else 30

        for conn in self._connections:
            a, b = conn["from"], conn["to"]
            x1, y1 = self._city_to_xy(a, w, h)
            x2, y2 = self._city_to_xy(b, w, h)
            pts = self._curve_points(x1, y1, x2, y2, steps=steps)
            flat = [c for p in pts for c in p]
            self.canvas.create_line(*flat, fill="#003322", width=5, smooth=True, tags="anim")
            self.canvas.create_line(
                *flat, fill=conn["color"], width=2,
                dash=(10, 7), dashoffset=self._dash_offset, smooth=True, tags="anim",
            )
            conn["progress"] = (conn["progress"] + conn["speed"]) % 1.0
            idx = int(conn["progress"] * (len(pts) - 1))
            px, py = pts[idx]
            self.canvas.create_oval(px - 5, py - 5, px + 5, py + 5, outline=conn["color"], width=1, tags="anim")
            for pkt in conn["packets"]:
                pkt["t"] = (pkt["t"] + conn["speed"] * 1.8) % 1.0
                pidx = int(pkt["t"] * (len(pts) - 1))
                qx, qy = pts[pidx]
                self.canvas.create_oval(qx - 2, qy - 2, qx + 2, qy + 2, fill=conn["color"], outline="", tags="anim")

        for city in CITIES:
            x, y = self._city_to_xy(city, w, h)
            is_major = city["name"] in major
            r = pulse_r if is_major else 5
            self.canvas.create_oval(x - r, y - r, x + r, y + r, outline=t.map_node, width=1, tags="anim")
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=t.map_node_fill, outline="", tags="anim")
            if is_major:
                self.canvas.create_text(
                    x + 10, y - 6, text=city["name"].upper(),
                    fill=t.map_label, font=("Consolas", 9, "bold"), anchor="w", tags="anim",
                )

    def _draw(self) -> None:
        rw = max(self.canvas.winfo_width(), 500)
        rh = max(self.canvas.winfo_height(), 280)
        w, h = clamp_dims(rw, rh)
        if (w, h) != self._static_size:
            self.canvas.delete("all")
            self._rebuild_static(w, h)
        self._draw_anim(w, h)

    def _animate(self) -> None:
        if not self._running:
            return
        self._pulse += 0.12
        self._dash_offset = (self._dash_offset + 3) % 24
        self._draw()
        self.after(66, self._animate)

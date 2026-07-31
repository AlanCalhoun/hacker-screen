"""IP geolocation trace — street map with static layer caching."""

from __future__ import annotations

import math
import tkinter as tk

from PIL import ImageEnhance, ImageTk

from hacker_screen.data.console_themes import ConsoleTheme
from hacker_screen.effects.perf import fast_resize
from hacker_screen.effects.tactical_imagery import DEFAULT_TARGET, render_street_map, street_map_pin_fraction

TARGET = {
    "ip": "185.220.101.47",
    "hostname": "exit-relay-47.tor-exit.net",
    "address": DEFAULT_TARGET.address,
    "city": DEFAULT_TARGET.city_line,
    "country": "United States",
    "isp": "Portland Fiber Co-op",
    "asn": "AS 394256",
    "lat": 45.5122,
    "lon": -122.6536,
}


class IpTraceMapPanel(tk.Frame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        bg = theme.inner_bg
        super().__init__(master, bg=bg, **kwargs)
        self._theme = theme
        self._running = False
        self._pulse = 0.0
        self._trace_progress = 0.0
        self._static_photo: ImageTk.PhotoImage | None = None
        self._layout_size: tuple[int, int, int, int] = (0, 0, 0, 0)  # w, h, map_top, map_bot
        self._pin_xy: tuple[int, int] = (0, 0)
        self._resize_after: str | None = None

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_resize)

    def _layout(self, w: int, h: int) -> tuple[int, int, int, int]:
        banner, footer = 56, 58
        return 0, banner, w, h - footer

    def _canvas_dims(self) -> tuple[int, int] | None:
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 2 or h <= 2:
            return None
        return w, h

    def _rebuild_static(self, w: int, h: int) -> None:
        _, map_top, _, map_bot = self._layout(w, h)
        mh = max(map_bot - map_top, 120)
        base = render_street_map(w, mh, seed=742, target=DEFAULT_TARGET)
        if base.size != (w, mh):
            base = fast_resize(base, w, mh)
        base = ImageEnhance.Contrast(base).enhance(1.08)
        self._static_photo = ImageTk.PhotoImage(base)

        t = self._theme
        self.canvas.delete("all")
        self.canvas.configure(scrollregion=(0, 0, w, h))
        self.canvas.create_rectangle(0, 0, w, h, fill="#010806", outline="", tags="static")
        if self._static_photo:
            self.canvas.create_image(0, map_top, anchor="nw", image=self._static_photo, tags="static")

        pnx, pny = street_map_pin_fraction(w, mh)
        self._pin_xy = (int(pnx * w), map_top + int(pny * mh))

        self.canvas.create_rectangle(0, 0, w, map_top, fill="#010806", outline="", tags="static")
        self.canvas.create_line(0, map_top - 1, w, map_top - 1, fill=t.map_border, tags="static")
        self.canvas.create_text(14, 14, anchor="w", text="TARGET IP", fill=t.label_muted, font=("Consolas", 9), tags="static")
        self.canvas.create_text(14, 36, anchor="w", text=TARGET["ip"], fill=t.accent2, font=("Consolas", 20, "bold"), tags="static")
        self.canvas.create_text(
            w - 14, 36, anchor="e", text=f"PTR  {TARGET['hostname']}",
            fill=t.map_hud, font=("Consolas", 10), tags="static",
        )
        self.canvas.create_rectangle(0, map_bot, w, h, fill="#010806", outline="", tags="static")
        self.canvas.create_line(0, map_bot, w, map_bot, fill=t.map_border, tags="static")
        self.canvas.create_text(
            14, map_bot + 18, anchor="w",
            text=f"▶  {TARGET['address'].upper()}, {TARGET['city'].upper()}",
            fill=t.accent2, font=("Consolas", 12, "bold"), tags="static",
        )
        self.canvas.create_text(
            14, map_bot + 38, anchor="w",
            text=f"GEO  {TARGET['lat']:.4f}°N {abs(TARGET['lon']):.4f}°W  │  {TARGET['isp']}  {TARGET['asn']}",
            fill=t.map_hud, font=("Consolas", 9), tags="static",
        )
        self.canvas.create_text(
            14, map_bot + 52, anchor="w",
            text="STREET-LEVEL LOCK  │  WHOIS MATCH  │  SANCTIONS CROSS-REF ACTIVE",
            fill=t.label_muted, font=("Consolas", 9), tags="static",
        )
        self.canvas.create_rectangle(0, 0, w, h, fill="", outline=t.map_border, width=2, tags="static")
        self._layout_size = (w, h, map_top, map_bot)

    def start(self) -> None:
        self._running = True
        self._paint()
        self._animate()

    def stop(self) -> None:
        self._running = False
        if self._resize_after:
            self.after_cancel(self._resize_after)
            self._resize_after = None

    def _on_resize(self, event=None) -> None:
        if event is not None and event.widget is not self.canvas:
            return
        self._layout_size = (0, 0, 0, 0)
        if self._resize_after:
            self.after_cancel(self._resize_after)
        self._resize_after = self.after(80, self._paint)

    def _draw_anim(self) -> None:
        if not self._layout_size[0]:
            return
        w, h, map_top, map_bot = self._layout_size
        self.canvas.delete("anim")
        t = self._theme
        tx, ty = self._pin_xy
        sx, sy = 40, map_bot - 16
        prog = min(1.0, self._trace_progress)
        if prog > 0.05:
            pts: list[float] = []
            for i in range(16):
                frac = prog * (i / 15)
                pts.extend([sx + (tx - sx) * frac, sy + (ty - sy) * frac - math.sin(frac * math.pi) * 20])
            self.canvas.create_line(*pts, fill="#0a3020", width=5, smooth=True, tags="anim")
            self.canvas.create_line(*pts, fill=t.accent, width=2, dash=(6, 4), smooth=True, tags="anim")
        pr = 20 + int(4 * math.sin(self._pulse))
        self.canvas.create_oval(tx - pr, ty - pr, tx + pr, ty + pr, outline=t.accent2, width=1, dash=(4, 4), tags="anim")

    def _paint(self) -> None:
        dims = self._canvas_dims()
        if dims is None:
            return
        w, h = dims
        if (w, h) != self._layout_size[:2]:
            self._rebuild_static(w, h)
        self._draw_anim()

    def _animate(self) -> None:
        if not self._running:
            return
        self._pulse += 0.13
        self._trace_progress = (self._trace_progress + 0.012) % 1.35
        if self._trace_progress > 1.0:
            self._trace_progress = 0.0
        self._paint()
        self.after(66, self._animate)

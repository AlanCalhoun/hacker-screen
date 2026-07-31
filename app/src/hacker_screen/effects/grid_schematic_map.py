"""SCADA transmission grid schematic — substations and power lines."""

from __future__ import annotations

import math
import tkinter as tk

from hacker_screen.data.console_themes import ConsoleTheme


class TransmissionGridPanel(tk.Frame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        bg = theme.inner_bg
        super().__init__(master, bg=bg, **kwargs)
        self._theme = theme
        self._running = False
        self._pulse = 0.0
        self._flow = 0.0
        self._size: tuple[int, int] = (0, 0)
        self._nodes = [
            ("NP-01", 0.12, 0.38, "NUCLEAR"),
            ("SS-011", 0.30, 0.28, "345kV"),
            ("SS-014", 0.48, 0.22, "138kV"),
            ("SS-019", 0.68, 0.32, "138kV"),
            ("SS-022", 0.86, 0.48, "69kV"),
            ("WR-08", 0.22, 0.72, "WIND"),
            ("HD-03", 0.58, 0.78, "HYDRO"),
            ("TX-765", 0.78, 0.68, "765kV"),
        ]
        self._edges = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 1), (2, 6), (6, 3), (3, 7), (2, 7)]
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _e: setattr(self, "_size", (0, 0)))

    def _node_xy(self, idx: int, w: int, top: int, mh: int) -> tuple[int, int]:
        nx, ny = self._nodes[idx][1], self._nodes[idx][2]
        return int(nx * w), int(top + ny * mh)

    def _draw_tower(self, x: int, y: int, t: ConsoleTheme) -> None:
        self.canvas.create_line(x, y, x - 8, y - 22, fill=t.accent, width=2, tags="static")
        self.canvas.create_line(x, y, x + 8, y - 22, fill=t.accent, width=2, tags="static")
        self.canvas.create_line(x - 8, y - 22, x + 8, y - 22, fill=t.accent2, width=2, tags="static")
        self.canvas.create_line(x - 5, y - 16, x + 5, y - 16, fill=t.accent, width=1, tags="static")

    def _rebuild_static(self, w: int, h: int, top: int, bot: int, mh: int) -> None:
        t = self._theme
        self.canvas.delete("static")
        self.canvas.create_rectangle(0, top, w, bot, fill="#040806", outline="", tags="static")
        for by in (0.28, 0.52, 0.76):
            y = int(top + by * mh)
            self.canvas.create_line(16, y, w - 16, y, fill="#1a4030", width=5, tags="static")
            self.canvas.create_line(16, y, w - 16, y, fill=t.accent, width=1, dash=(14, 10), tags="static")
        for a, b in self._edges:
            x1, y1 = self._node_xy(a, w, top, mh)
            x2, y2 = self._node_xy(b, w, top, mh)
            mx = (x1 + x2) // 2
            pts = [x1, y1, mx, y1, mx, y2, x2, y2]
            self.canvas.create_line(*pts, fill="#0a2818", width=6, tags="static")
            self.canvas.create_line(*pts, fill=t.accent, width=2, tags="static")
        for i, (label, _nx, _ny, kv) in enumerate(self._nodes):
            x, y = self._node_xy(i, w, top, mh)
            is_nuclear = label == "NP-01"
            is_focus = label == "SS-014"
            r = 16 if is_nuclear else 14 + (3 if is_focus else 0)
            col = t.accent2 if is_focus or is_nuclear else t.map_node
            if is_nuclear:
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="#0a1810", outline=col, width=3, tags="static")
                self.canvas.create_text(x, y, text="☢", fill=col, font=("Consolas", 12, "bold"), tags="static")
            else:
                self.canvas.create_rectangle(
                    x - r, y - r, x + r, y + r,
                    fill="#0a1810", outline=col, width=3 if is_focus else 2, tags="static",
                )
            self.canvas.create_text(x, y - r - 10, text=label, fill=t.map_label, font=("Consolas", 9, "bold"), tags="static")
            self.canvas.create_text(x, y + r + 12, text=kv, fill=t.label_muted, font=("Consolas", 8), tags="static")
        for tx in (int(w * 0.38), int(w * 0.62)):
            self._draw_tower(tx, int(top + mh * 0.52), t)
        self.canvas.create_rectangle(0, 0, w, top, fill="#000000", outline="", tags="static")
        self.canvas.create_rectangle(0, bot, w, h, fill="#000000", outline="", tags="static")
        self.canvas.create_rectangle(0, 0, w, h, fill="", outline=t.map_border, width=2, tags="static")
        self._size = (w, h)

    def _draw_anim(self, w: int, top: int, mh: int) -> None:
        t = self._theme
        self.canvas.delete("anim")
        for a, b in self._edges:
            x1, y1 = self._node_xy(a, w, top, mh)
            x2, y2 = self._node_xy(b, w, top, mh)
            mx = (x1 + x2) // 2
            frac = (self._flow + a * 0.17) % 1.0
            if frac < 0.5:
                f = frac * 2
                qx, qy = int(x1 + (mx - x1) * f), y1
            else:
                f = (frac - 0.5) * 2
                qx, qy = mx, int(y1 + (y2 - y1) * f)
            self.canvas.create_oval(qx - 4, qy - 4, qx + 4, qy + 4, fill=t.accent2, outline="", tags="anim")
        x, y = self._node_xy(2, w, top, mh)
        pulse = int(3 * math.sin(self._pulse))
        self.canvas.create_oval(
            x - 22 - pulse, y - 22 - pulse, x + 22 + pulse, y + 22 + pulse,
            outline=t.map_scan, width=1, dash=(3, 4), tags="anim",
        )
        load = 2847 + int(40 * math.sin(self._pulse * 0.5))
        shed = int(self._pulse * 0.3) % 12 < 3
        status = "STAGE-2 LOAD SHED ACTIVE" if shed else "TRANSMISSION NOMINAL"
        self.canvas.create_text(
            10, 14, anchor="w",
            text=f"345kV BACKBONE  │  SS-014 MONITOR  │  GRID LOAD {load} MW",
            fill=t.map_hud, font=("Consolas", 10, "bold"), tags="anim",
        )
        self.canvas.create_text(
            w - 10, 14, anchor="e", text=f"765kV HVDC  │  {status}",
            fill=t.tag_colors.get("warn", "#ccaa44") if shed else t.map_hud,
            font=("Consolas", 9, "bold"), tags="anim",
        )
        self.canvas.create_text(
            10, self.canvas.winfo_height() - 14, anchor="w",
            text="138kV FEEDER BAY-7 CLOSED  │  RTU POLL 2s  │  IED TRIP DISABLED  │  SPINNING RESERVE 12%",
            fill=t.map_hud, font=("Consolas", 9), tags="anim",
        )

    def start(self) -> None:
        self._running = True
        self._animate()

    def stop(self) -> None:
        self._running = False

    def _paint(self) -> None:
        w = max(self.canvas.winfo_width(), 360)
        h = max(self.canvas.winfo_height(), 240)
        top, bot = 28, h - 28
        mh = bot - top
        if (w, h) != self._size:
            self.canvas.delete("all")
            self._rebuild_static(w, h, top, bot, mh)
        self._draw_anim(w, top, mh)

    def _animate(self) -> None:
        if not self._running:
            return
        self._pulse += 0.12
        self._flow = (self._flow + 0.025) % 1.0
        self._paint()
        self.after(80, self._animate)

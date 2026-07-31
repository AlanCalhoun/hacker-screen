"""Live operations panel — hex dumps, metrics, agency seals, endpoints."""

from __future__ import annotations

import random
import tkinter as tk
from datetime import datetime

import customtkinter as ctk

from hacker_screen.data.console_themes import ConsoleTheme
from hacker_screen.effects.seal_banner import SealBanner

SAT_STATIONS_DEFAULT = [
    ("Goldstone", "DSN-14", "California"),
    ("Madrid", "DSN-55", "Spain"),
    ("Canberra", "DSN-43", "Australia"),
    ("Weilheim", "GS-01", "Germany"),
]

ENDPOINTS_DEFAULT = [
    "core-rtr1.dc-east.net",
    "ixp-lon1.transit.net",
    "bgp-peer.tyo.backbone.jp",
    "mpls-gw.fra.tier1.de",
    "sat-uplink.us-west.mil",
    "mirror-span.sgp.ix",
]


class OpsPanel(ctk.CTkFrame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._endpoints = theme.endpoints or ENDPOINTS_DEFAULT
        self._sat_stations = theme.sat_stations or SAT_STATIONS_DEFAULT
        self._running = False
        self._graph_vals: list[float] = [random.uniform(0.2, 0.9) for _ in range(40)]
        self._sat_signals = [random.uniform(0.5, 0.95) for _ in self._sat_stations]

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)   # hex expands
        self.grid_rowconfigure(7, weight=1)   # bottom section expands

        ctk.CTkLabel(
            self,
            text=theme.ops_title,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.title_color,
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 4))

        seals_frame = ctk.CTkFrame(self, fg_color="transparent")
        seals_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=4)
        self.seal_banner = SealBanner(seals_frame)
        self.seal_banner.pack(fill="x")

        ctk.CTkLabel(
            self, text=theme.hex_title,
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=theme.label_muted, anchor="w",
        ).grid(row=2, column=0, sticky="ew", padx=10, pady=(6, 2))

        self.hex_box = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=theme.inner_bg,
            text_color=theme.label_muted,
            wrap="none",
            activate_scrollbars=False,
            border_width=1,
            border_color=theme.panel_border,
        )
        self.hex_box.grid(row=3, column=0, sticky="nsew", padx=10, pady=4)

        ctk.CTkLabel(
            self, text=theme.graph_title,
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=theme.label_muted, anchor="w",
        ).grid(row=4, column=0, sticky="ew", padx=10, pady=(4, 2))

        self.graph_canvas = tk.Canvas(
            self, bg=theme.inner_bg, height=64, highlightthickness=1,
            highlightbackground=theme.panel_border,
        )
        self.graph_canvas.grid(row=5, column=0, sticky="ew", padx=10, pady=4)

        metrics = ctk.CTkFrame(self, fg_color="transparent")
        metrics.grid(row=6, column=0, sticky="ew", padx=10, pady=2)
        self.bars: dict[str, ctk.CTkProgressBar] = {}
        for label in ("TUNNEL", "ENCRYPT", "ROUTE", "CAPTURE"):
            row = ctk.CTkFrame(metrics, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text=label, width=68,
                         font=ctk.CTkFont(family="Consolas", size=10),
                         text_color="#667788", anchor="w").pack(side="left")
            bar = ctk.CTkProgressBar(row, height=7, progress_color=theme.progress_color, fg_color="#1a2530")
            bar.pack(side="left", fill="x", expand=True, padx=(4, 0))
            bar.set(random.uniform(0.4, 0.85))
            self.bars[label] = bar

        # ── Expanded bottom section ──
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=7, column=0, sticky="nsew", padx=10, pady=(6, 8))
        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_columnconfigure(1, weight=1)
        bottom.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            bottom, text=theme.endpoints_title,
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=theme.label_muted, anchor="w",
        ).grid(row=0, column=0, sticky="w", pady=(0, 2))

        ctk.CTkLabel(
            bottom, text=theme.sat_title,
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=theme.label_muted, anchor="w",
        ).grid(row=0, column=1, sticky="w", padx=(8, 0), pady=(0, 2))

        self.endpoint_box = ctk.CTkTextbox(
            bottom,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=theme.inner_bg,
            text_color=theme.label_muted,
            wrap="none",
            activate_scrollbars=False,
            border_width=1,
            border_color=theme.panel_border,
        )
        self.endpoint_box.grid(row=1, column=0, sticky="nsew", pady=2)

        self.sat_canvas = tk.Canvas(
            bottom, bg=theme.inner_bg, highlightthickness=1,
            highlightbackground=theme.panel_border,
        )
        self.sat_canvas.grid(row=1, column=1, sticky="nsew", padx=(8, 0), pady=2)

        self.endpoint_box._textbox.tag_configure("ok", foreground=theme.accent)
        self.endpoint_box._textbox.tag_configure("warn", foreground=theme.tag_colors.get("warn", "#aa8844"))

        ctk.CTkLabel(
            self, text=theme.classification,
            font=ctk.CTkFont(family="Consolas", size=9),
            text_color="#445566",
        ).grid(row=8, column=0, pady=(0, 6))

    def start(self) -> None:
        self._running = True
        self.seal_banner.start()
        self._append_hex_block()
        self._append_endpoint()
        self._tick_graph()
        self._tick_bars()
        self._tick_sat()

    def stop(self) -> None:
        self._running = False
        self.seal_banner.stop()

    def _append_hex_block(self) -> None:
        if not self._running:
            return
        ts = datetime.now().strftime("%H:%M:%S")
        offset = random.randint(0x7FF00000, 0x7FFFFFFF)
        lines = [f"[{ts}] OFFSET 0x{offset:08X}"]
        for i in range(4):
            addr = offset + i * 16
            words = " ".join(f"{random.randint(0, 255):02X}" for _ in range(16))
            ascii_part = "".join(
                chr(c) if 32 <= c < 127 else "."
                for c in [random.randint(0, 255) for _ in range(16)]
            )
            lines.append(f"{addr:08X}  {words}  |{ascii_part}|")

        self.hex_box.configure(state="normal")
        for line in lines:
            self.hex_box._textbox.insert("end", line + "\n")
        self.hex_box._textbox.see("end")
        total = int(self.hex_box._textbox.index("end-1c").split(".")[0])
        if total > 100:
            self.hex_box._textbox.delete("1.0", f"{total - 70}.0")
        self.hex_box.configure(state="disabled")
        self.after(random.randint(200, 450), self._append_hex_block)

    def _append_endpoint(self) -> None:
        if not self._running:
            return
        host = random.choice(self._endpoints)
        ip = f"{random.randint(10,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        port = random.choice([22, 80, 443, 179, 8080, 8443])
        status = random.choice(["OK", "OK", "OK", "TIMEOUT"])
        tag = "ok" if status == "OK" else "warn"
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"{ts}  {host:<28} {ip}:{port}  {status}\n"

        self.endpoint_box.configure(state="normal")
        self.endpoint_box._textbox.insert("end", line, tag)
        self.endpoint_box._textbox.see("end")
        total = int(self.endpoint_box._textbox.index("end-1c").split(".")[0])
        if total > 60:
            self.endpoint_box._textbox.delete("1.0", f"{total - 40}.0")
        self.endpoint_box.configure(state="disabled")
        self.after(random.randint(600, 1400), self._append_endpoint)

    def _tick_graph(self) -> None:
        if not self._running:
            return
        self._graph_vals.pop(0)
        self._graph_vals.append(random.uniform(0.15, 0.95))
        self._draw_graph()
        self.after(150, self._tick_graph)

    def _draw_graph(self) -> None:
        c = self.graph_canvas
        t = self._theme
        c.delete("all")
        w = max(c.winfo_width(), 200)
        h = max(c.winfo_height(), 64)
        c.create_rectangle(0, 0, w, h, fill=t.inner_bg, outline="")
        n = len(self._graph_vals)
        if n < 2:
            return
        step = w / (n - 1)
        pts = []
        for i, v in enumerate(self._graph_vals):
            pts.extend([i * step, h - v * (h - 8) - 4])
        c.create_line(*pts, fill=t.graph_line, width=2, smooth=True)
        fill_pts = pts + [w, h, 0, h]
        c.create_polygon(fill_pts, fill=t.graph_fill, outline="")
        c.create_line(*pts, fill=t.graph_line, width=2, smooth=True)

    def _tick_bars(self) -> None:
        if not self._running:
            return
        for bar in self.bars.values():
            bar.set(max(0.1, min(0.98, bar.get() + random.uniform(-0.08, 0.08))))
        self.after(600, self._tick_bars)

    def _tick_sat(self) -> None:
        if not self._running:
            return
        self._sat_signals = [
            max(0.2, min(0.99, s + random.uniform(-0.05, 0.05)))
            for s in self._sat_signals
        ]
        self._draw_sat()
        self.after(900, self._tick_sat)

    def _draw_sat(self) -> None:
        c = self.sat_canvas
        t = self._theme
        c.delete("all")
        w = max(c.winfo_width(), 160)
        h = max(c.winfo_height(), 100)
        c.create_rectangle(0, 0, w, h, fill=t.inner_bg, outline="")

        row_h = max(22, h // max(len(self._sat_stations), 1))
        for i, (site, code, loc) in enumerate(self._sat_stations):
            y = 6 + i * row_h
            sig = self._sat_signals[i]
            c.create_text(6, y, text=code, fill="#8899aa",
                          font=("Consolas", 9, "bold"), anchor="nw")
            c.create_text(6, y + 12, text=f"{site}, {loc}", fill="#556677",
                          font=("Consolas", 7), anchor="nw")
            bx, bw = 6, w - 16
            by = y + 24
            c.create_rectangle(bx, by, bx + bw, by + 5, fill="#1a2530", outline="")
            color = t.progress_color if sig > 0.6 else t.tag_colors.get("warn", "#886644")
            c.create_rectangle(bx, by, bx + int(bw * sig), by + 5, fill=color, outline="")
            c.create_text(w - 6, y + 4, text=f"{int(sig * 100)}%",
                          fill=color, font=("Consolas", 8), anchor="ne")

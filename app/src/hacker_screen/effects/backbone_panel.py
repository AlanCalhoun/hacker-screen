"""Active BGP routes and backbone session monitor — sits below the world map."""

from __future__ import annotations

import random
import tkinter as tk
from datetime import datetime

import customtkinter as ctk

from hacker_screen.data.console_themes import ConsoleTheme

PEERS = [
    ("AS7018", "AT&T Backbone", "New York"),
    ("AS1299", "Telia Carrier", "London"),
    ("AS3356", "Lumen", "Chicago"),
    ("AS174", "Cogent", "Washington"),
    ("AS6939", "Hurricane Electric", "Fremont"),
    ("AS5511", "Orange OpenTransit", "Paris"),
    ("AS2914", "NTT Communications", "Tokyo"),
    ("AS3257", "GTT Backbone", "Frankfurt"),
    ("AS3491", "PCCW Global", "Hong Kong"),
    ("AS6453", "TATA Communications", "Mumbai"),
]

PROTOCOLS = ["BGP4", "OSPF", "MPLS", "GRE", "IPsec"]


class BackbonePanel(ctk.CTkFrame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text=f"◈  {theme.backbone_title}",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.label_muted,
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(8, 4))

        ctk.CTkLabel(
            self,
            text=f"◈  {theme.tunnels_title}",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.label_muted,
            anchor="w",
        ).grid(row=0, column=1, sticky="w", padx=10, pady=(8, 4))

        route_frame = ctk.CTkFrame(
            self, fg_color=theme.inner_bg, border_width=1, border_color=theme.panel_border,
        )
        route_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        route_frame.grid_rowconfigure(0, weight=1)
        route_frame.grid_columnconfigure(0, weight=1)

        self.route_box = ctk.CTkTextbox(
            route_frame,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=theme.inner_bg,
            text_color=theme.label_muted,
            wrap="none",
            activate_scrollbars=False,
        )
        self.route_box.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        self._setup_route_tags()

        # Tunnels canvas
        tunnel_frame = ctk.CTkFrame(
            self, fg_color=theme.inner_bg, border_width=1, border_color=theme.panel_border,
        )
        tunnel_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        tunnel_frame.grid_rowconfigure(0, weight=1)
        tunnel_frame.grid_columnconfigure(0, weight=1)

        self.tunnel_canvas = tk.Canvas(
            tunnel_frame, bg=theme.inner_bg, highlightthickness=0, bd=0,
        )
        self.tunnel_canvas.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        self._tunnels: list[dict] = []
        self._init_tunnels()

    def _setup_route_tags(self) -> None:
        tb = self.route_box._textbox
        t = self._theme
        tb.tag_configure("hdr", foreground="#556677")
        tb.tag_configure("ok", foreground=t.accent)
        tb.tag_configure("warn", foreground=t.tag_colors.get("warn", "#aa9955"))
        tb.tag_configure("new", foreground=t.accent2)

    def _init_tunnels(self) -> None:
        self._tunnels = []
        for i in range(6):
            self._tunnels.append({
                "name": f"TUN-{100 + i}",
                "proto": random.choice(PROTOCOLS),
                "endpoint": f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
                "load": random.uniform(0.2, 0.9),
                "latency": random.randint(8, 120),
            })

    def start(self) -> None:
        self._running = True
        self._write_route_header()
        self._append_route()
        self._draw_tunnels()
        self._tick_tunnels()

    def stop(self) -> None:
        self._running = False

    def _write_route_header(self) -> None:
        hdr = f"{'PEER':<8} {'NETWORK':<22} {'NEXT-HOP':<16} {'PREFIXES':>8}  STATUS\n"
        hdr += "─" * 62 + "\n"
        self.route_box.configure(state="normal")
        self.route_box._textbox.insert("end", hdr, "hdr")
        self.route_box.configure(state="disabled")

    def _append_route(self) -> None:
        if not self._running:
            return
        asn, name, city = random.choice(PEERS)
        prefix = f"{random.randint(1,223)}.{random.randint(0,255)}.0.0/16"
        hop = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        count = random.randint(120, 8900)
        status = random.choice(["ESTABLISHED", "ESTABLISHED", "ESTABLISHED", "FLapping"])
        tag = "ok" if status == "ESTABLISHED" else "warn"

        line = f"{asn:<8} {prefix:<22} {hop:<16} {count:>8}  {status}\n"
        self.route_box.configure(state="normal")
        self.route_box._textbox.insert("end", line, tag)
        self.route_box._textbox.see("end")
        total = int(self.route_box._textbox.index("end-1c").split(".")[0])
        if total > 80:
            self.route_box._textbox.delete("8.0", f"{total - 60}.0")
        self.route_box.configure(state="disabled")

        self.after(random.randint(400, 900), self._append_route)

    def _tick_tunnels(self) -> None:
        if not self._running:
            return
        for t in self._tunnels:
            t["load"] = max(0.1, min(0.98, t["load"] + random.uniform(-0.06, 0.06)))
            t["latency"] = max(5, min(200, t["latency"] + random.randint(-8, 8)))
        self._draw_tunnels()
        self.after(800, self._tick_tunnels)

    def _draw_tunnels(self) -> None:
        c = self.tunnel_canvas
        c.delete("all")
        w = max(c.winfo_width(), 180)
        h = max(c.winfo_height(), 120)
        c.create_rectangle(0, 0, w, h, fill=self._theme.inner_bg, outline="")

        row_h = max(28, h // max(len(self._tunnels), 1))
        for i, t in enumerate(self._tunnels):
            y = 8 + i * row_h
            c.create_text(8, y, text=t["name"], fill="#8899aa",
                          font=("Consolas", 9, "bold"), anchor="nw")
            c.create_text(58, y, text=t["proto"], fill="#667788",
                          font=("Consolas", 8), anchor="nw")
            c.create_text(8, y + 13, text=t["endpoint"], fill="#556677",
                          font=("Consolas", 8), anchor="nw")

            bar_x, bar_w = 8, w - 70
            bar_y = y + 24
            c.create_rectangle(bar_x, bar_y, bar_x + bar_w, bar_y + 6, fill="#1a2530", outline="")
            fill_w = bar_x + int(bar_w * t["load"])
            color = self._theme.progress_color if t["load"] < 0.75 else self._theme.tag_colors.get("warn", "#886644")
            c.create_rectangle(bar_x, bar_y, fill_w, bar_y + 6, fill=color, outline="")

            lat_color = self._theme.accent if t["latency"] < 50 else self._theme.tag_colors.get("warn", "#aa8844")
            c.create_text(w - 8, y + 10, text=f"{t['latency']}ms", fill=lat_color,
                          font=("Consolas", 9), anchor="ne")

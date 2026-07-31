"""Theme branding — stylized seals, utility logos, FX and grid monitors."""

from __future__ import annotations

import math
import random
import tkinter as tk
from datetime import datetime

import customtkinter as ctk

from hacker_screen.data.console_themes import ConsoleTheme


def _draw_fed_seal(c: tk.Canvas, cx: int, cy: int, r: int, theme: ConsoleTheme) -> None:
    """Stylized Federal Reserve emblem (original artwork, not an official seal)."""
    t = theme
    c.create_oval(cx - r, cy - r, cx + r, cy + r, outline=t.accent2, width=2, tags="seal")
    c.create_oval(cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8, outline=t.accent, width=1, tags="seal")
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        sx = cx + int((r - 4) * math.cos(ang))
        sy = cy + int((r - 4) * math.sin(ang))
        c.create_text(sx, sy, text="★", fill=t.accent2, font=("Consolas", 7), tags="seal")
    c.create_polygon(
        cx, cy - r // 3,
        cx - r // 4, cy + r // 5,
        cx - r // 8, cy + r // 4,
        cx, cy + r // 6,
        cx + r // 8, cy + r // 4,
        cx + r // 4, cy + r // 5,
        fill="", outline=t.accent2, width=2, tags="seal",
    )
    c.create_oval(cx - r // 6, cy - r // 8, cx + r // 6, cy + r // 4, outline=t.accent, width=1, tags="seal")
    c.create_text(cx, cy + r // 2 + 2, text="FEDERAL RESERVE", fill=t.accent2, font=("Consolas", 7, "bold"), tags="seal")
    c.create_text(cx, cy + r // 2 + 12, text="SYSTEM", fill=t.label_muted, font=("Consolas", 6, "bold"), tags="seal")


def _draw_cooling_towers(c: tk.Canvas, cx: int, base_y: int, scale: float, theme: ConsoleTheme) -> None:
    """Hyperbolic cooling towers + reactor dome."""
    t = theme
    tw = int(28 * scale)
    th = int(52 * scale)
    gap = int(18 * scale)
    for i, ox in enumerate((-gap - tw, gap)):
        x0, x1 = cx + ox, cx + ox + tw
        y0, y1 = base_y - th, base_y
        c.create_line(x0, y0, x0 + tw // 4, y0 + th // 3, fill=t.accent, width=2, tags="logo")
        c.create_line(x1, y0, x1 - tw // 4, y0 + th // 3, fill=t.accent, width=2, tags="logo")
        c.create_line(x0 + tw // 4, y0 + th // 3, x1 - tw // 4, y0 + th // 3, fill=t.accent, width=2, tags="logo")
        c.create_line(x0 + tw // 4, y0 + th // 3, x0 + tw // 3, y1, fill=t.accent, width=2, tags="logo")
        c.create_line(x1 - tw // 4, y0 + th // 3, x1 - tw // 3, y1, fill=t.accent, width=2, tags="logo")
        c.create_line(x0 + tw // 3, y1, x1 - tw // 3, y1, fill=t.accent2, width=2, tags="logo")
        for s in range(3):
            sx = x0 + tw // 2 + (s - 1) * 4
            c.create_line(sx, y0 - 4 - s * 6, sx + 3, y0 - 10 - s * 6, fill="#446655", width=1, tags="logo")
    dome_r = int(14 * scale)
    c.create_arc(cx - dome_r, base_y - th - dome_r, cx + dome_r, base_y - th + dome_r,
                 start=200, extent=140, style="arc", outline=t.accent2, width=2, tags="logo")
    c.create_line(cx - dome_r, base_y - th, cx + dome_r, base_y - th, fill=t.accent2, width=2, tags="logo")


class FedReserveBannerPanel(ctk.CTkFrame):
    """Federal Reserve System branding + live policy telemetry."""

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        self.canvas = tk.Canvas(self, bg=theme.inner_bg, highlightthickness=1,
                                highlightbackground=theme.panel_border, height=96)
        self.canvas.pack(fill="x", padx=8, pady=(8, 4))
        self.stats = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(family="Consolas", size=10),
            text_color=theme.map_hud, anchor="w",
        )
        self.stats.pack(fill="x", padx=10, pady=(0, 8))

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _paint_seal(self) -> None:
        c = self.canvas
        c.delete("all")
        w = max(c.winfo_width(), 280)
        h = max(c.winfo_height(), 80)
        c.configure(height=h)
        _draw_fed_seal(c, 52, h // 2, 36, self._theme)
        t = self._theme
        c.create_text(108, 18, anchor="w", text="BOARD OF GOVERNORS — WASHINGTON D.C.",
                      fill=t.label_muted, font=("Consolas", 8), tags="seal")
        c.create_text(108, 36, anchor="w", text="FEDERAL RESERVE SYSTEM",
                      fill=t.accent2, font=("Consolas", 13, "bold"), tags="seal")
        c.create_text(108, 56, anchor="w", text="FEDWIRE / CHIPS / NSS SETTLEMENT DESK",
                      fill=t.accent, font=("Consolas", 9), tags="seal")
        c.create_text(w - 8, h - 8, anchor="se", text="FRB-NY PRIMARY",
                      fill=t.label_muted, font=("Consolas", 8), tags="seal")

    def _tick(self) -> None:
        if not self._running:
            return
        self._paint_seal()
        ff = 5.25 + random.uniform(-0.02, 0.02)
        sofr = 5.31 + random.uniform(-0.03, 0.03)
        disc = 5.50
        self.stats.configure(
            text=f"FED FUNDS {ff:.2f}%  │  SOFR {sofr:.2f}%  │  DISCOUNT {disc:.2f}%  │  "
                 f"FEDWIRE VOL ${random.randint(820, 940)}B TODAY",
        )
        self.after(1200, self._tick)


class BankCorrespondentsPanel(ctk.CTkFrame):
    """Major correspondent banks — text wordmarks (no trademark logos)."""

    _BANKS = [
        ("JPMorgan Chase", "CHASUS33"),
        ("Bank of America", "BOFAUS3N"),
        ("Wells Fargo", "WFBIUS6S"),
        ("Citibank", "CITIUS33"),
        ("Goldman Sachs", "GOLDUS33"),
        ("HSBC", "MIDLGB22"),
    ]

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        ctk.CTkLabel(
            self, text="CORRESPONDENT BANKS", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(6, 2))
        self.grid_frame = ctk.CTkFrame(self, fg_color=theme.inner_bg, border_color=theme.panel_border, border_width=1)
        self.grid_frame.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        self._dots: list[ctk.CTkLabel] = []
        self._vols: list[ctk.CTkLabel] = []
        for i, (name, bic) in enumerate(self._BANKS):
            row = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
            row.pack(fill="x", padx=6, pady=2)
            dot = ctk.CTkLabel(row, text="●", width=16, text_color=theme.accent, font=ctk.CTkFont(size=12))
            dot.pack(side="left")
            self._dots.append(dot)
            ctk.CTkLabel(
                row, text=f"{name:<18} {bic}", anchor="w",
                font=ctk.CTkFont(family="Consolas", size=9), text_color=theme.label_muted,
            ).pack(side="left", fill="x", expand=True)
            vol = ctk.CTkLabel(row, text="$0M", width=52, font=ctk.CTkFont(family="Consolas", size=9),
                               text_color=theme.accent)
            vol.pack(side="right")
            self._vols.append(vol)

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        t = self._theme
        for dot, vol in zip(self._dots, self._vols):
            active = random.random() > 0.25
            dot.configure(text_color=t.accent2 if active else "#335544")
            if active:
                vol.configure(text=f"${random.randint(12, 890)}M")
        self.after(800, self._tick)


class ExchangeRatePanel(ctk.CTkFrame):
    """Live FX cross-rates."""

    _PAIRS = [
        ("EUR/USD", 1.0847, 0.12),
        ("GBP/USD", 1.2734, -0.08),
        ("USD/JPY", 149.82, 0.31),
        ("USD/CHF", 0.8812, -0.05),
        ("AUD/USD", 0.6621, 0.18),
        ("USD/CAD", 1.3589, -0.11),
        ("USD/CNY", 7.2456, 0.02),
        ("EUR/GBP", 0.8518, 0.09),
    ]

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        self._rates = {p: v for p, v, _ in self._PAIRS}
        ctk.CTkLabel(
            self, text="FX DESK — LIVE RATES", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(6, 2))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=theme.terminal_bg, text_color=theme.terminal_fg,
            border_color=theme.terminal_border, border_width=1, activate_scrollbars=False, height=120,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        self.text._textbox.tag_configure("up", foreground=theme.accent2)
        self.text._textbox.tag_configure("dn", foreground=theme.tag_colors.get("alert", "#cc6644"))

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        ts = datetime.now().strftime("%H:%M:%S")
        self.text.insert("end", f"  {ts} UTC  BLOOMBERG B-PIPE FEED\n\n")
        for pair, base, _ in self._PAIRS:
            drift = random.uniform(-0.0015, 0.0015)
            self._rates[pair] = max(0.0001, self._rates[pair] + drift)
            rate = self._rates[pair]
            chg = drift / base * 100 if base else 0
            tag = "up" if chg >= 0 else "dn"
            arrow = "▲" if chg >= 0 else "▼"
            self.text._textbox.insert(
                "end", f"  {pair:<10} {rate:>10.4f}  {arrow} {abs(chg):+.3f}%\n", tag,
            )
        self.text.configure(state="disabled")
        self.after(600, self._tick)


class FedWireTickerPanel(ctk.CTkFrame):
    """High-volume settlement stream."""

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        ctk.CTkLabel(
            self, text="FEDWIRE / SWIFT SETTLEMENTS", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(6, 2))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=theme.inner_bg, text_color=theme.label_muted,
            border_color=theme.panel_border, border_width=1, activate_scrollbars=False,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        self.text._textbox.tag_configure("large", foreground=theme.accent2)
        self.text._textbox.tag_configure("flag", foreground=theme.tag_colors.get("alert", "#cc8844"))

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        kind = random.choice(["FEDWIRE", "CHIPS", "SWIFT MT202", "ACH BATCH", "TIPS", "TARGET2"])
        amt = random.randint(50, 2500)
        ref = random.randint(10000000, 99999999)
        bank = random.choice(["FRB-NY", "JPM", "BOFA", "CITI", "DEUT", "UBS"])
        tag = "large" if amt > 500 else "flag" if random.random() < 0.15 else "info"
        line = f"{kind}  REF{ref}  ${amt}M  {bank}  SETTLED\n"
        self.text.configure(state="normal")
        self.text._textbox.insert("end", line, tag if tag != "info" else "")
        self.text._textbox.see("end")
        total = int(self.text._textbox.index("end-1c").split(".")[0])
        if total > 50:
            self.text._textbox.delete("1.0", f"{total - 35}.0")
        self.text.configure(state="disabled")
        self.after(random.randint(300, 900), self._tick)


class PowerUtilityLogoPanel(ctk.CTkFrame):
    """Fictional utility brand with nuclear cooling towers."""

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        self.canvas = tk.Canvas(self, bg=theme.inner_bg, highlightthickness=1,
                                highlightbackground=theme.panel_border, height=110)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=8)

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _paint(self) -> None:
        c = self.canvas
        c.delete("all")
        w = max(c.winfo_width(), 200)
        h = max(c.winfo_height(), 90)
        t = self._theme
        c.create_rectangle(0, 0, w, h, fill=t.inner_bg, outline="")
        scale = min(w / 320, h / 100, 1.2)
        _draw_cooling_towers(c, w // 2 - 40, h - 18, scale, t)
        c.create_text(w // 2 + 30, 22, text="CONTINENTAL GRID POWER", fill=t.accent2,
                      font=("Consolas", 12, "bold"), tags="logo")
        c.create_text(w // 2 + 30, 40, text="NUCLEAR · TRANSMISSION · SCADA", fill=t.accent,
                      font=("Consolas", 9), tags="logo")
        c.create_text(w // 2 + 30, 58, text="NERC REGION IV  │  3,847 MW ONLINE", fill=t.label_muted,
                      font=("Consolas", 8), tags="logo")
        load = 2847 + int(40 * math.sin(datetime.now().second * 0.5))
        c.create_text(w // 2 + 30, 74, text=f"SYSTEM LOAD {load} MW  │  345kV BACKBONE", fill=t.map_hud,
                      font=("Consolas", 8), tags="logo")

    def _tick(self) -> None:
        if not self._running:
            return
        self._paint()
        self.after(900, self._tick)


class BlackoutMonitorPanel(ctk.CTkFrame):
    """Rolling blackout and load-shed alerts."""

    _REGIONS = [
        "Sector 7A — Metro East", "Feeder North-765", "Substation SS-014",
        "Industrial Park Delta", "Residential Grid West", "HVDC Link B-2",
    ]

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        ctk.CTkLabel(
            self, text="⚠ BLACKOUT / LOAD SHED MONITOR", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=theme.tag_colors.get("warn", "#ccaa44"), anchor="w",
        ).pack(fill="x", padx=10, pady=(6, 2))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=theme.terminal_bg, text_color=theme.terminal_fg,
            border_color=theme.terminal_border, border_width=1, activate_scrollbars=False,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        self.text._textbox.tag_configure("crit", foreground=theme.tag_colors.get("alert", "#ccaa33"))
        self.text._textbox.tag_configure("warn", foreground=theme.tag_colors.get("warn", "#cccc44"))
        self.text._textbox.tag_configure("ok", foreground=theme.accent)

    def start(self) -> None:
        self._running = True
        for line, tag in [
            ("[STANDBY] Rolling blackout protocol ARMED — Stage 2", "warn"),
            ("[SHED] 847 MW dropped — Feeder North-765 OPEN", "crit"),
            ("[ISO] CAISO emergency order E-2026-014 active", "warn"),
            ("[RESTORE] Phase 1 complete — 38% capacity back", "ok"),
        ]:
            self.text._textbox.insert("end", line + "\n", tag)
        self.text.configure(state="disabled")
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        ts = datetime.now().strftime("%H:%M:%S")
        evt = random.choice([
            ("ROLLING BLACKOUT", "crit"), ("CIRCUIT OPEN", "crit"), ("LOAD SHED", "warn"),
            ("RESTORATION", "ok"), ("UNDER-FREQ", "warn"), ("SPINNING RESERVE", "ok"),
        ])
        region = random.choice(self._REGIONS)
        mw = random.randint(120, 920)
        tag = evt[1]
        line = f"[{ts}] {evt[0]}  {region}  — {mw} MW\n"
        self.text.configure(state="normal")
        self.text._textbox.insert("end", line, tag)
        self.text._textbox.see("end")
        total = int(self.text._textbox.index("end-1c").split(".")[0])
        if total > 35:
            self.text._textbox.delete("1.0", f"{total - 25}.0")
        self.text.configure(state="disabled")
        self.after(random.randint(1500, 3500), self._tick)


class RelayElectronicsPanel(ctk.CTkFrame):
    """Protection relay / IED register map — electronics feel."""

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        self._bits = [random.randint(0, 1) for _ in range(24)]
        ctk.CTkLabel(
            self, text="PROTECTION RELAY — IED MAP", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(6, 2))
        self.canvas = tk.Canvas(self, bg=theme.inner_bg, highlightthickness=1,
                                highlightbackground=theme.panel_border, height=100)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=(0, 6))

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _paint(self) -> None:
        c = self.canvas
        c.delete("all")
        w = max(c.winfo_width(), 180)
        h = max(c.winfo_height(), 80)
        t = self._theme
        labels = ["52A", "52B", "87T", "50/51", "27", "59", "81", "BF"]
        for i, lbl in enumerate(labels):
            x = 20 + (i % 4) * (w // 4)
            y = 20 + (i // 4) * 38
            on = self._bits[i % len(self._bits)]
            col = t.accent2 if on else "#334433"
            c.create_rectangle(x, y, x + 36, y + 22, outline=col, fill="#0a1810", width=2, tags="relay")
            c.create_text(x + 18, y + 11, text=lbl, fill=col, font=("Consolas", 8, "bold"), tags="relay")
            c.create_line(x + 40, y + 11, x + 56, y + 11, fill=t.panel_border, width=1, tags="relay")
            if i < 7:
                c.create_line(x + 56, y + 11, x + 56, y + 38, fill=t.panel_border, width=1, tags="relay")
        c.create_text(w - 8, h - 6, anchor="se", text="SEL-421  │  MODBUS 502  │  GOOSE",
                      fill=t.label_muted, font=("Consolas", 7), tags="relay")

    def _tick(self) -> None:
        if not self._running:
            return
        idx = random.randint(0, len(self._bits) - 1)
        self._bits[idx] = 1 - self._bits[idx]
        self._paint()
        self.after(400, self._tick)

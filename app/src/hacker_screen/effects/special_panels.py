"""Extra panels for non-netdefense dashboard layouts."""

from __future__ import annotations

import math
import random
import tkinter as tk
from datetime import datetime, timedelta

import customtkinter as ctk

from hacker_screen.data.console_themes import ConsoleTheme


class IncidentQueuePanel(ctk.CTkFrame):
    """Threat intercept — compact incident ticker."""

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        ctk.CTkLabel(
            self, text="INCIDENT QUEUE", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=theme.terminal_bg, text_color=theme.terminal_fg,
            border_color=theme.terminal_border, border_width=1,
            activate_scrollbars=False,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.text._textbox.tag_configure("crit", foreground=theme.accent2)
        self.text._textbox.tag_configure("warn", foreground=theme.tag_colors.get("warn", "#ccaa44"))

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        ts = datetime.now().strftime("%H:%M:%S")
        sev = random.choice(["crit", "crit", "warn", "warn", "info"])
        tag = "crit" if sev == "crit" else "warn" if sev == "warn" else "info"
        msg = random.choice([
            f"Trojan dropper on {random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
            f"C2 beacon interval 60s — callback active",
            f"YARA match APT-{random.randint(28,29)} cluster",
            f"Sandbox detonation score {random.randint(70,99)}/100",
            f"Credential dump lsass.exe PID {random.randint(1000,9999)}",
        ])
        line = f"{ts}  [{sev.upper()}]  {msg}\n"
        self.text.configure(state="normal")
        self.text._textbox.insert("end", line, tag if tag != "info" else "")
        self.text._textbox.see("end")
        total = int(self.text._textbox.index("end-1c").split(".")[0])
        if total > 80:
            self.text._textbox.delete("1.0", f"{total - 60}.0")
        self.text.configure(state="disabled")
        self.after(random.randint(400, 900), self._tick)


class TargetListPanel(ctk.CTkFrame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        ctk.CTkLabel(
            self, text="ACTIVE TARGETS", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=theme.inner_bg, text_color=theme.label_muted,
            border_color=theme.panel_border, border_width=1, activate_scrollbars=False,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.text._textbox.tag_configure("pwn", foreground=theme.accent2)
        self.text._textbox.tag_configure("scan", foreground=theme.tag_colors.get("warn", "#ccaa44"))

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        ip = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        st = random.choice(["PWNED", "PWNED", "BEACONING", "SCANNING"])
        tag = "pwn" if st == "PWNED" else "scan"
        self.text.configure(state="normal")
        self.text._textbox.insert("end", f"{ip:<22} {st}\n", tag)
        self.text._textbox.see("end")
        total = int(self.text._textbox.index("end-1c").split(".")[0])
        if total > 50:
            self.text._textbox.delete("1.0", f"{total - 35}.0")
        self.text.configure(state="disabled")
        self.after(random.randint(700, 1600), self._tick)


class PassSchedulePanel(ctk.CTkFrame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        ctk.CTkLabel(
            self, text="PASS SCHEDULE", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=theme.inner_bg, text_color=theme.label_muted,
            border_color=theme.panel_border, border_width=1, activate_scrollbars=False,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def start(self) -> None:
        self._running = True
        base = datetime.now()
        self.text.configure(state="normal")
        for i, name in enumerate(["NOAA-21", "ISS-ZARYA", "GOES-18", "HST"]):
            aos = base + timedelta(minutes=12 + i * 47)
            los = aos + timedelta(minutes=8 + i * 2)
            self.text._textbox.insert(
                "end",
                f"{name:<14} AOS {aos.strftime('%H:%M')}  LOS {los.strftime('%H:%M')}\n",
            )
        self.text.configure(state="disabled")
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        self.after(3000, self._tick)


class TelemetryStripPanel(ctk.CTkFrame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        ctk.CTkLabel(
            self, text="LIVE TELEMETRY", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=theme.terminal_bg, text_color=theme.terminal_fg,
            border_color=theme.terminal_border, border_width=1, activate_scrollbars=False,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        line = (
            f"TM {random.randint(100000,999999)}  APID={random.randint(1,2047)}  "
            f"SNR {random.randint(14,28)}dB  {random.randint(256,2048)}B\n"
        )
        self.text.configure(state="normal")
        self.text._textbox.insert("end", line)
        self.text._textbox.see("end")
        total = int(self.text._textbox.index("end-1c").split(".")[0])
        if total > 60:
            self.text._textbox.delete("1.0", f"{total - 40}.0")
        self.text.configure(state="disabled")
        self.after(random.randint(300, 700), self._tick)


class TrackedObjectsPanel(ctk.CTkFrame):
    """Orbital catalog — NORAD IDs and object status."""

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        ctk.CTkLabel(
            self, text="TRACKED OBJECTS", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=theme.inner_bg, text_color=theme.label_muted,
            border_color=theme.panel_border, border_width=1, activate_scrollbars=False,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.text._textbox.tag_configure("active", foreground=theme.accent2)
        self.text._textbox.tag_configure("idle", foreground=theme.label_muted)

    def start(self) -> None:
        self._running = True
        objects = [
            ("NOAA-21", "54234", "ACTIVE"),
            ("ISS-ZARYA", "25544", "ACTIVE"),
            ("GOES-18", "51850", "ACTIVE"),
            ("STARLINK-4821", "55061", "TRACK"),
            ("HST", "20580", "IDLE"),
            ("GPS-III-SV05", "43873", "TRACK"),
        ]
        self.text.configure(state="normal")
        for name, norad, st in objects:
            tag = "active" if st == "ACTIVE" else "idle"
            self.text._textbox.insert("end", f"{name:<16} {norad}  {st}\n", tag)
        self.text.configure(state="disabled")
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        name = random.choice(["DEBRIS-014", "COSMOS-1408", "SL-16 R/B", "NOAA-20"])
        self.text.configure(state="normal")
        self.text._textbox.insert(
            "end", f"{name:<16} {random.randint(40000,99999)}  NEW\n", "idle",
        )
        self.text._textbox.see("end")
        total = int(self.text._textbox.index("end-1c").split(".")[0])
        if total > 40:
            self.text._textbox.delete("1.0", f"{total - 30}.0")
        self.text.configure(state="disabled")
        self.after(random.randint(2000, 4000), self._tick)


class GroundStationPanel(ctk.CTkFrame):
    """DSN / ground station link status."""

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        self._stations = [
            ("Goldstone DSN-14", 94),
            ("Canberra DSN-43", 88),
            ("Madrid DSN-55", 72),
            ("Svalbard GS", 91),
            ("Weilheim GS-01", 65),
        ]
        ctk.CTkLabel(
            self, text="GROUND STATION LINKS", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
        self.frame = ctk.CTkFrame(self, fg_color=theme.inner_bg, border_color=theme.panel_border, border_width=1)
        self.frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._bars: list[ctk.CTkProgressBar] = []
        self._labels: list[ctk.CTkLabel] = []
        for name, snr in self._stations:
            row = ctk.CTkFrame(self.frame, fg_color="transparent")
            row.pack(fill="x", padx=8, pady=4)
            ctk.CTkLabel(
                row, text=name, font=ctk.CTkFont(family="Consolas", size=10),
                text_color=theme.label_muted, anchor="w", width=140,
            ).pack(side="left")
            bar = ctk.CTkProgressBar(row, height=10, progress_color=theme.accent)
            bar.pack(side="left", fill="x", expand=True, padx=(4, 8))
            bar.set(snr / 100)
            self._bars.append(bar)
            lbl = ctk.CTkLabel(
                row, text=f"{snr}%", font=ctk.CTkFont(family="Consolas", size=10),
                text_color=theme.accent, width=36,
            )
            lbl.pack(side="right")
            self._labels.append(lbl)

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        for bar, lbl in zip(self._bars, self._labels):
            v = max(0.35, min(0.99, bar.get() + random.uniform(-0.08, 0.08)))
            bar.set(v)
            lbl.configure(text=f"{int(v * 100)}%")
        self.after(900, self._tick)


class OrbitalTlePanel(ctk.CTkFrame):
    """Two-line element set readout for active pass."""

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        ctk.CTkLabel(
            self, text="ACTIVE TLE — NOAA-21", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=9),
            fg_color=theme.terminal_bg, text_color=theme.terminal_fg,
            border_color=theme.terminal_border, border_width=1, activate_scrollbars=False, height=72,
        )
        self.text.pack(fill="x", padx=8, pady=(0, 8))
        self.text.insert("1.0", "1 54234U 23057A   24212.45678901  .00000012  00000+0  12345-4 0  999\n")
        self.text.insert("end", "2 54234  98.7123  45.6789 0012345 123.4567 236.7890 14.19555555000001")
        self.text.configure(state="disabled")


class GaugeBoardPanel(ctk.CTkFrame):
    """SCADA-style gauge row."""

    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        self._vals = [random.uniform(0.35, 0.85) for _ in range(4)]
        self._labels = ["FREQUENCY Hz", "LOAD MW", "VOLTAGE kV", "REACTOR %"]
        self._canvas = tk.Canvas(self, bg=theme.inner_bg, highlightthickness=0, height=120)
        self._canvas.pack(fill="both", expand=True, padx=8, pady=8)

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        self._vals = [max(0.15, min(0.95, v + random.uniform(-0.06, 0.06))) for v in self._vals]
        self._paint()
        self.after(500, self._tick)

    def _paint(self) -> None:
        c = self._canvas
        c.delete("all")
        t = self._theme
        w = max(c.winfo_width(), 400)
        h = max(c.winfo_height(), 100)
        c.create_rectangle(0, 0, w, h, fill=t.inner_bg, outline="")
        gw = w // 4
        for i, (lbl, val) in enumerate(zip(self._labels, self._vals)):
            cx = gw * i + gw // 2
            c.create_text(cx, 18, text=lbl, fill=t.label_muted, font=("Consolas", 10, "bold"))
            c.create_arc(cx - 50, 30, cx + 50, 110, start=180, extent=180, outline=t.panel_border, width=2, style="arc")
            angle = 180 - int(val * 180)
            rad = angle * 3.14159 / 180
            c.create_line(cx, 70, cx + int(45 * math.cos(rad)), 70 - int(45 * math.sin(rad)), fill=t.accent2, width=3)
            c.create_text(cx, 100, text=f"{val * 100:.0f}%", fill=t.accent, font=("Consolas", 11, "bold"))


class TransactionTickerPanel(ctk.CTkFrame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        ctk.CTkLabel(
            self, text="WIRE TRANSFERS", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.accent2, anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=theme.terminal_bg, text_color=theme.terminal_fg,
            border_color=theme.terminal_border, border_width=1, activate_scrollbars=False,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.text._textbox.tag_configure("flag", foreground=theme.tag_colors.get("alert", "#cc8844"))
        self.text._textbox.tag_configure("ok", foreground=theme.accent)

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        amt = random.randint(10, 999)
        ref = random.randint(100000, 999999)
        bank = random.choice(["JPM", "BOFA", "Wells", "CITI", "HSBC", "FRB-NY"])
        ccy = random.choice(["USD", "EUR", "GBP", "CHF", "JPY"])
        st = random.choice(["OK", "OK", "FLAG", "HOLD"])
        tag = "flag" if st in ("FLAG", "HOLD") else "ok"
        line = f"MT103  {bank}  {ccy}  REF{ref}  ${amt},{random.randint(10,99):02d}K  {st}\n"
        self.text.configure(state="normal")
        self.text._textbox.insert("end", line, tag)
        self.text._textbox.see("end")
        total = int(self.text._textbox.index("end-1c").split(".")[0])
        if total > 70:
            self.text._textbox.delete("1.0", f"{total - 50}.0")
        self.text.configure(state="disabled")
        self.after(random.randint(500, 1200), self._tick)


class MarketGraphPanel(ctk.CTkFrame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        self._vals = [random.uniform(0.3, 0.7) for _ in range(50)]
        ctk.CTkLabel(
            self, text="VOLUME INDEX", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.label_muted, anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
        self.canvas = tk.Canvas(self, bg=theme.inner_bg, highlightthickness=1, highlightbackground=theme.panel_border)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        self._vals.pop(0)
        self._vals.append(random.uniform(0.2, 0.9))
        self._paint()
        self.after(200, self._tick)

    def _paint(self) -> None:
        c = self.canvas
        c.delete("all")
        t = self._theme
        w = max(c.winfo_width(), 200)
        h = max(c.winfo_height(), 80)
        step = w / max(len(self._vals) - 1, 1)
        pts = []
        for i, v in enumerate(self._vals):
            pts.extend([i * step, h - v * (h - 10) - 5])
        if len(pts) >= 4:
            c.create_line(*pts, fill=t.accent2, width=2, smooth=True)


class FlaggedAccountsPanel(ctk.CTkFrame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False
        ctk.CTkLabel(
            self, text="FLAGGED ACCOUNTS", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=theme.label_muted, anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))
        self.text = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=theme.inner_bg, text_color=theme.label_muted,
            border_color=theme.panel_border, border_width=1, activate_scrollbars=False,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.text._textbox.tag_configure("flag", foreground=theme.tag_colors.get("alert", "#cc8844"))

    def start(self) -> None:
        self._running = True
        self._tick()

    def stop(self) -> None:
        self._running = False

    def _tick(self) -> None:
        if not self._running:
            return
        acct = f"****{random.randint(1000,9999)}"
        score = random.randint(85, 99)
        self.text.configure(state="normal")
        self.text._textbox.insert("end", f"OFAC {score}%  {acct}  SANCTIONS MATCH\n", "flag")
        self.text._textbox.see("end")
        total = int(self.text._textbox.index("end-1c").split(".")[0])
        if total > 40:
            self.text._textbox.delete("1.0", f"{total - 25}.0")
        self.text.configure(state="disabled")
        self.after(random.randint(900, 2000), self._tick)

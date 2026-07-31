"""Themed operations console — each theme uses a distinct dashboard layout."""

from __future__ import annotations

import random
from collections.abc import Callable

import customtkinter as ctk

from hacker_screen.data.console_themes import ConsoleTheme
from hacker_screen.effects.brand_panels import (
    BankCorrespondentsPanel,
    BlackoutMonitorPanel,
    ExchangeRatePanel,
    FedReserveBannerPanel,
    FedWireTickerPanel,
    PowerUtilityLogoPanel,
    RelayElectronicsPanel,
)
from hacker_screen.effects.backbone_panel import BackbonePanel
from hacker_screen.effects.ops_panel import OpsPanel
from hacker_screen.effects.special_panels import (
    FlaggedAccountsPanel,
    GaugeBoardPanel,
    GroundStationPanel,
    IncidentQueuePanel,
    MarketGraphPanel,
    OrbitalTlePanel,
    PassSchedulePanel,
    TargetListPanel,
    TelemetryStripPanel,
    TrackedObjectsPanel,
    TransactionTickerPanel,
)
from hacker_screen.effects.terminal_feed import TerminalFeed
from hacker_screen.effects.video_feed import VideoFeedPanel
from hacker_screen.effects.world_map import WorldMapPanel
from hacker_screen.effects.orbital_track_map import OrbitalTrackPanel
from hacker_screen.effects.grid_schematic_map import TransmissionGridPanel
from hacker_screen.effects.ip_trace_map import IpTraceMapPanel
from hacker_screen.paths import apply_window_icon

DEFAULT_W, DEFAULT_H = 1360, 900
MIN_W, MIN_H = 1000, 680


def _panel_style(theme: ConsoleTheme) -> dict:
    return {
        "border_width": 1,
        "border_color": theme.panel_border,
        "fg_color": theme.panel_fg,
        "corner_radius": 6,
    }


class ConsoleWindow:
    """A standalone themed dashboard in a new top-level window."""

    _open_count = 0

    def __init__(
        self,
        parent: ctk.CTk,
        theme: ConsoleTheme,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        self.theme = theme
        self._on_close = on_close
        self._running = True
        self._widgets: list = []

        ConsoleWindow._open_count += 1
        offset = (ConsoleWindow._open_count - 1) * 36

        self.window = ctk.CTkToplevel(parent)
        self.window.title(theme.window_title)
        self.window.configure(fg_color=theme.bg)
        self.window.minsize(MIN_W, MIN_H)
        self.window.resizable(True, True)

        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = max(0, (sw - DEFAULT_W) // 2 + offset)
        y = max(0, (sh - DEFAULT_H) // 2 + offset)
        self.window.geometry(f"{DEFAULT_W}x{DEFAULT_H}+{x}+{y}")

        apply_window_icon(self.window)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.bind("<Escape>", self.close)

        builders = {
            "netdefense": self._build_netdefense,
            "threatwatch": self._build_threatwatch,
            "orbital": self._build_orbital,
            "ledger": self._build_ledger,
            "gridops": self._build_gridops,
        }
        builders.get(theme.id, self._build_netdefense)()
        self.window.after(300, self._start_effects)

    def _track(self, widget) -> None:
        self._widgets.append(widget)

    def _place(self, widget, **grid_kw) -> None:
        self._track(widget)
        widget.grid(**grid_kw)

    def _header(self, root: ctk.CTk, cols: int = 1) -> None:
        t = self.theme
        header = ctk.CTkFrame(root, fg_color=t.header_bg, height=46, corner_radius=0)
        header.grid(row=0, column=0, columnspan=cols, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            header, text=f"◆  {t.header_title}",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color=t.title_color,
        ).grid(row=0, column=0, padx=16, pady=10)
        self.status_label = ctk.CTkLabel(
            header, text=f"● LIVE — {t.status_live}",
            font=ctk.CTkFont(family="Consolas", size=12), text_color=t.accent,
        )
        self.status_label.grid(row=0, column=1, pady=10)
        ctk.CTkButton(
            header, text="Close", width=96, height=28,
            fg_color=t.btn_fg, hover_color=t.btn_hover, text_color="#99aabb",
            font=ctk.CTkFont(family="Consolas", size=11), command=self.close,
        ).grid(row=0, column=2, padx=16, pady=10)

    def _footer(self, root: ctk.CTk, cols: int = 1) -> None:
        t = self.theme
        stats = ctk.CTkFrame(root, fg_color=t.header_bg, height=30, corner_radius=0)
        stats.grid(row=2, column=0, columnspan=cols, sticky="ew")
        self.stats_label = ctk.CTkLabel(
            stats, text="", font=ctk.CTkFont(family="Consolas", size=10), text_color=t.label_muted,
        )
        self.stats_label.pack(pady=7)
        self._animate_stats()

    # ── Original layout (unchanged) ──

    def _build_netdefense(self) -> None:
        t = self.theme
        root = self.window
        ps = _panel_style(t)
        root.grid_columnconfigure(0, weight=34)
        root.grid_columnconfigure(1, weight=40)
        root.grid_columnconfigure(2, weight=26)
        root.grid_rowconfigure(1, weight=1)
        self._header(root, 3)

        left = ctk.CTkFrame(root, fg_color="transparent")
        left.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=(8, 6))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(0, weight=2)
        left.grid_rowconfigure(1, weight=3, minsize=240)

        self.terminal = TerminalFeed(left, t, **ps)
        self._place(self.terminal, row=0, column=0, sticky="nsew", pady=(0, 4))
        self.video_feed = VideoFeedPanel(left, t, **ps)
        self._place(self.video_feed, row=1, column=0, sticky="nsew", pady=(4, 0))

        center = ctk.CTkFrame(root, fg_color="transparent")
        center.grid(row=1, column=1, sticky="nsew", padx=6, pady=(8, 6))
        center.grid_columnconfigure(0, weight=1)
        center.grid_rowconfigure(0, weight=1)
        center.grid_rowconfigure(1, weight=1)

        map_wrap = ctk.CTkFrame(center, **ps)
        map_wrap.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        map_wrap.grid_rowconfigure(1, weight=1)
        map_wrap.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            map_wrap, text=f"◈  {t.map_title}",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=t.label_muted, anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(6, 2))
        self.world_map = WorldMapPanel(map_wrap, t)
        self._place(self.world_map, row=1, column=0, sticky="nsew", padx=4, pady=(0, 4))

        self.backbone = BackbonePanel(center, t, **ps)
        self._place(self.backbone, row=1, column=0, sticky="nsew", pady=(4, 0))

        self.ops = OpsPanel(root, t, **ps)
        self._place(self.ops, row=1, column=2, sticky="nsew", padx=(6, 12), pady=(8, 6))
        self._footer(root, 3)

    # ── Hacker terminal wall + incident sidebar (no map / ops / video) ──

    def _build_threatwatch(self) -> None:
        t = self.theme
        root = self.window
        ps = _panel_style(t)
        root.grid_columnconfigure(0, weight=7)
        root.grid_columnconfigure(1, weight=3)
        root.grid_rowconfigure(1, weight=1)
        self._header(root, 2)

        self.terminal = TerminalFeed(root, t, **ps)
        self._place(self.terminal, row=1, column=0, sticky="nsew", padx=(12, 6), pady=(8, 6))

        right = ctk.CTkFrame(root, fg_color="transparent")
        right.grid(row=1, column=1, sticky="nsew", padx=(6, 12), pady=(8, 6))
        right.grid_rowconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        incident = IncidentQueuePanel(right, t, **ps)
        self._place(incident, row=0, column=0, sticky="nsew", pady=(0, 4))
        targets = TargetListPanel(right, t, **ps)
        self._place(targets, row=1, column=0, sticky="nsew", pady=(4, 0))

        self.world_map = self.backbone = self.ops = self.video_feed = None
        self._footer(root, 2)

    # ── Large map + pass schedule sidebar + bottom telemetry ──

    def _build_orbital(self) -> None:
        t = self.theme
        root = self.window
        ps = _panel_style(t)
        root.grid_columnconfigure(0, weight=6)
        root.grid_columnconfigure(1, weight=2)
        root.grid_columnconfigure(2, weight=2)
        root.grid_rowconfigure(1, weight=3)
        root.grid_rowconfigure(2, weight=1)
        self._header(root, 3)

        map_wrap = ctk.CTkFrame(root, **ps)
        map_wrap.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=(8, 4))
        map_wrap.grid_rowconfigure(1, weight=1)
        map_wrap.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            map_wrap, text=f"◈  {t.map_title}",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=t.label_muted, anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(6, 2))
        self.world_map = OrbitalTrackPanel(map_wrap, t)
        self._place(self.world_map, row=1, column=0, sticky="nsew", padx=4, pady=(0, 4))

        mid = ctk.CTkFrame(root, fg_color="transparent")
        mid.grid(row=1, column=1, sticky="nsew", padx=6, pady=(8, 4))
        mid.grid_rowconfigure(0, weight=1)
        mid.grid_rowconfigure(1, weight=1)
        passes = PassSchedulePanel(mid, t, **ps)
        self._place(passes, row=0, column=0, sticky="nsew", pady=(0, 4))
        telemetry = TelemetryStripPanel(mid, t, **ps)
        self._place(telemetry, row=1, column=0, sticky="nsew", pady=(4, 0))

        right = ctk.CTkFrame(root, fg_color="transparent")
        right.grid(row=1, column=2, sticky="nsew", padx=(6, 12), pady=(8, 4))
        right.grid_rowconfigure(0, weight=2)
        right.grid_rowconfigure(1, weight=2)
        right.grid_rowconfigure(2, weight=0)
        tracked = TrackedObjectsPanel(right, t, **ps)
        self._place(tracked, row=0, column=0, sticky="nsew", pady=(0, 4))
        stations = GroundStationPanel(right, t, **ps)
        self._place(stations, row=1, column=0, sticky="nsew", pady=(4, 4))
        tle = OrbitalTlePanel(right, t, **ps)
        self._place(tle, row=2, column=0, sticky="ew", pady=(4, 0))

        self.terminal = TerminalFeed(root, t, **ps)
        self._place(self.terminal, row=2, column=0, columnspan=3, sticky="nsew", padx=12, pady=(4, 6))

        self.backbone = self.ops = self.video_feed = None
        self._footer(root, 3)

    # ── Ticker | map | flagged — video bar bottom ──

    def _build_ledger(self) -> None:
        t = self.theme
        root = self.window
        ps = _panel_style(t)
        root.grid_columnconfigure(0, weight=2)
        root.grid_columnconfigure(1, weight=5)
        root.grid_columnconfigure(2, weight=3)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=0, minsize=160)
        self._header(root, 3)

        left = ctk.CTkFrame(root, fg_color="transparent")
        left.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=(8, 4))
        left.grid_rowconfigure(0, weight=3)
        left.grid_rowconfigure(1, weight=2)
        ticker = TransactionTickerPanel(left, t, **ps)
        self._place(ticker, row=0, column=0, sticky="nsew", pady=(0, 4))
        fx = ExchangeRatePanel(left, t, **ps)
        self._place(fx, row=1, column=0, sticky="nsew", pady=(4, 0))

        center = ctk.CTkFrame(root, **ps)
        center.grid(row=1, column=1, sticky="nsew", padx=6, pady=(8, 4))
        center.grid_rowconfigure(1, weight=1)
        center.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            center, text=f"◈  {t.map_title}",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=t.label_muted, anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(6, 2))
        self.ip_trace_map = IpTraceMapPanel(center, t)
        self._place(self.ip_trace_map, row=1, column=0, sticky="nsew", padx=4, pady=(0, 4))

        right = ctk.CTkFrame(root, fg_color="transparent")
        right.grid(row=1, column=2, sticky="nsew", padx=(6, 12), pady=(8, 4))
        right.grid_rowconfigure(1, weight=2)
        right.grid_rowconfigure(2, weight=2)
        right.grid_rowconfigure(3, weight=2)
        fed = FedReserveBannerPanel(right, t, **ps)
        self._place(fed, row=0, column=0, sticky="ew", pady=(0, 4))
        flagged = FlaggedAccountsPanel(right, t, **ps)
        self._place(flagged, row=1, column=0, sticky="nsew", pady=(4, 4))
        banks = BankCorrespondentsPanel(right, t, **ps)
        self._place(banks, row=2, column=0, sticky="nsew", pady=(4, 4))
        market = MarketGraphPanel(right, t, **ps)
        self._place(market, row=3, column=0, sticky="nsew", pady=(4, 0))

        bottom = ctk.CTkFrame(root, fg_color="transparent")
        bottom.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=12, pady=(4, 6))
        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=2)
        bottom.grid_rowconfigure(0, weight=1)
        settlements = FedWireTickerPanel(bottom, t, **ps)
        self._place(settlements, row=0, column=0, sticky="nsew", padx=(0, 6))
        self.video_feed = VideoFeedPanel(bottom, t, **ps)
        self._place(self.video_feed, row=0, column=1, sticky="nsew", padx=(6, 0))

        self.terminal = self.backbone = self.ops = None
        self._footer(root, 3)

    # ── Gauges top, scada log + small map bottom ──

    def _build_gridops(self) -> None:
        t = self.theme
        root = self.window
        ps = _panel_style(t)
        root.grid_columnconfigure(0, weight=3)
        root.grid_columnconfigure(1, weight=5)
        root.grid_columnconfigure(2, weight=3)
        root.grid_rowconfigure(2, weight=1)
        self._header(root, 3)

        top = ctk.CTkFrame(root, fg_color="transparent")
        top.grid(row=1, column=0, columnspan=3, sticky="ew", padx=12, pady=(8, 4))
        top.grid_columnconfigure(0, weight=3)
        top.grid_columnconfigure(1, weight=2)
        gauge_wrap = ctk.CTkFrame(top, **ps)
        gauge_wrap.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        gauge_wrap.grid_columnconfigure(0, weight=1)
        gauges = GaugeBoardPanel(gauge_wrap, t, fg_color="transparent", border_width=0)
        self._place(gauges, row=0, column=0, sticky="ew")
        utility = PowerUtilityLogoPanel(top, t, **ps)
        self._place(utility, row=0, column=1, sticky="nsew")

        self.terminal = TerminalFeed(root, t, **ps)
        self._place(self.terminal, row=2, column=0, sticky="nsew", padx=(12, 6), pady=(4, 6))

        map_wrap = ctk.CTkFrame(root, **ps)
        map_wrap.grid(row=2, column=1, sticky="nsew", padx=6, pady=(4, 6))
        map_wrap.grid_rowconfigure(1, weight=1)
        map_wrap.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            map_wrap, text=f"◈  {t.map_title}",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=t.label_muted, anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=8, pady=(4, 0))
        self.world_map = TransmissionGridPanel(map_wrap, t)
        self._place(self.world_map, row=1, column=0, sticky="nsew", padx=2, pady=(0, 2))

        right = ctk.CTkFrame(root, fg_color="transparent")
        right.grid(row=2, column=2, sticky="nsew", padx=(6, 12), pady=(4, 6))
        right.grid_rowconfigure(0, weight=2)
        right.grid_rowconfigure(1, weight=2)
        right.grid_rowconfigure(2, weight=2)
        right.grid_rowconfigure(3, weight=1)
        blackout = BlackoutMonitorPanel(right, t, **ps)
        self._place(blackout, row=0, column=0, sticky="nsew", pady=(0, 4))
        relays = RelayElectronicsPanel(right, t, **ps)
        self._place(relays, row=1, column=0, sticky="nsew", pady=(4, 4))
        self.backbone = BackbonePanel(right, t, **ps)
        self._place(self.backbone, row=2, column=0, rowspan=2, sticky="nsew", pady=(4, 0))

        self.ops = self.video_feed = None
        self._footer(root, 3)

    def _start_effects(self) -> None:
        if not self._running:
            return
        for w in self._widgets:
            if hasattr(w, "start"):
                w.start()

    def _animate_stats(self) -> None:
        if not self._running:
            return
        t = self.theme
        val = random.randint(800, 4200)
        peers = random.randint(12, 48)
        routes = random.randint(900000, 980000)
        self.stats_label.configure(
            text=(
                f"{t.stats_prefix} {val}  │  PEERS {peers}  │  ROUTES {routes:,}  "
                f"│  UPTIME 99.{random.randint(90, 99)}%  │  {t.classification}"
            )
        )
        self.window.after(900, self._animate_stats)

    def close(self, _event=None) -> None:
        if not self._running:
            return
        self._running = False
        for w in self._widgets:
            if hasattr(w, "stop"):
                w.stop()
        try:
            self.window.destroy()
        except Exception:
            pass
        ConsoleWindow._open_count = max(0, ConsoleWindow._open_count - 1)
        if self._on_close:
            self._on_close()

    def lift(self) -> None:
        self.window.lift()
        self.window.focus_force()

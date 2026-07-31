"""Startup screen — pick a console; each opens in its own window."""

from __future__ import annotations

from collections.abc import Callable

import customtkinter as ctk
from PIL import Image

from hacker_screen.data.console_themes import ConsoleTheme, all_themes
from hacker_screen.paths import assets_dir

LAUNCHER_BG = assets_dir() / "images" / "launcher_bg.png"
LAUNCHER_W, LAUNCHER_H = 980, 780


class LauncherWindow:
    def __init__(
        self,
        root: ctk.CTk,
        on_open: Callable[[ConsoleTheme], None],
        on_quit: Callable[[], None],
    ) -> None:
        self.root = root
        self.on_open = on_open
        self.on_quit = on_quit
        self._buttons: list[ctk.CTkButton] = []
        self._build()

    def _build(self) -> None:
        root = self.root
        root.title("Hacker Screen — Console Selector")
        root.configure(fg_color="#04080c")
        root.minsize(720, 560)
        root.resizable(True, True)

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = max(0, (sw - LAUNCHER_W) // 2)
        y = max(0, (sh - LAUNCHER_H) // 2)
        root.geometry(f"{LAUNCHER_W}x{LAUNCHER_H}+{x}+{y}")

        ctk.set_appearance_mode("dark")

        if LAUNCHER_BG.exists():
            bg_img = Image.open(LAUNCHER_BG)
            self._bg = ctk.CTkImage(light_image=bg_img, dark_image=bg_img, size=(980, 780))
            ctk.CTkLabel(root, text="", image=self._bg).place(relx=0.5, rely=0.5, anchor="center")

        overlay = ctk.CTkFrame(root, fg_color="transparent")
        overlay.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.92)

        panel = ctk.CTkFrame(
            overlay,
            fg_color="#0a1018",
            corner_radius=12,
            border_width=1,
            border_color="#2a4050",
        )
        panel.pack(fill="both", expand=True)
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel,
            text="HACKER SCREEN",
            font=ctk.CTkFont(family="Consolas", size=32, weight="bold"),
            text_color="#b8d0e8",
        ).grid(row=0, column=0, pady=(24, 4))

        ctk.CTkLabel(
            panel,
            text="MULTI-MONITOR OPERATIONS SIMULATOR",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#668899",
        ).grid(row=1, column=0, pady=(0, 4))

        ctk.CTkLabel(
            panel,
            text="Open one or more consoles — drag each window to a different display",
            font=ctk.CTkFont(size=12),
            text_color="#778899",
        ).grid(row=2, column=0, pady=(0, 16))

        btn_frame = ctk.CTkFrame(panel, fg_color="transparent")
        btn_frame.grid(row=3, column=0, sticky="nsew", padx=32, pady=8)
        btn_frame.grid_columnconfigure(0, weight=1)

        themes = all_themes()
        accent_map = {t.id: t.accent2 for t in themes}

        for i, theme in enumerate(themes):
            row = ctk.CTkFrame(btn_frame, fg_color="transparent")
            row.grid(row=i, column=0, sticky="ew", pady=5)
            row.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                row,
                text="◆",
                font=ctk.CTkFont(size=16),
                text_color=accent_map.get(theme.id, "#88bbaa"),
                width=24,
            ).grid(row=0, column=0, padx=(0, 8))

            btn = ctk.CTkButton(
                row,
                text=f"{theme.button_label}   —   {theme.button_desc}",
                font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
                fg_color="#1a2530",
                hover_color="#2a4050",
                text_color="#c8d8e8",
                border_width=1,
                border_color="#3a5060",
                height=48,
                anchor="w",
                command=lambda th=theme: self._open_console(th),
            )
            btn.grid(row=0, column=1, sticky="ew")
            self._buttons.append(btn)

        footer = ctk.CTkFrame(panel, fg_color="transparent")
        footer.grid(row=4, column=0, pady=(12, 20))

        ctk.CTkButton(
            footer,
            text="Exit",
            width=100,
            height=32,
            fg_color="#1a2028",
            hover_color="#3a2020",
            text_color="#99aabb",
            command=self.on_quit,
        ).pack()

        ctk.CTkLabel(
            panel,
            text="Simulation only — no real network activity",
            font=ctk.CTkFont(size=10),
            text_color="#445566",
        ).grid(row=5, column=0, pady=(0, 12))

        root.bind("<Escape>", lambda _e: self.on_quit())
        root.protocol("WM_DELETE_WINDOW", self.on_quit)

    def _open_console(self, theme: ConsoleTheme) -> None:
        self.on_open(theme)

    def set_status(self, text: str) -> None:
        pass

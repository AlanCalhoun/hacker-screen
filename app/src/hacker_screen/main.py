"""Application entry point."""

from __future__ import annotations

import customtkinter as ctk

from hacker_screen.app import ConsoleWindow
from hacker_screen.data.console_themes import ConsoleTheme
from hacker_screen.generate_assets import ensure_assets
from hacker_screen.generate_videos import ensure_videos
from hacker_screen.launcher import LauncherWindow
from hacker_screen.paths import apply_window_icon, is_frozen


class SessionManager:
    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        self._consoles: dict[str, ConsoleWindow] = {}

    def open_console(self, theme: ConsoleTheme) -> None:
        existing = self._consoles.get(theme.id)
        if existing is not None:
            try:
                if existing.window.winfo_exists():
                    existing.lift()
                    return
            except Exception:
                pass
            self._consoles.pop(theme.id, None)

        console = ConsoleWindow(
            self.root,
            theme,
            on_close=lambda tid=theme.id: self._consoles.pop(tid, None),
        )
        self._consoles[theme.id] = console


def main() -> None:
    ensure_assets()
    ensure_videos(force=False)

    root = ctk.CTk()
    apply_window_icon(root)

    manager = SessionManager(root)

    def on_quit() -> None:
        for console in list(manager._consoles.values()):
            console.close()
        root.quit()
        root.destroy()

    LauncherWindow(root, manager.open_console, on_quit)
    root.mainloop()

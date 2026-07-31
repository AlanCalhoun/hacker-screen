"""Scrolling terminal feed with fake hacking messages."""

from __future__ import annotations

import customtkinter as ctk

from hacker_screen.data.console_themes import ConsoleTheme
from hacker_screen.data.theme_messages import boot_sequence, generate_line


class TerminalFeed(ctk.CTkFrame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._running = False

        ctk.CTkLabel(
            self,
            text=f"◈  {theme.session_log_title}",
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
            text_color=theme.terminal_header,
            anchor="w",
        ).pack(fill="x", padx=10, pady=(10, 6))

        self.text = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=theme.terminal_bg,
            text_color=theme.terminal_fg,
            wrap="none",
            activate_scrollbars=False,
            border_width=1,
            border_color=theme.terminal_border,
        )
        self.text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._setup_tags()

    def _setup_tags(self) -> None:
        for tag, color in self._theme.tag_colors.items():
            self.text._textbox.tag_configure(tag, foreground=color)

    def start(self) -> None:
        self._running = True
        self._append_boot_sequence()
        self._schedule_line()

    def stop(self) -> None:
        self._running = False

    def _append_boot_sequence(self) -> None:
        for line, tag in boot_sequence(self._theme.id):
            self._insert_line(line, tag)

    def _insert_line(self, line: str, tag: str) -> None:
        self.text.configure(state="normal")
        self.text._textbox.insert("end", line + "\n", tag)
        self.text._textbox.see("end")
        total = int(self.text._textbox.index("end-1c").split(".")[0])
        if total > 200:
            self.text._textbox.delete("1.0", f"{total - 180}.0")
        self.text.configure(state="disabled")

    def _schedule_line(self) -> None:
        if not self._running:
            return
        line, tag = generate_line(self._theme.id)
        self._insert_line(line, tag)
        delay = 120 if tag == "alert" else 220
        self.after(delay, self._schedule_line)

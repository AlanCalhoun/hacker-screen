"""Rotating high-tech tactical video feed panel."""

from __future__ import annotations

from pathlib import Path

import customtkinter as ctk
import cv2
from PIL import Image, ImageEnhance

from hacker_screen.data.console_themes import ConsoleTheme
from hacker_screen.effects.perf import MAX_VIDEO_H, MAX_VIDEO_W
from hacker_screen.data.video_theme_config import get_video_config
from hacker_screen.paths import theme_videos_dir

LOOPS_BEFORE_SWITCH = 2
VIDEO_ASPECT = 16 / 9  # matches generated feed resolution (960x540)


class VideoFeedPanel(ctk.CTkFrame):
    def __init__(self, master, theme: ConsoleTheme, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self._theme = theme
        self._feed_titles = get_video_config(theme.id).feed_titles
        self._videos_dir = theme_videos_dir(theme.id)
        self._running = False
        self._video_paths = sorted(self._videos_dir.glob("feed_*.mp4"))
        if not self._video_paths:
            # fallback legacy flat layout (netdefense only)
            from hacker_screen.paths import videos_dir
            self._video_paths = sorted(videos_dir().glob("feed_*.mp4"))
        self._video_index = 0
        self._loop_count = 0
        self._cap: cv2.VideoCapture | None = None
        self._last_video_size: tuple[int, int] = (0, 0)

        ctk.CTkLabel(
            self,
            text=f"◈  {theme.video_title}",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=theme.label_muted,
            anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))

        self._video_container = ctk.CTkFrame(self, fg_color="transparent")
        self._video_container.pack(fill="both", expand=True, padx=10, pady=4)

        self.video_label = ctk.CTkLabel(
            self._video_container, text="", fg_color=theme.inner_bg, corner_radius=4,
            border_width=1, border_color=theme.panel_border,
        )
        self.video_label.place(relx=0.5, rely=0.5, anchor="center")

        self.status = ctk.CTkLabel(
            self,
            text="STANDBY",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#556677",
        )
        self.status.pack(pady=(0, 8))

        self._video_container.bind("<Configure>", lambda _e: self._resize_video())

    def _fit_video_size(self, container_w: int, container_h: int) -> tuple[int, int]:
        """Landscape 16:9 box that fills as much of the panel as possible."""
        cw = max(container_w, 1)
        ch = max(container_h, 1)
        w = cw
        h = int(w / VIDEO_ASPECT)
        if h > ch:
            h = ch
            w = int(h * VIDEO_ASPECT)
        return max(w, 240), max(h, 135)

    def _resize_video(self) -> None:
        w, h = self._fit_video_size(
            self._video_container.winfo_width(),
            self._video_container.winfo_height(),
        )
        self.video_label.configure(width=w, height=h)

    def start(self) -> None:
        self._running = True
        self._loop_count = 0
        self._video_paths = sorted(self._videos_dir.glob("feed_*.mp4"))
        if not self._video_paths:
            from hacker_screen.paths import videos_dir
            self._video_paths = sorted(videos_dir().glob("feed_*.mp4"))
        self._open_video()
        self.after(200, self._play_frame)

    def stop(self) -> None:
        self._running = False
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def _current_title(self) -> str:
        if not self._video_paths:
            return "NO FEED"
        stem = self._video_paths[self._video_index % len(self._video_paths)].stem
        return self._feed_titles.get(stem, stem.replace("_", " ").upper())

    def _open_video(self) -> None:
        if self._cap is not None:
            self._cap.release()
            self._cap = None
        if not self._video_paths:
            self.status.configure(text="NO VIDEO ASSETS — run main.py to build feeds")
            return
        path = self._video_paths[self._video_index % len(self._video_paths)]
        self._cap = cv2.VideoCapture(str(path))
        if not self._cap.isOpened():
            self._video_index += 1
            self._cap = None

    def _advance_video(self) -> None:
        self._loop_count = 0
        self._video_index += 1
        self._open_video()

    def _play_frame(self) -> None:
        if not self._running:
            return
        if not self._video_paths:
            self.after(500, self._play_frame)
            return
        if self._cap is None or not self._cap.isOpened():
            self._open_video()
            self.after(100, self._play_frame)
            return

        ret, frame = self._cap.read()
        if not ret:
            self._loop_count += 1
            if self._loop_count >= LOOPS_BEFORE_SWITCH:
                self._advance_video()
            else:
                self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.after(30, self._play_frame)
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img = ImageEnhance.Contrast(img).enhance(1.04)
        self._video_container.update_idletasks()
        vw, vh = self._fit_video_size(
            self._video_container.winfo_width(),
            self._video_container.winfo_height(),
        )
        vw = min(vw, MAX_VIDEO_W)
        vh = min(vh, MAX_VIDEO_H)
        img = img.resize((vw, vh), Image.Resampling.BILINEAR)
        vid_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        self.video_label.configure(image=vid_img, text="")
        self.video_label._ref = vid_img
        self._last_video_size = (vw, vh)

        n = len(self._video_paths)
        idx = self._video_index % n
        self.status.configure(
            text=f"● {self._current_title()}  ·  feed {idx + 1}/{n}  ·  loop {self._loop_count + 1}/{LOOPS_BEFORE_SWITCH}"
        )
        self.after(40, self._play_frame)

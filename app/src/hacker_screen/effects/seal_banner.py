"""Rotating agency seal banner with fixed Kali Linux logo."""

from __future__ import annotations

from pathlib import Path

import customtkinter as ctk
from PIL import Image

from hacker_screen.paths import assets_dir

SEALS_DIR = assets_dir() / "images" / "seals"
KALI_LOGO = assets_dir() / "images" / "kali_logo.png"

SEAL_SIZE = 132
KALI_SIZE = 118

# Display names for seal filenames
SEAL_LABELS: dict[str, str] = {
    "seal_cyber_command": "U.S. CYBER COMMAND",
    "seal_network_ops": "NAT'L TELEMETRY ADMIN",
    "seal_dhcs": "HOMELAND CYBER SECURITY",
    "seal_disa": "DEFENSE INFO SYSTEMS",
    "seal_nsib": "SIGNALS INTEL BUREAU",
}

ROTATE_MS = 4200


class SealBanner(ctk.CTkFrame):
    """Kali logo (fixed) + one rotating agency seal at a time."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._running = False
        self._seal_paths: list[Path] = []
        self._seal_index = 0
        self._images: dict[str, ctk.CTkImage] = {}

        self._load_assets()
        self._build_ui()

    def _load_assets(self) -> None:
        self._seal_paths = sorted(SEALS_DIR.glob("seal_*.png"))
        for path in self._seal_paths:
            img = Image.open(path).convert("RGB")
            img.thumbnail((SEAL_SIZE, SEAL_SIZE), Image.Resampling.LANCZOS)
            self._images[path.name] = ctk.CTkImage(
                light_image=img, dark_image=img, size=img.size,
            )

    def _build_ui(self) -> None:
        # Kali logo — always visible
        kali_frame = ctk.CTkFrame(self, fg_color="#0a1018", corner_radius=8,
                                  border_width=1, border_color="#1a3040")
        kali_frame.pack(side="left", padx=(0, 10))

        if KALI_LOGO.exists():
            kimg = Image.open(KALI_LOGO).convert("RGBA")
            kimg.thumbnail((KALI_SIZE, KALI_SIZE), Image.Resampling.LANCZOS)
            self._kali_ctk = ctk.CTkImage(light_image=kimg, dark_image=kimg, size=kimg.size)
            ctk.CTkLabel(kali_frame, text="", image=self._kali_ctk).pack(padx=8, pady=8)
        else:
            ctk.CTkLabel(
                kali_frame, text="KALI", width=KALI_SIZE, height=KALI_SIZE,
                font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
                text_color="#367bf0", fg_color="#0a1018",
            ).pack(padx=8, pady=8)

        ctk.CTkLabel(
            kali_frame, text="KALI LINUX",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            text_color="#5588cc",
        ).pack(pady=(0, 6))

        # Rotating seal slot
        self.seal_frame = ctk.CTkFrame(self, fg_color="#0a1018", corner_radius=8,
                                       border_width=1, border_color="#1a3040")
        self.seal_frame.pack(side="left", padx=(0, 10))

        self.seal_label = ctk.CTkLabel(self.seal_frame, text="", width=SEAL_SIZE, height=SEAL_SIZE)
        self.seal_label.pack(padx=8, pady=(8, 2))

        self.seal_name = ctk.CTkLabel(
            self.seal_frame, text="",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            text_color="#8899aa",
        )
        self.seal_name.pack(pady=(0, 6))

        # Task force info
        info = ctk.CTkFrame(self, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            info, text="JOINT TASK FORCE — NODE DELTA-7",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color="#8899aa", anchor="w",
        ).pack(anchor="w", pady=(12, 2))

        ctk.CTkLabel(
            info, text="Authorized: NET-DEFENSE / SAT-COM",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#667788", anchor="w",
        ).pack(anchor="w")

        self.rotate_hint = ctk.CTkLabel(
            info, text="",
            font=ctk.CTkFont(family="Consolas", size=9),
            text_color="#445566", anchor="w",
        )
        self.rotate_hint.pack(anchor="w", pady=(6, 0))

        self._show_current_seal()

    def _label_for(self, path: Path) -> str:
        key = path.stem
        return SEAL_LABELS.get(key, key.replace("seal_", "").replace("_", " ").upper())

    def _show_current_seal(self) -> None:
        if not self._seal_paths:
            self.seal_label.configure(text="NO SEAL", image=None)
            self.seal_name.configure(text="")
            return

        path = self._seal_paths[self._seal_index % len(self._seal_paths)]
        img = self._images.get(path.name)
        if img:
            self.seal_label.configure(image=img, text="")
        self.seal_name.configure(text=self._label_for(path))
        n = len(self._seal_paths)
        idx = self._seal_index % n
        self.rotate_hint.configure(text=f"Agency credential {idx + 1} of {n}  ·  rotating")

    def start(self) -> None:
        self._running = True
        self._rotate()

    def stop(self) -> None:
        self._running = False

    def _rotate(self) -> None:
        if not self._running or not self._seal_paths:
            return
        self._seal_index += 1
        self._show_current_seal()
        self.after(ROTATE_MS, self._rotate)

"""Build procedural video feeds — original netdefense + distinct themed consoles."""

from __future__ import annotations

from pathlib import Path

from hacker_screen.generate_videos_creative import THEME_BUILDER_MAP
from hacker_screen.generate_videos_legacy import NETDEFENSE_BUILDERS
from hacker_screen.paths import videos_dir

FEED_NAMES = [
    "feed_auth.mp4",
    "feed_network.mp4",
    "feed_packets.mp4",
    "feed_spectrum.mp4",
    "feed_tracking.mp4",
]

THEME_BUILDERS: dict[str, list] = {
    "netdefense": NETDEFENSE_BUILDERS,
    **THEME_BUILDER_MAP,
}


def theme_videos_dir(theme_id: str) -> Path:
    return videos_dir() / theme_id


def ensure_videos(force: bool = False, themes: list[str] | None = None) -> None:
    theme_list = themes or list(THEME_BUILDERS.keys())
    built = 0
    for theme_id in theme_list:
        builders = THEME_BUILDERS.get(theme_id)
        if not builders:
            continue
        out_dir = theme_videos_dir(theme_id)
        out_dir.mkdir(parents=True, exist_ok=True)
        if force:
            for old in out_dir.glob("*.mp4"):
                old.unlink()
        for name, builder in zip(FEED_NAMES, builders):
            dst = out_dir / name
            if force or not dst.exists():
                builder(dst)
                print(f"  built {theme_id}/{name}")
                built += 1
    if built == 0:
        print("  all theme videos up to date")
    else:
        print(f"  {built} video(s) built under {videos_dir()}")


if __name__ == "__main__":
    ensure_videos(force=False)

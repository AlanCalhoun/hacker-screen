#!/usr/bin/env python3
"""Hacker Screen — press one button, look like you're hacking the planet."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from hacker_screen.main import main

if __name__ == "__main__":
    main()

"""Distinctive video feeds for non-netdefense consoles — terminals, minimal UIs, etc."""

from __future__ import annotations

import math
import random
import string
from pathlib import Path

import cv2
import numpy as np

W, H = 960, 540
FPS = 30
DURATION_S = 10
FONT = cv2.FONT_HERSHEY_SIMPLEX


def _writer(path: Path) -> cv2.VideoWriter:
    wr = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), FPS, (W, H))
    if not wr.isOpened():
        wr = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"avc1"), FPS, (W, H))
    return wr


def _term_frame(bg: tuple[int, int, int], fg: tuple[int, int, int], dim: tuple[int, int, int]) -> np.ndarray:
    f = np.zeros((H, W, 3), dtype=np.uint8)
    f[:] = bg
    cv2.rectangle(f, (0, 0), (W, 28), (max(0, bg[0] - 10), max(0, bg[1] - 10), max(0, bg[2] - 10)), -1)
    cv2.putText(f, "root@ops-console", (12, 20), FONT, 0.5, dim, 1, cv2.LINE_AA)
    return f


def _scroll_terminal(
    out: Path,
    bg: tuple[int, int, int],
    fg: tuple[int, int, int],
    dim: tuple[int, int, int],
    prompt: str,
    line_fn,
    seed: int,
    title: str,
) -> None:
    rng = random.Random(seed)
    lines: list[str] = []
    writer = _writer(out)
    for i in range(FPS * DURATION_S):
        frame = _term_frame(bg, fg, dim)
        if i % 2 == 0:
            lines.append(line_fn(rng, i))
            if len(lines) > 22:
                lines.pop(0)
        scroll = i % 4
        for j, line in enumerate(lines):
            y = 48 + j * 22 - scroll
            if y < 36 or y > H - 10:
                continue
            col = fg if j >= len(lines) - 2 else dim
            if line.startswith("[+]") or line.startswith("OK"):
                col = (100, 255, 150) if bg[1] < 30 else (150, 255, 200)
            if line.startswith("[!]") or "FAIL" in line or "ERROR" in line:
                col = (80, 80, 255) if bg[2] < 30 else (100, 100, 255)
            cv2.putText(frame, line[:90], (16, y), FONT, 0.45, col, 1, cv2.LINE_AA)
        blink = "_" if (i // 15) % 2 == 0 else " "
        cv2.putText(frame, f"{prompt}{blink}", (16, H - 16), FONT, 0.5, fg, 1, cv2.LINE_AA)
        cv2.putText(frame, title, (W - 280, 20), FONT, 0.45, dim, 1, cv2.LINE_AA)
        writer.write(frame)
    writer.release()


def _matrix_rain(out: Path, bg: tuple, head: tuple, trail: tuple, seed: int) -> None:
    rng = random.Random(seed)
    cols = W // 14
    drops = [rng.randint(-H, 0) for _ in range(cols)]
    chars = string.ascii_letters + string.digits + "$<>[]{}|/\\"
    grid = [[rng.choice(chars) for _ in range(H // 18 + 2)] for _ in range(cols)]
    writer = _writer(out)
    for i in range(FPS * DURATION_S):
        frame = np.zeros((H, W, 3), dtype=np.uint8)
        frame[:] = bg
        for c in range(cols):
            drops[c] += rng.randint(8, 22)
            if drops[c] > H + 100:
                drops[c] = rng.randint(-120, -20)
            x = 8 + c * 14
            for row in range(H // 18 + 2):
                y = int(drops[c] + row * 18)
                if y < 0 or y > H:
                    continue
                ch = grid[c][row % len(grid[c])]
                if row == 0:
                    cv2.putText(frame, ch, (x, y), FONT, 0.45, head, 1, cv2.LINE_AA)
                else:
                    cv2.putText(frame, ch, (x, y), FONT, 0.45, trail, 1, cv2.LINE_AA)
            if i % 5 == c % 5:
                grid[c][rng.randint(0, len(grid[c]) - 1)] = rng.choice(chars)
        cv2.putText(frame, "LIVE C2 SNIFFER — ENCRYPTED TRAFFIC DECODED", (20, H - 20), FONT, 0.5, head, 1, cv2.LINE_AA)
        writer.write(frame)
    writer.release()


def _big_readout(out: Path, bg: tuple, fg: tuple, label: str, value_fn, seed: int, unit: str = "") -> None:
    rng = random.Random(seed)
    writer = _writer(out)
    for i in range(FPS * DURATION_S):
        frame = np.zeros((H, W, 3), dtype=np.uint8)
        frame[:] = bg
        val = value_fn(i, rng)
        cv2.putText(frame, label, (W // 2 - 200, H // 2 - 80), FONT, 0.9, (fg[0] // 2, fg[1] // 2, fg[2] // 2), 2, cv2.LINE_AA)
        cv2.putText(frame, str(val), (W // 2 - len(str(val)) * 28, H // 2 + 20), FONT, 2.2, fg, 4, cv2.LINE_AA)
        if unit:
            cv2.putText(frame, unit, (W // 2 + 180, H // 2 + 10), FONT, 0.8, fg, 2, cv2.LINE_AA)
        bar = int((W - 120) * (0.3 + 0.5 * abs(math.sin(i / 20))))
        cv2.rectangle(frame, (60, H - 80), (W - 60, H - 60), (20, 20, 40), -1)
        cv2.rectangle(frame, (60, H - 80), (60 + bar, H - 60), fg, -1)
        writer.write(frame)
    writer.release()


def _ticker_columns(out: Path, bg: tuple, fg: tuple, warn: tuple, headers: list[str], seed: int) -> None:
    rng = random.Random(seed)
    rows: list[list[str]] = []
    writer = _writer(out)
    col_w = (W - 40) // len(headers)
    for i in range(FPS * DURATION_S):
        frame = np.zeros((H, W, 3), dtype=np.uint8)
        frame[:] = bg
        for j, h in enumerate(headers):
            cv2.putText(frame, h, (24 + j * col_w, 40), FONT, 0.55, warn, 1, cv2.LINE_AA)
        if i % 3 == 0:
            rows.insert(0, [f"{rng.randint(1000,9999)}", f"${rng.randint(10,999)}.{rng.randint(10,99):02d}",
                            f"+{rng.randint(-5,12)}.{rng.randint(0,9)}%", rng.choice(["OK", "FLAG", "HOLD"])])
            if len(rows) > 20:
                rows.pop()
        for ri, row in enumerate(rows):
            y = 70 + ri * 24
            for ci, cell in enumerate(row):
                col = warn if cell == "FLAG" else fg if cell == "OK" else (80, 160, 255)
                cv2.putText(frame, cell, (24 + ci * col_w, y), FONT, 0.45, col, 1, cv2.LINE_AA)
        writer.write(frame)
    writer.release()


def _radar_sweep(out: Path, bg: tuple, line: tuple, blip: tuple, seed: int) -> None:
    rng = random.Random(seed)
    blips = [(rng.uniform(0.2, 0.8), rng.uniform(0.2, 0.8), rng.uniform(0, 6.28)) for _ in range(6)]
    writer = _writer(out)
    cx, cy, r = W // 2, H // 2 + 20, min(W, H) // 2 - 60
    for i in range(FPS * DURATION_S):
        frame = np.zeros((H, W, 3), dtype=np.uint8)
        frame[:] = bg
        cv2.circle(frame, (cx, cy), r, line, 1)
        cv2.circle(frame, (cx, cy), r * 2 // 3, line, 1)
        cv2.circle(frame, (cx, cy), r // 3, line, 1)
        ang = (i * 0.08) % (2 * math.pi)
        cv2.line(frame, (cx, cy), (int(cx + math.cos(ang) * r), int(cy + math.sin(ang) * r)), line, 2)
        for bx, by, _ in blips:
            px, py = int(cx + (bx - 0.5) * r * 1.8), int(cy + (by - 0.5) * r * 1.8)
            cv2.circle(frame, (px, py), 6, blip, -1)
        cv2.putText(frame, "ORBITAL RADAR — CONTACT TRACK", (cx - 180, 40), FONT, 0.6, line, 1, cv2.LINE_AA)
        cv2.putText(frame, f"SWEEP {i * 360 // FPS % 360:03d}", (cx - 60, H - 30), FONT, 0.55, line, 1, cv2.LINE_AA)
        writer.write(frame)
    writer.release()


def _alarm_board(out: Path, bg: tuple, ok: tuple, warn: tuple, crit: tuple, seed: int) -> None:
    rng = random.Random(seed)
    alarms: list[tuple[str, str]] = []
    writer = _writer(out)
    for i in range(FPS * DURATION_S):
        frame = np.zeros((H, W, 3), dtype=np.uint8)
        frame[:] = bg
        if i % 25 == 0:
            lvl = rng.choice(["CRIT", "WARN", "OK", "OK"])
            alarms.insert(0, (lvl, f"SUB-{rng.randint(1,99):02d}  FEEDER-{rng.randint(1,12)}  {rng.choice(['TRIP', 'OVERTEMP', 'RESTORE', 'NOMINAL'])}"))
            if len(alarms) > 18:
                alarms.pop()
        for j, (lvl, msg) in enumerate(alarms):
            col = crit if lvl == "CRIT" else warn if lvl == "WARN" else ok
            if lvl == "CRIT" and i % 10 < 5:
                col = bg
            cv2.rectangle(frame, (20, 50 + j * 26), (W - 20, 72 + j * 26), (col[0] // 4, col[1] // 4, col[2] // 4), -1)
            cv2.putText(frame, f"[{lvl}] {msg}", (32, 68 + j * 26), FONT, 0.48, col, 1, cv2.LINE_AA)
        cv2.putText(frame, "SCADA ALARM PANEL", (20, 30), FONT, 0.6, ok, 1, cv2.LINE_AA)
        writer.write(frame)
    writer.release()


# ── THREATWATCH: red/black hacker terminals ──

def _tw_line(rng: random.Random, i: int) -> str:
    cmds = [
        lambda: f"nmap -sV -p{rng.randint(1,65535)} {rng.randint(1,223)}.{rng.randint(0,255)}.{rng.randint(0,255)}.{rng.randint(1,254)}",
        lambda: f"[+] shell obtained — uid=0(root) pid={rng.randint(1000,9999)}",
        lambda: f"sqlmap --dump -D db{rng.randint(1,99)} --batch",
        lambda: f"[!] AV bypass failed on host .{rng.randint(10,250)} — retrying",
        lambda: f"msf6 exploit/windows/smb/ms17_010  RHOSTS={rng.randint(1,223)}.{rng.randint(0,255)}.0.0",
        lambda: f"hashcat -m 1000 hashes.txt — {rng.randint(1,40)}% complete",
        lambda: f"[+] C2 callback {rng.randint(1,223)}.{rng.randint(0,255)}.{rng.randint(0,255)}:{rng.randint(1024,65535)}",
        lambda: f"hydra -l admin -P wordlist.txt ssh://{rng.randint(1,223)}.{rng.randint(0,255)}.1.1",
    ]
    return rng.choice(cmds)()


def build_threatwatch_auth(out: Path) -> None:
    _scroll_terminal(out, (8, 4, 6), (180, 180, 255), (80, 60, 120), "kali# ", _tw_line, 101, "EXPLOIT SESSION")


def build_threatwatch_network(out: Path) -> None:
    _matrix_rain(out, (6, 2, 4), (120, 120, 255), (30, 10, 40), 102)


def build_threatwatch_packets(out: Path) -> None:
    def line(rng, _i):
        hx = " ".join(f"{rng.randint(0,255):02x}" for _ in range(16))
        return f"0x{rng.randint(0x7ff00000, 0x7fffffff):08x}  {hx}  // shellcode fragment"
    _scroll_terminal(out, (0, 0, 0), (0, 255, 70), (0, 90, 40), "dump# ", line, 103, "MEMORY HEX DUMP")


def build_threatwatch_spectrum(out: Path) -> None:
    def line(rng, _i):
        return rng.choice([
            f"wireshark: TCP stream {rng.randint(1,9999)} reassembled ({rng.randint(400,9000)} bytes)",
            f"DNS exfil? {rng.randint(80,250)}.{rng.choice(['txt','api','cdn'])}.evil.net",
            f"JA3 fingerprint match — Cobalt Strike beacon",
            f"TLS cert CN=*.microsoft.com SAN mismatch DETECTED",
        ])
    _scroll_terminal(out, (10, 8, 12), (200, 140, 255), (100, 60, 140), "tshark# ", line, 104, "PACKET SNIFFER")


def build_threatwatch_tracking(out: Path) -> None:
    rng = random.Random(105)
    targets: list[str] = []
    writer = _writer(out)
    for i in range(FPS * DURATION_S):
        frame = np.zeros((H, W, 3), dtype=np.uint8)
        frame[:] = (12, 4, 6)
        if i % 8 == 0:
            ip = f"{rng.randint(1,223)}.{rng.randint(0,255)}.{rng.randint(0,255)}.{rng.randint(1,254)}"
            st = rng.choice(["COMPROMISED", "SCANNING", "BEACONING", "EXFIL"])
            targets.insert(0, f"{ip:<22} {st}")
            if len(targets) > 16:
                targets.pop()
        cv2.putText(frame, "TARGET LIST — ACTIVE CAMPAIGN", (24, 36), FONT, 0.6, (200, 200, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "IP                    STATUS", (24, 62), FONT, 0.45, (100, 80, 160), 1, cv2.LINE_AA)
        for j, t in enumerate(targets):
            compromised = "COMPROMISED" in t or "EXFIL" in t
            col = (80, 80, 255) if compromised else (140, 140, 220)
            cv2.putText(frame, t, (24, 90 + j * 28), FONT, 0.5, col, 1, cv2.LINE_AA)
        writer.write(frame)
    writer.release()


THREATWATCH_BUILDERS = [
    build_threatwatch_auth,
    build_threatwatch_network,
    build_threatwatch_packets,
    build_threatwatch_spectrum,
    build_threatwatch_tracking,
]


# ── ORBITAL: blue CRT / radar / countdown ──

def build_orbital_auth(out: Path) -> None:
    def line(rng, _i):
        return rng.choice([
            f"DSN PASS AUTH  GS-{rng.choice(['14','43','55'])}  AOS T+{rng.randint(1,99):02d}:{rng.randint(10,59):02d}",
            f"CREDENTIAL OK  operator {rng.choice(['JPL','ESA','NASA'])}-{rng.randint(100,999)}",
            f"UPLINK KEY rotated — session {rng.randint(10000,99999)}",
            f"TLE verified NORAD {rng.randint(25000,99999)}",
        ])
    _scroll_terminal(out, (16, 12, 8), (255, 220, 160), (120, 100, 60), "dsn> ", line, 201, "GROUND STATION")


def build_orbital_network(out: Path) -> None:
    _radar_sweep(out, (20, 10, 6), (255, 180, 80), (255, 255, 200), 202)


def build_orbital_packets(out: Path) -> None:
    def line(rng, _i):
        return f"CCSDS TM #{rng.randint(100000,999999)}  APID={rng.randint(1,2047)}  {rng.randint(128,2048)} bytes  SNR {rng.randint(12,28)}dB"
    _scroll_terminal(out, (8, 10, 20), (255, 200, 120), (80, 100, 180), "tlm> ", line, 203, "TELEMETRY STREAM")


def build_orbital_spectrum(out: Path) -> None:
    _big_readout(
        out, (10, 8, 24), (255, 220, 100),
        "DOWNLINK SNR",
        lambda i, rng: f"{18 + int(6 * math.sin(i / 15)) + rng.randint(-1, 1)}",
        204, "dB",
    )


def build_orbital_tracking(out: Path) -> None:
    writer = _writer(out)
    for i in range(FPS * DURATION_S):
        frame = np.zeros((H, W, 3), dtype=np.uint8)
        frame[:] = (8, 6, 18)
        secs = max(0, 600 - i * 2)
        m, s = divmod(secs, 60)
        cv2.putText(frame, "ACQUISITION OF SIGNAL", (W // 2 - 220, H // 2 - 100), FONT, 0.8, (180, 140, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"T-{m:02d}:{s:02d}", (W // 2 - 140, H // 2 + 30), FONT, 2.5, (255, 230, 180), 4, cv2.LINE_AA)
        cv2.putText(frame, "NOAA-21  ·  GOLDSTONE DSN-14", (W // 2 - 180, H // 2 + 100), FONT, 0.6, (200, 160, 255), 1, cv2.LINE_AA)
        writer.write(frame)
    writer.release()


ORBITAL_BUILDERS = [
    build_orbital_auth,
    build_orbital_network,
    build_orbital_packets,
    build_orbital_spectrum,
    build_orbital_tracking,
]


# ── LEDGER: amber ticker / blockchain scroll ──

def build_ledger_auth(out: Path) -> None:
    def line(rng, _i):
        return f"SWIFT MT{rng.choice(['103','202','940'])}  REF{rng.randint(100000,999999)}  ${rng.randint(10,999)}K  {rng.choice(['AUTHORIZED','PENDING','BLOCKED'])}"
    _scroll_terminal(out, (8, 10, 14), (180, 220, 255), (80, 100, 140), "swift> ", line, 301, "WIRE GATEWAY")


def build_ledger_network(out: Path) -> None:
    _ticker_columns(out, (6, 8, 12), (150, 200, 255), (80, 160, 255),
                    ["REF", "AMOUNT", "CHG%", "STATUS"], 302)


def build_ledger_packets(out: Path) -> None:
    def line(rng, _i):
        return f"block {rng.randint(18000000, 19000000)}  tx 0x{''.join(rng.choice('0123456789abcdef') for _ in range(16))}...  {rng.randint(1,48)} conf"
    _scroll_terminal(out, (4, 6, 10), (100, 200, 255), (60, 100, 160), "chain> ", line, 303, "BLOCKCHAIN TRACE")


def build_ledger_spectrum(out: Path) -> None:
    rng = random.Random(304)
    writer = _writer(out)
    for i in range(FPS * DURATION_S):
        frame = np.zeros((H, W, 3), dtype=np.uint8)
        frame[:] = (6, 8, 10)
        cv2.putText(frame, "SESSION VOLUME INDEX", (40, 50), FONT, 0.7, (120, 180, 255), 1, cv2.LINE_AA)
        for b in range(40):
            h = int(30 + 280 * abs(math.sin(i / 8 + b * 0.4)) * rng.uniform(0.3, 1.0))
            cv2.rectangle(frame, (40 + b * 22, 420 - h), (58 + b * 22, 420), (40, 160, 255), -1)
        cv2.putText(frame, f"${rng.randint(800,4200)}M", (W - 200, H - 30), FONT, 0.8, (180, 220, 255), 2, cv2.LINE_AA)
        writer.write(frame)
    writer.release()


def build_ledger_tracking(out: Path) -> None:
    def line(rng, _i):
        return f"OFAC MATCH {rng.randint(92,99)}.{rng.randint(10,99)}%  acct ***{rng.randint(1000,9999)}  {rng.choice(['FREEZE', 'REVIEW', 'CLEARED'])}"
    _scroll_terminal(out, (10, 8, 6), (120, 200, 255), (70, 90, 130), "sar> ", line, 305, "SANCTIONS WATCH")


LEDGER_BUILDERS = [
    build_ledger_auth,
    build_ledger_network,
    build_ledger_packets,
    build_ledger_spectrum,
    build_ledger_tracking,
]


# ── GRIDOPS: green SCADA / alarms / big frequency ──

def build_gridops_auth(out: Path) -> None:
    def line(rng, _i):
        return f"OPERATOR {rng.choice(['J.Smith','M.Chen','R.Davis'])} badge {rng.randint(1000,9999)}  {rng.choice(['LOGIN OK','MFA OK','SHIFT START'])}  PLC zone {rng.randint(1,12)}"
    _scroll_terminal(out, (4, 8, 4), (180, 255, 120), (60, 120, 50), "ics> ", line, 401, "OPERATOR LOG")


def build_gridops_network(out: Path) -> None:
    _big_readout(
        out, (4, 10, 4), (200, 255, 150),
        "GRID FREQUENCY",
        lambda i, _rng: f"60.{(500 + int(50 * math.sin(i / 25))):03d}",
        402, "Hz",
    )


def build_gridops_packets(out: Path) -> None:
    def line(rng, _i):
        return f"MODBUS FC{rng.choice(['03','04','06','16'])}  reg {40000 + rng.randint(0,999)}  val {rng.randint(0,65535)}  RTU-{rng.randint(1,48)}"
    _scroll_terminal(out, (2, 6, 2), (170, 255, 100), (50, 100, 40), "modbus> ", line, 403, "REGISTER POLL")


def build_gridops_spectrum(out: Path) -> None:
    _big_readout(
        out, (6, 12, 6), (150, 255, 200),
        "SYSTEM LOAD",
        lambda i, rng: f"{rng.randint(8200, 9400) + int(200 * math.sin(i / 18))}",
        404, "MW",
    )


def build_gridops_tracking(out: Path) -> None:
    _alarm_board(out, (4, 8, 4), (120, 255, 100), (80, 200, 255), (80, 80, 255), 405)


GRIDOPS_BUILDERS = [
    build_gridops_auth,
    build_gridops_network,
    build_gridops_packets,
    build_gridops_spectrum,
    build_gridops_tracking,
]


THEME_BUILDER_MAP = {
    "threatwatch": THREATWATCH_BUILDERS,
    "orbital": ORBITAL_BUILDERS,
    "ledger": LEDGER_BUILDERS,
    "gridops": GRIDOPS_BUILDERS,
}

"""Original netdefense video feeds — unchanged multi-panel monitors."""

from __future__ import annotations

import math
import random
from pathlib import Path

import cv2
import numpy as np

W, H = 960, 540
FPS = 30
DURATION_S = 10


def _writer(path: Path) -> cv2.VideoWriter:
    wr = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), FPS, (W, H))
    if not wr.isOpened():
        wr = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"avc1"), FPS, (W, H))
    return wr


def _base_canvas() -> np.ndarray:
    c = np.zeros((H, W, 3), dtype=np.uint8)
    c[:] = (8, 12, 16)
    return c


def _hud(frame: np.ndarray, title: str, frame_i: int, extra: str = "") -> None:
    cv2.rectangle(frame, (0, 0), (W, 36), (4, 8, 12), -1)
    cv2.rectangle(frame, (0, H - 28), (W, H), (4, 8, 12), -1)
    cv2.putText(frame, f">> {title}", (12, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (120, 200, 170), 1, cv2.LINE_AA)
    ts = f"T+{frame_i // FPS:02d}:{frame_i % FPS:02d}"
    cv2.putText(frame, ts, (W - 110, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (90, 150, 130), 1, cv2.LINE_AA)
    cv2.putText(frame, "LIVE MONITORING", (12, H - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (70, 110, 90), 1, cv2.LINE_AA)
    if extra:
        cv2.putText(frame, extra, (W - 340, H - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (90, 160, 130), 1, cv2.LINE_AA)


def _panel(frame: np.ndarray, x: int, y: int, pw: int, ph: int, title: str) -> None:
    cv2.rectangle(frame, (x, y), (x + pw, y + ph), (18, 40, 35), 1)
    cv2.rectangle(frame, (x, y), (x + pw, y + 22), (12, 28, 24), -1)
    cv2.putText(frame, title, (x + 6, y + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (90, 170, 140), 1, cv2.LINE_AA)


def _noise_patch(frame: np.ndarray, intensity: int = 10) -> None:
    frame[:] = cv2.add(frame, np.random.randint(0, intensity, frame.shape, dtype=np.uint8))


def build_auth_gateway(out: Path) -> None:
    rng = random.Random(31)
    events: list[str] = []
    blocked: list[str] = []
    writer = _writer(out)
    fails = 847
    ok = 1203
    for i in range(FPS * DURATION_S):
        frame = _base_canvas()
        _panel(frame, 10, 44, 620, 430, "AUTH GATEWAY — LIVE SESSIONS")
        if i % 4 == 0:
            user = rng.choice(["admin", "root", "operator", "netops", "svc-backup", "deploy"])
            ip = f"{rng.randint(1,223)}.{rng.randint(0,255)}.{rng.randint(0,255)}.{rng.randint(1,254)}"
            if rng.random() > 0.35:
                ok += 1
                events.insert(0, f"OK   {user}@{ip}  token issued")
            else:
                fails += 1
                events.insert(0, f"FAIL {user}@{ip}  bad credential")
                if rng.random() < 0.25:
                    blocked.insert(0, ip)
                    if len(blocked) > 8:
                        blocked.pop()
            if len(events) > 16:
                events.pop()
        for b in range(12):
            bx = 30 + b * 48
            hbar = int(30 + 120 * abs(math.sin(i / 8 + b * 0.9)))
            col = (50, 160, 120) if b % 3 else (40, 100, 180)
            cv2.rectangle(frame, (bx, 380 - hbar), (bx + 32, 380), col, -1)
        for j, ev in enumerate(events):
            col = (100, 230, 170) if ev.startswith("OK") else (120, 100, 255)
            cv2.putText(frame, ev[:52], (22, 78 + j * 24), cv2.FONT_HERSHEY_SIMPLEX, 0.4, col, 1, cv2.LINE_AA)
        if fails > 900 and i % 18 < 9:
            cv2.putText(frame, "!! BRUTE FORCE DETECTED — RATE LIMIT ACTIVE", (170, 66),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (140, 120, 255), 1, cv2.LINE_AA)
        _panel(frame, 640, 44, 310, 200, "BLOCKED IPS")
        for j, ip in enumerate(blocked):
            cv2.putText(frame, f"BLOCK  {ip}", (650, 78 + j * 22), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (180, 100, 255), 1, cv2.LINE_AA)
        _panel(frame, 640, 250, 310, 224, "SESSION METRICS")
        cv2.putText(frame, f"SUCCESS:  {ok}", (650, 285), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (80, 200, 150), 1)
        cv2.putText(frame, f"FAILED:   {fails}", (650, 315), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (140, 110, 255), 1)
        _hud(frame, "AUTH GATEWAY MONITOR", i, f"ACTIVE SESSIONS: {ok % 200 + 40}")
        writer.write(frame)
    writer.release()


def build_network(out: Path) -> None:
    rng = random.Random(11)
    nodes = [(120, 120), (280, 90), (440, 110), (600, 130), (780, 100), (150, 240), (320, 220),
             (500, 250), (680, 230), (850, 260), (200, 370), (400, 360), (600, 380), (780, 350)]
    labels = ["IX-NY", "RTR-01", "FW-EAST", "CDN-01", "BGP-HUB", "MPLS-02", "CORE-DC", "FW-WEST",
              "SAT-UPL", "MIRROR", "PEER-LON", "PEER-FRA", "PEER-TYO", "PEER-SYD"]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (8, 4),
             (5, 9), (9, 10), (10, 11), (11, 12), (12, 13), (6, 11), (2, 6), (3, 8)]
    packets = [{"e": k % len(edges), "t": rng.random(), "hot": k % 5 == 0} for k in range(55)]
    events: list[str] = []
    writer = _writer(out)
    for i in range(FPS * DURATION_S):
        frame = _base_canvas()
        _panel(frame, 10, 44, 620, 430, "BACKBONE TOPOLOGY")
        ddos = (i // 90) % 3 == 0 and (i % 90) < 45
        wave = (i * 2) % len(nodes)
        for a, b in edges:
            col = (40, 120, 80) if ddos and (a == wave or b == wave) else (25, 60, 50)
            cv2.line(frame, nodes[a], nodes[b], col, 1)
        for p in packets:
            p["t"] = (p["t"] + (0.025 if ddos else 0.014)) % 1.0
            a, b = edges[p["e"]]
            x1, y1 = nodes[a]
            x2, y2 = nodes[b]
            px = int(x1 + (x2 - x1) * p["t"])
            py = int(y1 + (y2 - y1) * p["t"])
            cv2.circle(frame, (px, py), 4, (100, 230, 170), -1)
        for j, ((x, y), lbl) in enumerate(zip(nodes, labels)):
            cv2.circle(frame, (x, y), 10, (30, 120, 120), -1)
            cv2.putText(frame, lbl, (x - 24, y + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (70, 130, 110), 1, cv2.LINE_AA)
        if i % 20 == 0:
            events.insert(0, f"ROUTE ADV {labels[rng.randint(0, 13)]} → AS{rng.randint(1000, 9999)}")
            if len(events) > 14:
                events.pop()
        _panel(frame, 640, 44, 310, 430, "EVENT STREAM")
        for j, ev in enumerate(events):
            cv2.putText(frame, ev[:38], (650, 78 + j * 26), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (65, 140, 115), 1, cv2.LINE_AA)
        _hud(frame, "NETWORK TRAFFIC MESH", i, f"{'DDOS ACTIVE' if ddos else 'NOMINAL'}")
        writer.write(frame)
    writer.release()


def build_packets(out: Path) -> None:
    rng = random.Random(3)
    hex_lines: list[str] = []
    decode: list[str] = []
    alerts: list[list] = []
    writer = _writer(out)
    total = 12847
    for i in range(FPS * DURATION_S):
        frame = _base_canvas()
        total += rng.randint(3, 18)
        for _ in range(2):
            hexpart = " ".join(f"{rng.randint(0, 255):02X}" for _ in range(14))
            hex_lines.append(f"#{total:06d}  {hexpart}")
            if len(hex_lines) > 14:
                hex_lines.pop(0)
        if i % 8 == 0:
            decode.insert(0, f"[TCP] len={rng.randint(64, 1500)}")
            if len(decode) > 10:
                decode.pop()
        _panel(frame, 10, 44, 520, 430, "HEX STREAM")
        for j, line in enumerate(hex_lines):
            cv2.putText(frame, line, (20, 72 + j * 26), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (55, 115, 95), 1, cv2.LINE_AA)
        _panel(frame, 540, 44, 410, 250, "PROTOCOL DECODE")
        for j, line in enumerate(decode):
            cv2.putText(frame, line, (550, 78 + j * 22), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (80, 180, 150), 1, cv2.LINE_AA)
        _hud(frame, "DEEP PACKET CAPTURE", i, f"PKTS: {total:,}")
        _noise_patch(frame, 8)
        writer.write(frame)
    writer.release()


def _waterfall_color(v: float) -> tuple[int, int, int]:
    v = max(0.0, min(1.0, v))
    if v < 0.25:
        return (0, int(v * 400), int(80 + v * 300))
    if v < 0.65:
        return (0, int(180 + v * 80), int(200 - v * 100))
    return (0, int(200 + v * 55), int(40 + v * 60))


def build_spectrum(out: Path) -> None:
    rng = random.Random(19)
    bins = 256
    wf_h = 280
    waterfall = np.zeros((wf_h, bins, 3), dtype=np.uint8)
    carriers = [{"bin": rng.randint(20, bins - 20), "drift": rng.uniform(-0.15, 0.15),
                 "width": rng.randint(2, 8), "str": rng.uniform(0.4, 0.95)} for _ in range(8)]
    writer = _writer(out)
    wf_x, wf_y, wf_w = 20, 175, W - 40
    for i in range(FPS * DURATION_S):
        frame = _base_canvas()
        frame[:] = (2, 4, 8)
        _panel(frame, 10, 44, W - 20, 130, "AUDIO WAVEFORM — MONITOR OUT")
        wave_pts = []
        for x in range(wf_x + 4, wf_x + wf_w - 4, 3):
            amp = math.sin((x + i * 8) / 40) * 0.35
            wave_pts.append((x, int(110 + amp * 55)))
        if len(wave_pts) > 2:
            for k in range(1, len(wave_pts)):
                cv2.line(frame, wave_pts[k - 1], wave_pts[k], (60, 220, 180), 1, cv2.LINE_AA)
        _panel(frame, 10, 178, W - 20, 300, "SDR WATERFALL — 20M BAND")
        row = np.zeros(bins, dtype=np.float32)
        row += np.array([rng.uniform(0, 0.06) for _ in range(bins)], dtype=np.float32)
        for c in carriers:
            c["bin"] = (c["bin"] + c["drift"]) % bins
            b = int(c["bin"])
            for dw in range(-c["width"], c["width"] + 1):
                row[(b + dw) % bins] = max(row[(b + dw) % bins], c["str"])
        waterfall = np.roll(waterfall, 1, axis=0)
        for b in range(bins):
            waterfall[0, b] = _waterfall_color(float(row[b]))
        cell_w = max(1, (wf_w - 8) // bins)
        for wy in range(wf_h):
            for bx in range(bins):
                x1 = wf_x + 4 + bx * cell_w
                y1 = wf_y + 24 + int(wy * (wf_h - 28) / wf_h)
                cv2.rectangle(frame, (x1, y1), (x1 + cell_w, y1 + max(1, (wf_h - 28) // wf_h)),
                              tuple(int(c) for c in waterfall[wy, bx]), -1)
        _hud(frame, "HAM RADIO SDR WATERFALL", i, "14.000–14.350 MHz")
        writer.write(frame)
    writer.release()


def build_tracking(out: Path) -> None:
    rng = random.Random(23)
    sats = [{"name": n, "lon": rng.uniform(-180, 180), "spd": rng.uniform(0.8, 2.2),
             "lat": rng.uniform(-40, 60), "alt": rng.randint(380, 1200)}
            for n in ["USA-284", "NOAA-21", "GOES-18"]]
    track_pts: list[tuple[int, int]] = []
    telemetry: list[str] = []
    writer = _writer(out)
    for i in range(FPS * DURATION_S):
        frame = _base_canvas()
        _panel(frame, 10, 44, 620, 430, "SATELLITE GROUND TRACK")
        for lon in range(-180, 181, 30):
            x = int(30 + (lon + 180) / 360 * 560)
            cv2.line(frame, (x, 70), (x, 440), (15, 35, 30), 1)
        active = i // 80 % 3
        for si, sat in enumerate(sats):
            sat["lon"] = (sat["lon"] + sat["spd"]) % 360 - 180
            sx = int(30 + (sat["lon"] + 180) / 360 * 560)
            sy = int(440 - (sat["lat"] + 60) / 120 * 370)
            if si == active:
                track_pts.append((sx, sy))
            col = (80, 220, 180) if si == active else (50, 100, 85)
            cv2.circle(frame, (sx, sy), 8, col, -1)
            cv2.putText(frame, sat["name"], (sx + 12, sy - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.38, col, 1)
        _panel(frame, 640, 44, 310, 430, "TELEMETRY DOWNLINK")
        if i % 15 == 0:
            s = sats[active]
            telemetry.insert(0, f"{s['name']}  LAT {s['lat']:+.2f}  LON {s['lon']:+.1f}")
            if len(telemetry) > 14:
                telemetry.pop()
        for j, line in enumerate(telemetry):
            cv2.putText(frame, line, (650, 78 + j * 26), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (65, 140, 115), 1, cv2.LINE_AA)
        _hud(frame, "SATELLITE TRACKING", i, f"ACTIVE: {sats[active]['name']}")
        writer.write(frame)
    writer.release()


NETDEFENSE_BUILDERS = [
    build_auth_gateway,
    build_network,
    build_packets,
    build_spectrum,
    build_tracking,
]

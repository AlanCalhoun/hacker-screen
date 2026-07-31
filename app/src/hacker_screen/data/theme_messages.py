"""Theme-specific session log messages and boot sequences."""

from __future__ import annotations

import random
from datetime import datetime

from hacker_screen.data import messages as net


def boot_sequence(theme_id: str) -> list[tuple[str, str]]:
    boots = {
        "netdefense": [
            ("Session authenticated — operator NET-7741", "success"),
            ("BGP feed connected — 42 peers online", "info"),
            ("Packet mirror SPAN-02 active on backbone IX", "info"),
            ("Route table synced — 942,881 prefixes", "success"),
            ("Telemetry link to ground stations: OK", "info"),
            ("─" * 58, "info"),
        ],
        "threatwatch": [
            ("Threat feed ingesting — 18,402 IOCs loaded", "success"),
            ("YARA rules compiled — 2,847 signatures active", "info"),
            ("Sandbox cluster online — 6 VMs ready", "info"),
            ("C2 domain sinkhole routing: ENABLED", "warn"),
            ("Reverse-engineering queue: 14 samples pending", "info"),
            ("─" * 58, "info"),
        ],
        "orbital": [
            ("Pass predictor online — 847 TLEs current", "success"),
            ("Goldstone 70m dish — acquisition ready", "info"),
            ("Multi-spectral pipeline calibrated", "info"),
            ("Orbital debris catalog synced — NORAD feed", "success"),
            ("Next pass: NOAA-21 @ 14:32 UTC", "info"),
            ("─" * 58, "info"),
        ],
        "ledger": [
            ("SWIFT MT103 monitor — session established", "success"),
            ("Sanctions list OFAC-2026 synced", "info"),
            ("Blockchain indexer connected — 12 chains", "info"),
            ("Suspicious activity threshold: $50,000 USD", "warn"),
            ("Correspondent bank feeds: 34 active", "success"),
            ("─" * 58, "info"),
        ],
        "gridops": [
            ("SCADA master station — link OK", "success"),
            ("IEC 61850 GOOSE subscriptions active", "info"),
            ("Substation RTU poll cycle: 2.0s", "info"),
            ("NERC CIP compliance scan: PASS", "success"),
            ("Load forecast model updated — peak +4.2%", "warn"),
            ("─" * 58, "info"),
        ],
    }
    return boots.get(theme_id, boots["netdefense"])


def _line(theme_id: str, action: str, template: str, tag: str) -> tuple[str, str]:
    ts = datetime.now().strftime("%H:%M:%S")
    msg = f"{ts} [{action}] " + template.format(
        target=net._ip(),
        domain=random.choice(net.DOMAINS),
        n=random.randint(1, 9999),
        hex="".join(random.choice("0123456789ABCDEF") for _ in range(8)),
        city=random.choice(net.CITY_NAMES),
        method=random.choice(net.METHODS).format(n=random.randint(1000, 9999)),
        wallet=f"0x{''.join(random.choice('0123456789abcdef') for _ in range(8))}",
        hash=net._ip(),
    )
    return msg, tag


_THREAT_ACTIONS = [
    ("MALWARE", "Trojan.{method} detected on {target}", "alert"),
    ("C2", "Beacon interval 60s — callback {domain}", "warn"),
    ("IOC", "Hash {hex} matches APT-29 cluster", "alert"),
    ("SANDBOX", "Sample detonated — score {n}/100", "info"),
    ("PHISH", "Credential harvest on {domain} blocked", "warn"),
    ("LATERAL", "SMB pivot attempt {target} ← {city}", "alert"),
    ("YARA", "Rule match: MAL_{hex} on endpoint", "success"),
    ("SINK", "C2 domain {domain} redirected to honeypot", "success"),
]

_ORBITAL_ACTIONS = [
    ("PASS", "AOS {city} GS — object NORAD {n}", "info"),
    ("TLE", "Orbital update — inclination {n}.2°", "info"),
    ("DOWN", "Downlink {n} Mbps — SNR 18.4 dB", "success"),
    ("LOS", "Loss of signal predicted in {n} min", "warn"),
    ("TRACK", "Object {hex} crossing {city} footprint", "info"),
    ("MANEUVER", "Delta-V event detected — obj {n}", "alert"),
    ("IMG", "Frame {n} received — cloud cover 12%", "success"),
    ("DOPPLER", "Shift +{n} Hz — pass stable", "info"),
]

_LEDGER_ACTIONS = [
    ("SWIFT", "MT103 ${n}K — {city} → {target}", "info"),
    ("FLAG", "Sanctions hit on wallet {wallet}...", "alert"),
    ("MIXER", "Tornado deposit {n} ETH traced", "warn"),
    ("KYC", "Beneficiary mismatch — acct {target}", "warn"),
    ("BLOCK", "Transfer frozen — ref {hex}", "alert"),
    ("CHAIN", "Bridge tx confirmed — block {n}", "info"),
    ("SAR", "Suspicious activity report filed", "success"),
    ("OFAC", "Entity match 98.{n}% — {domain}", "alert"),
    ("FEDWIRE", "Fed settlement ${n}M — FRB-NY cleared", "success"),
    ("FX", "EUR/USD 1.08{n} — desk hedge executed", "info"),
    ("CHIPS", "CHIPS net settle ${n}M — multilateral", "info"),
]

_GRID_ACTIONS = [
    ("RTU", "Modbus read coil {n} @ {target}", "info"),
    ("TRIP", "Breaker OPEN — feeder {city}-F{n}", "alert"),
    ("LOAD", "Substation load {n}% — nominal", "info"),
    ("FREQ", "Grid frequency 59.98 Hz — stable", "success"),
    ("PLC", "Setpoint changed register 400{n}", "warn"),
    ("ALARM", "Overvoltage detected bus {target}", "alert"),
    ("RESTORE", "Automatic reclose successful", "success"),
    ("POLL", "IEC 61850 GOOSE from {domain}", "info"),
    ("BLACKOUT", "Rolling shed Stage {n} — {city} sector", "alert"),
    ("SHED", "847 MW dropped — HV feeder OPEN", "alert"),
    ("ISO", "Emergency order E-2026-{n} — load curtailment", "warn"),
    ("RELAY", "SEL-421 trip signal latched bay {n}", "alert"),
]


def generate_line(theme_id: str) -> tuple[str, str]:
    if theme_id == "netdefense":
        return net.generate_line()
    pools = {
        "threatwatch": _THREAT_ACTIONS,
        "orbital": _ORBITAL_ACTIONS,
        "ledger": _LEDGER_ACTIONS,
        "gridops": _GRID_ACTIONS,
    }
    action, template, tag = random.choice(pools.get(theme_id, _THREAT_ACTIONS))
    return _line(theme_id, action, template, tag)

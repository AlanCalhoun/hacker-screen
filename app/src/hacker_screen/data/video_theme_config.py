"""Per-console video palettes and feed labels (OpenCV BGR colors)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ThemeConfig:
    theme_id: str
    seed: int
    bg: tuple[int, int, int]
    hud_bg: tuple[int, int, int]
    text_primary: tuple[int, int, int]
    text_bright: tuple[int, int, int]
    text_dim: tuple[int, int, int]
    text_warn: tuple[int, int, int]
    panel_border: tuple[int, int, int]
    panel_header: tuple[int, int, int]
    grid: tuple[int, int, int]
    bar_ok: tuple[int, int, int]
    bar_alt: tuple[int, int, int]
    bar_warn: tuple[int, int, int]
    node_fill: tuple[int, int, int]
    packet: tuple[int, int, int]
    packet_hot: tuple[int, int, int]
    waterfall: str  # green | red | blue | gold | lime
    auth_panel: str
    auth_hud: str
    auth_blocked: str
    auth_alert: str
    network_panel: str
    network_hud: str
    network_event_panel: str
    network_labels: list[str]
    network_ddos_msg: str
    packets_panel: str
    packets_hud: str
    packets_decode: str
    packets_alerts: str
    spectrum_panel: str
    spectrum_wave: str
    spectrum_hud: str
    spectrum_band: str
    tracking_panel: str
    tracking_hud: str
    tracking_telem: str
    tracking_orbit: str
    sat_names: list[str]
    feed_titles: dict[str, str] = field(default_factory=dict)


def _titles(prefix: str, a: str, b: str, c: str, d: str, e: str) -> dict[str, str]:
    return {
        "feed_auth": a,
        "feed_network": b,
        "feed_packets": c,
        "feed_spectrum": d,
        "feed_tracking": e,
    }


THEME_CONFIGS: dict[str, ThemeConfig] = {
    "netdefense": ThemeConfig(
        theme_id="netdefense",
        seed=31,
        bg=(8, 12, 16),
        hud_bg=(4, 8, 12),
        text_primary=(120, 200, 170),
        text_bright=(100, 230, 170),
        text_dim=(65, 140, 115),
        text_warn=(90, 140, 255),
        panel_border=(18, 40, 35),
        panel_header=(12, 28, 24),
        grid=(15, 35, 30),
        bar_ok=(50, 160, 120),
        bar_alt=(40, 100, 180),
        bar_warn=(120, 60, 200),
        node_fill=(30, 120, 120),
        packet=(100, 230, 170),
        packet_hot=(80, 200, 255),
        waterfall="green",
        auth_panel="AUTH GATEWAY — LIVE SESSIONS",
        auth_hud="AUTH GATEWAY MONITOR",
        auth_blocked="BLOCKED IPS",
        auth_alert="!! BRUTE FORCE DETECTED — RATE LIMIT ACTIVE",
        network_panel="BACKBONE TOPOLOGY",
        network_hud="NETWORK TRAFFIC MESH",
        network_event_panel="EVENT STREAM",
        network_labels=[
            "IX-NY", "RTR-01", "FW-EAST", "CDN-01", "BGP-HUB", "MPLS-02", "CORE-DC",
            "FW-WEST", "SAT-UPL", "MIRROR", "PEER-LON", "PEER-FRA", "PEER-TYO", "PEER-SYD",
        ],
        network_ddos_msg="!! DDoS MITIGATED on {lbl} — {n} pps",
        packets_panel="HEX STREAM",
        packets_hud="DEEP PACKET CAPTURE",
        packets_decode="PROTOCOL DECODE",
        packets_alerts="ALERTS",
        spectrum_panel="SDR WATERFALL — 20M BAND",
        spectrum_wave="AUDIO WAVEFORM — MONITOR OUT",
        spectrum_hud="HAM RADIO SDR WATERFALL",
        spectrum_band="14.000–14.350 MHz",
        tracking_panel="SATELLITE GROUND TRACK",
        tracking_hud="SATELLITE TRACKING",
        tracking_telem="TELEMETRY DOWNLINK",
        tracking_orbit="ORBIT",
        sat_names=["USA-284", "NOAA-21", "GOES-18"],
        feed_titles=_titles(
            "netdefense",
            "AUTH GATEWAY MONITOR",
            "NETWORK TRAFFIC MESH",
            "DEEP PACKET CAPTURE",
            "HAM RADIO SDR WATERFALL",
            "SATELLITE TRACKING",
        ),
    ),
    "threatwatch": ThemeConfig(
        theme_id="threatwatch",
        seed=47,
        bg=(8, 4, 6),
        hud_bg=(12, 4, 6),
        text_primary=(120, 120, 220),
        text_bright=(100, 100, 255),
        text_dim=(80, 70, 180),
        text_warn=(80, 160, 255),
        panel_border=(35, 20, 28),
        panel_header=(24, 12, 18),
        grid=(30, 15, 20),
        bar_ok=(50, 60, 200),
        bar_alt=(80, 40, 180),
        bar_warn=(40, 80, 255),
        node_fill=(40, 40, 160),
        packet=(100, 100, 255),
        packet_hot=(80, 140, 255),
        waterfall="red",
        auth_panel="HONEYPOT — INTRUSION LOG",
        auth_hud="INTRUSION TRAP MONITOR",
        auth_blocked="QUARANTINED HOSTS",
        auth_alert="!! RANSOMWARE BEACON DETECTED — ISOLATING",
        network_panel="BOTNET C2 TOPOLOGY",
        network_hud="C2 TRAFFIC MESH",
        network_event_panel="MALWARE EVENTS",
        network_labels=[
            "C2-01", "BOT-A", "DROP", "PAYLOAD", "EXFIL", "PROXY", "TOR-GW",
            "LOADER", "STAGE-2", "HK-SINK", "SANDBOX", "IOC-FEED", "YARA", "SIG-DB",
        ],
        network_ddos_msg="!! C2 BURST on {lbl} — {n} beacons/s",
        packets_panel="SAMPLE HEX DUMP",
        packets_hud="MALWARE DISSECTION",
        packets_decode="BEHAVIOR DECODE",
        packets_alerts="IOC MATCHES",
        spectrum_panel="RF C2 SIGNATURE SCAN",
        spectrum_wave="BEACON TIMING — WAVEFORM",
        spectrum_hud="C2 SPECTRUM ANALYZER",
        spectrum_band="433–434 MHz ISM",
        tracking_panel="THREAT ORIGIN MAP",
        tracking_hud="APT GEO TRACKING",
        tracking_telem="EXFIL DOWNLINK",
        tracking_orbit="CAMPAIGN",
        sat_names=["APT-29", "LAZ-GRP", "C2-NK", "LOCKBIT"],
        feed_titles=_titles(
            "threatwatch",
            "EXPLOIT TERMINAL",
            "MATRIX C2 RAIN",
            "SHELLCODE HEX DUMP",
            "WIRESHARK SNIFFER",
            "TARGET TRACKER",
        ),
    ),
    "orbital": ThemeConfig(
        theme_id="orbital",
        seed=59,
        bg=(8, 8, 16),
        hud_bg=(8, 8, 18),
        text_primary=(200, 170, 120),
        text_bright=(230, 190, 100),
        text_dim=(140, 115, 65),
        text_warn=(255, 180, 90),
        panel_border=(40, 28, 18),
        panel_header=(28, 20, 12),
        grid=(30, 28, 15),
        bar_ok=(120, 160, 50),
        bar_alt=(180, 140, 40),
        bar_warn=(200, 120, 40),
        node_fill=(100, 120, 30),
        packet=(170, 200, 100),
        packet_hot=(255, 220, 80),
        waterfall="blue",
        auth_panel="GROUND STATION — PASS AUTH",
        auth_hud="DSN ACCESS GATEWAY",
        auth_blocked="REVOKED CREDENTIALS",
        auth_alert="!! UNAUTHORIZED UPLINK ATTEMPT",
        network_panel="CONSTELLATION LINK MAP",
        network_hud="ORBITAL DATA MESH",
        network_event_panel="PASS EVENTS",
        network_labels=[
            "GS-GOLD", "DSN-14", "CANB", "MADR", "LEO-1", "MEO-3", "GEO-S",
            "STAR-X", "ISS", "HST", "NOAA", "GPS-III", "RELAY", "TTC",
        ],
        network_ddos_msg="!! DOWNLINK CONGESTION {lbl} — {n} Mbps",
        packets_panel="TELEMETRY FRAMES",
        packets_hud="CCSDS FRAME CAPTURE",
        packets_decode="SPACE PROTOCOL DECODE",
        packets_alerts="ANOMALY FLAGS",
        spectrum_panel="DOWNLINK SPECTRUM — S-BAND",
        spectrum_wave="CARRIER WAVEFORM — IF OUT",
        spectrum_hud="RF DOWNLINK WATERFALL",
        spectrum_band="2.2–2.3 GHz S-BAND",
        tracking_panel="ORBITAL GROUND TRACK",
        tracking_hud="SATELLITE PASS TRACKER",
        tracking_telem="LIVE TELEMETRY",
        tracking_orbit="ORBIT VIEW",
        sat_names=["NOAA-21", "ISS-ZARYA", "GOES-18"],
        feed_titles=_titles(
            "orbital",
            "DSN GROUND TERMINAL",
            "ORBITAL RADAR SWEEP",
            "CCSDS TELEMETRY",
            "SNR READOUT",
            "AOS COUNTDOWN",
        ),
    ),
    "ledger": ThemeConfig(
        theme_id="ledger",
        seed=71,
        bg=(4, 8, 12),
        hud_bg=(4, 10, 14),
        text_primary=(170, 200, 120),
        text_bright=(190, 230, 100),
        text_dim=(115, 140, 65),
        text_warn=(255, 200, 90),
        panel_border=(35, 40, 18),
        panel_header=(24, 28, 12),
        grid=(30, 35, 15),
        bar_ok=(50, 170, 200),
        bar_alt=(40, 140, 180),
        bar_warn=(40, 100, 255),
        node_fill=(80, 120, 30),
        packet=(170, 230, 100),
        packet_hot=(255, 200, 80),
        waterfall="gold",
        auth_panel="SWIFT — SESSION GATEWAY",
        auth_hud="BANKING AUTH MONITOR",
        auth_blocked="FROZEN ACCOUNTS",
        auth_alert="!! SANCTIONS HIT — TRANSFER BLOCKED",
        network_panel="CORRESPONDENT BANK MESH",
        network_hud="PAYMENT ROUTING MESH",
        network_event_panel="TRANSACTION EVENTS",
        network_labels=[
            "SWIFT", "CHIPS", "FED", "SEPA", "CHAPS", "TARGET", "JPM-GW",
            "HSBC", "UBS", "DB-NY", "CITI", "BRIDGE", "MIXER", "KYC",
        ],
        network_ddos_msg="!! SURGE on {lbl} — {n} tx/s",
        packets_panel="BLOCKCHAIN HEX",
        packets_hud="LEDGER TRACE CAPTURE",
        packets_decode="TX DECODE",
        packets_alerts="SAR ALERTS",
        spectrum_panel="MARKET FREQUENCY HEATMAP",
        spectrum_wave="ORDER FLOW — WAVEFORM",
        spectrum_hud="MARKET SPECTRUM MONITOR",
        spectrum_band="T+0 SESSION WINDOW",
        tracking_panel="GLOBAL FUNDS FLOW",
        tracking_hud="ASSET FLOW TRACKER",
        tracking_telem="WIRE LOG",
        tracking_orbit="CORRIDOR",
        sat_names=["SWIFT-NY", "FED-CHI", "EUR-CB", "SG-HUB"],
        feed_titles=_titles(
            "ledger",
            "SWIFT WIRE TERMINAL",
            "LIVE TICKER BOARD",
            "BLOCKCHAIN TRACE",
            "VOLUME BAR CHART",
            "SANCTIONS WATCH",
        ),
    ),
    "gridops": ThemeConfig(
        theme_id="gridops",
        seed=83,
        bg=(4, 8, 6),
        hud_bg=(6, 10, 8),
        text_primary=(150, 220, 120),
        text_bright=(170, 255, 100),
        text_dim=(85, 140, 55),
        text_warn=(80, 200, 255),
        panel_border=(35, 40, 18),
        panel_header=(24, 28, 12),
        grid=(30, 40, 15),
        bar_ok=(50, 200, 80),
        bar_alt=(40, 180, 120),
        bar_warn=(40, 140, 255),
        node_fill=(60, 140, 30),
        packet=(150, 255, 100),
        packet_hot=(255, 220, 80),
        waterfall="lime",
        auth_panel="SCADA — OPERATOR LOGIN",
        auth_hud="ICS ACCESS MONITOR",
        auth_blocked="LOCKED RTUs",
        auth_alert="!! UNAUTHORIZED PLC WRITE ATTEMPT",
        network_panel="SUBSTATION TOPOLOGY",
        network_hud="GRID FIELD BUS MESH",
        network_event_panel="SCADA EVENTS",
        network_labels=[
            "SS-14", "RTU-7", "PLC-A", "IED-1", "HMI", "GW-N", "FEEDER",
            "BREAKER", "TURB", "SOLAR", "WIND", "HYDRO", "NUC", "PMU",
        ],
        network_ddos_msg="!! FAULT CURRENT on {lbl} — {n} A",
        packets_panel="MODBUS REGISTER DUMP",
        packets_hud="ICS PROTOCOL CAPTURE",
        packets_decode="REGISTER DECODE",
        packets_alerts="GRID ALARMS",
        spectrum_panel="POWER FREQUENCY SCAN",
        spectrum_wave="GRID FREQUENCY — WAVEFORM",
        spectrum_hud="FREQUENCY MONITOR 60Hz",
        spectrum_band="59.5–60.5 Hz",
        tracking_panel="TRANSMISSION GRID MAP",
        tracking_hud="LOAD FLOW TRACKER",
        tracking_telem="SCADA TELEMETRY",
        tracking_orbit="REGION",
        sat_names=["TEX-W", "NEV-S", "WASH-H", "GEO-N"],
        feed_titles=_titles(
            "gridops",
            "ICS OPERATOR LOG",
            "GRID FREQUENCY",
            "MODBUS REGISTER POLL",
            "SYSTEM LOAD MW",
            "SCADA ALARM PANEL",
        ),
    ),
}


def get_video_config(theme_id: str) -> ThemeConfig:
    return THEME_CONFIGS[theme_id]


def all_theme_ids() -> list[str]:
    return list(THEME_CONFIGS.keys())

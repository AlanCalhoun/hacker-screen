"""Visual themes for the five operations consoles."""

from __future__ import annotations

from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class ConsoleTheme:
    id: str
    name: str
    button_label: str
    button_desc: str
    window_title: str
    header_title: str
    status_live: str
    bg: str
    header_bg: str
    panel_fg: str
    panel_border: str
    accent: str
    accent2: str
    title_color: str
    label_muted: str
    btn_fg: str
    btn_hover: str
    btn_border: str
    terminal_header: str
    terminal_fg: str
    terminal_bg: str
    terminal_border: str
    tag_colors: dict[str, str]
    map_arc_colors: list[str]
    map_scan: str
    map_node: str
    map_node_fill: str
    map_label: str
    map_hud: str
    map_border: str
    inner_bg: str
    session_log_title: str
    map_title: str
    backbone_title: str
    tunnels_title: str
    video_title: str
    ops_title: str
    hex_title: str
    graph_title: str
    endpoints_title: str
    sat_title: str
    classification: str
    stats_prefix: str
    graph_line: str
    graph_fill: str
    progress_color: str
    endpoints: list[str] = field(default_factory=list)
    sat_stations: list[tuple[str, str, str]] = field(default_factory=list)


THEMES: dict[str, ConsoleTheme] = {
    "netdefense": ConsoleTheme(
        id="netdefense",
        name="Net Defense Ops",
        button_label="NET DEFENSE OPS",
        button_desc="Global backbone · BGP · packet capture",
        window_title="NET-DEFENSE OPS CONSOLE — LIVE",
        header_title="NET-DEFENSE JOINT OPERATIONS CENTER",
        status_live="GLOBAL BACKBONE MONITORING ACTIVE",
        bg="#04080c",
        header_bg="#0a1018",
        panel_fg="#060a0e",
        panel_border="#1a3040",
        accent="#44cc88",
        accent2="#00ffaa",
        title_color="#b0c4d8",
        label_muted="#88bbaa",
        btn_fg="#1a2530",
        btn_hover="#2a4050",
        btn_border="#2a4050",
        terminal_header="#00ffaa",
        terminal_fg="#00dd88",
        terminal_bg="#020608",
        terminal_border="#0a4030",
        tag_colors={"info": "#88aacc", "warn": "#ccaa44", "alert": "#cc6644", "success": "#66aa88"},
        map_arc_colors=["#4488aa", "#55aa88", "#6699bb", "#77bbaa", "#558899"],
        map_scan="#00aa66",
        map_node="#00ffaa",
        map_node_fill="#00ffcc",
        map_label="#aaffdd",
        map_hud="#00dd99",
        map_border="#0a5040",
        inner_bg="#030608",
        session_log_title="SESSION LOG",
        map_title="GLOBAL NETWORK TELEMETRY",
        backbone_title="BACKBONE ROUTING TABLE",
        tunnels_title="ACTIVE TUNNELS",
        video_title="TACTICAL VIDEO FEED",
        ops_title="INTERAGENCY NETWORK OPERATIONS",
        hex_title="LIVE PACKET CAPTURE",
        graph_title="TRAFFIC THROUGHPUT",
        endpoints_title="MONITORED ENDPOINTS",
        sat_title="SAT-COM GROUND STATIONS",
        classification="CLASSIFICATION: UNCLASSIFIED // FOUO",
        stats_prefix="THROUGHPUT",
        graph_line="#55aa88",
        graph_fill="#0a2018",
        progress_color="#337766",
        endpoints=[
            "core-rtr1.dc-east.net", "ixp-lon1.transit.net", "bgp-peer.tyo.backbone.jp",
            "mpls-gw.fra.tier1.de", "sat-uplink.us-west.mil", "mirror-span.sgp.ix",
        ],
        sat_stations=[
            ("Goldstone", "DSN-14", "California"),
            ("Madrid", "DSN-55", "Spain"),
            ("Canberra", "DSN-43", "Australia"),
            ("Weilheim", "GS-01", "Germany"),
        ],
    ),
    "threatwatch": ConsoleTheme(
        id="threatwatch",
        name="Threat Intercept",
        button_label="THREAT INTERCEPT",
        button_desc="Malware · C2 beacons · IOC correlation",
        window_title="THREAT INTERCEPT CONSOLE — LIVE",
        header_title="CYBER THREAT INTERCEPT CENTER",
        status_live="MALWARE ANALYSIS PIPELINE ACTIVE",
        bg="#0c0406",
        header_bg="#18080c",
        panel_fg="#100608",
        panel_border="#402028",
        accent="#ff4455",
        accent2="#ff8866",
        title_color="#e8b0b8",
        label_muted="#bb8899",
        btn_fg="#301820",
        btn_hover="#502030",
        btn_border="#603040",
        terminal_header="#ff5566",
        terminal_fg="#ff9988",
        terminal_bg="#0a0204",
        terminal_border="#501820",
        tag_colors={"info": "#cc8899", "warn": "#ffaa44", "alert": "#ff3344", "success": "#cc6666"},
        map_arc_colors=["#aa4455", "#cc5566", "#994455", "#bb6677", "#883344"],
        map_scan="#aa2233",
        map_node="#ff5566",
        map_node_fill="#ff8899",
        map_label="#ffccd0",
        map_hud="#ff6677",
        map_border="#602030",
        inner_bg="#0a0406",
        session_log_title="INCIDENT STREAM",
        map_title="GLOBAL THREAT ORIGIN MAP",
        backbone_title="C2 INFRASTRUCTURE FEED",
        tunnels_title="EXFIL CHANNELS",
        video_title="SURVEILLANCE FEED",
        ops_title="MALWARE RESEARCH LAB",
        hex_title="SAMPLE HEX DISSECTION",
        graph_title="BEACON FREQUENCY",
        endpoints_title="COMPROMISED HOSTS",
        sat_title="HONEYPOT SENSORS",
        classification="TLP: AMBER — THREAT INTEL ONLY",
        stats_prefix="SAMPLES/HOUR",
        graph_line="#cc4455",
        graph_fill="#200810",
        progress_color="#883344",
        endpoints=[
            "wsus-mirror.evil-cdn.net", "c2-panel.onion.relay", "dropper-stage-04.ru",
            "phish-kit.api.dark", "loader-c2.bullet.host", "stealer-gate.xyz",
        ],
        sat_stations=[
            ("Sinkhole-A", "HK-01", "Amsterdam"),
            ("Darknet-M", "DN-07", "Reykjavik"),
            ("Honeypot-E", "HP-22", "Singapore"),
            ("Sandbox-W", "SB-09", "Virginia"),
        ],
    ),
    "orbital": ConsoleTheme(
        id="orbital",
        name="Orbital Surveillance",
        button_label="ORBITAL SURVEILLANCE",
        button_desc="Satellite passes · TLE · ground links",
        window_title="ORBITAL SURVEILLANCE CONSOLE — LIVE",
        header_title="DEEP SPACE SURVEILLANCE NETWORK",
        status_live="MULTI-SPECTRAL DOWNLINK LOCKED",
        bg="#04060c",
        header_bg="#080c18",
        panel_fg="#060810",
        panel_border="#1a2848",
        accent="#4488ff",
        accent2="#66aaff",
        title_color="#b0c8e8",
        label_muted="#8899cc",
        btn_fg="#182040",
        btn_hover="#283860",
        btn_border="#304878",
        terminal_header="#66aaff",
        terminal_fg="#88bbff",
        terminal_bg="#020408",
        terminal_border="#1a3060",
        tag_colors={"info": "#8899cc", "warn": "#aa88ff", "alert": "#6688ff", "success": "#5599dd"},
        map_arc_colors=["#4466bb", "#5577cc", "#6688dd", "#4477aa", "#5566cc"],
        map_scan="#3366cc",
        map_node="#66aaff",
        map_node_fill="#88ccff",
        map_label="#cce0ff",
        map_hud="#88bbff",
        map_border="#2040a0",
        inner_bg="#030508",
        session_log_title="PASS SCHEDULE LOG",
        map_title="GROUND TRACK PROJECTION",
        backbone_title="ORBITAL ASSET REGISTRY",
        tunnels_title="UPLINK SESSIONS",
        video_title="SENSOR VIDEO FEED",
        ops_title="MISSION OPERATIONS DESK",
        hex_title="TELEMETRY FRAME DUMP",
        graph_title="DOWNLINK SNR",
        endpoints_title="TRACKED OBJECTS",
        sat_title="DEEP SPACE NODES",
        classification="COSMIC TOP SECRET // SCI",
        stats_prefix="DOWNLINK MBPS",
        graph_line="#4488cc",
        graph_fill="#081028",
        progress_color="#3355aa",
        endpoints=[
            "ISS-ZARYA.trk.nasa", "NOAA-21.pass.gsfc", "STARLINK-4821.tle",
            "HST.orbit.stsci", "GPS-III-SV05.nav", "GOES-18.imagery",
        ],
        sat_stations=[
            ("Goldstone", "DSN-14", "California"),
            ("Canberra", "DSN-43", "Australia"),
            ("Madrid", "DSN-55", "Spain"),
            ("Weilheim", "GS-01", "Germany"),
        ],
    ),
    "ledger": ConsoleTheme(
        id="ledger",
        name="Financial Intelligence",
        button_label="FINANCIAL INTEL",
        button_desc="SWIFT · crypto flows · sanctions watch",
        window_title="FINANCIAL INTEL CONSOLE — LIVE",
        header_title="FINANCIAL CRIME ANALYSIS CENTER",
        status_live="TRANSACTION MONITORING ACTIVE",
        bg="#0c0a04",
        header_bg="#141008",
        panel_fg="#100e06",
        panel_border="#403820",
        accent="#ccaa44",
        accent2="#ffcc66",
        title_color="#e8d8b0",
        label_muted="#bbaa77",
        btn_fg="#302818",
        btn_hover="#504830",
        btn_border="#605840",
        terminal_header="#ffcc55",
        terminal_fg="#ddbb66",
        terminal_bg="#0a0804",
        terminal_border="#504020",
        tag_colors={"info": "#bbaa77", "warn": "#ffaa33", "alert": "#cc8844", "success": "#aa9955"},
        map_arc_colors=["#aa8844", "#bb9955", "#ccaa66", "#997733", "#aa7733"],
        map_scan="#aa8822",
        map_node="#ffcc66",
        map_node_fill="#ffdd88",
        map_label="#ffe8bb",
        map_hud="#ddbb66",
        map_border="#806020",
        inner_bg="#0a0804",
        session_log_title="TRANSACTION LOG",
        map_title="IP GEOLOCATION TRACE",
        backbone_title="SWIFT ROUTING TABLE",
        tunnels_title="SETTLEMENT CHANNELS",
        video_title="MARKET SURVEILLANCE",
        ops_title="ASSET RECOVERY DESK",
        hex_title="BLOCKCHAIN TRACE",
        graph_title="VOLUME INDEX",
        endpoints_title="FLAGGED ACCOUNTS",
        sat_title="CORRESPONDENT BANKS",
        classification="BANK SECRECY ACT — RESTRICTED",
        stats_prefix="VOLUME USD",
        graph_line="#ccaa55",
        graph_fill="#201808",
        progress_color="#887733",
        endpoints=[
            "swift-mt103.correspondent.ch", "wallet-mixer.eth.node", "sanctions-ofac.watch",
            "ledger-custody.api", "fx-desk.london.bank", "stablecoin-bridge.io",
        ],
        sat_stations=[
            ("Zurich", "SWF-01", "Switzerland"),
            ("London", "CIT-02", "UK"),
            ("New York", "FED-03", "USA"),
            ("Singapore", "MAS-04", "APAC"),
        ],
    ),
    "gridops": ConsoleTheme(
        id="gridops",
        name="Grid Operations",
        button_label="GRID OPERATIONS",
        button_desc="SCADA · substations · industrial telemetry",
        window_title="GRID OPS CONSOLE — LIVE",
        header_title="CRITICAL INFRASTRUCTURE CONTROL",
        status_live="SCADA TELEMETRY NOMINAL",
        bg="#060804",
        header_bg="#0c1008",
        panel_fg="#080a06",
        panel_border="#304020",
        accent="#88cc44",
        accent2="#aaff66",
        title_color="#c8d8b0",
        label_muted="#99bb77",
        btn_fg="#203018",
        btn_hover="#405030",
        btn_border="#506040",
        terminal_header="#aaff66",
        terminal_fg="#99dd55",
        terminal_bg="#040604",
        terminal_border="#305020",
        tag_colors={"info": "#99bb77", "warn": "#cccc44", "alert": "#ccaa33", "success": "#77aa55"},
        map_arc_colors=["#668844", "#779955", "#88aa55", "#557733", "#669933"],
        map_scan="#66aa22",
        map_node="#aaff66",
        map_node_fill="#ccff88",
        map_label="#ddffbb",
        map_hud="#99dd66",
        map_border="#406030",
        inner_bg="#040604",
        session_log_title="SCADA EVENT LOG",
        map_title="TRANSMISSION GRID MAP",
        backbone_title="SUBSTATION REGISTRY",
        tunnels_title="FIELD BUS LINKS",
        video_title="PLANT CAMERA FEED",
        ops_title="INDUSTRIAL CONTROL DESK",
        hex_title="MODBUS REGISTER DUMP",
        graph_title="LOAD CURVE",
        endpoints_title="RTU ENDPOINTS",
        sat_title="REMOTE SUBSTATIONS",
        classification="NERC CIP — CRITICAL INFRASTRUCTURE",
        stats_prefix="GRID LOAD MW",
        graph_line="#88bb55",
        graph_fill="#102008",
        progress_color="#557733",
        endpoints=[
            "substation-014.scada.grid", "rtu-bay-7.modbus.local", "plc-turbine.wind.farm",
            "breaker-feeder.north.grid", "hmi-control.center.ops", "ied-protection.relay",
        ],
        sat_stations=[
            ("Nevada Solar", "SS-11", "Nevada"),
            ("Wind Ridge", "WR-08", "Texas"),
            ("Hydro Dam", "HD-03", "Washington"),
            ("Nuclear Plant", "NP-01", "Georgia"),
        ],
    ),
}


# Shared netdefense palette for every console (layouts differ; colors do not).
_VISUAL_FIELDS = (
    "bg", "header_bg", "panel_fg", "panel_border", "accent", "accent2",
    "title_color", "label_muted", "btn_fg", "btn_hover", "btn_border",
    "terminal_header", "terminal_fg", "terminal_bg", "terminal_border",
    "tag_colors", "map_arc_colors", "map_scan", "map_node", "map_node_fill",
    "map_label", "map_hud", "map_border", "inner_bg",
    "graph_line", "graph_fill", "progress_color",
)


def _shared_visual() -> dict:
    base = THEMES["netdefense"]
    return {name: getattr(base, name) for name in _VISUAL_FIELDS}


def get_theme(theme_id: str) -> ConsoleTheme:
    if theme_id not in THEMES:
        raise KeyError(f"Unknown console theme: {theme_id}")
    return replace(THEMES[theme_id], **_shared_visual())


def all_themes() -> list[ConsoleTheme]:
    return [get_theme(theme_id) for theme_id in THEMES]

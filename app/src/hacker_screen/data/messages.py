"""Randomized network operations log messages — infrastructure focus."""

import random
from datetime import datetime

TARGETS = [
    "192.168.{a}.{b}",
    "10.{a}.{b}.{c}",
    "172.16.{a}.{b}",
    "{a}.{b}.{c}.{d}",
]

DOMAINS = [
    "dns-root.lan",
    "bgp-peer.net",
    "core-router.gov",
    "sat-uplink.mil",
    "ixp-exchange.net",
    "cdn-edge.cloud",
    "backbone-tier1.net",
    "mpls-gateway.sys",
]

ACTIONS = [
    ("ROUTE", "BGP prefix {target}/24 propagated via {city} IX", "info"),
    ("CAPTURE", "TCP stream reassembled — {n} packets from {target}", "info"),
    ("TUNNEL", "GRE encapsulation active — endpoint {target}", "warn"),
    ("DECRYPT", "TLS 1.3 session key extracted [{hex}]", "success"),
    ("SNIFF", "Mirror port SPAN — {n}KB from {domain}", "info"),
    ("BYPASS", "ACL rule #{n} overridden on {target}", "warn"),
    ("INJECT", "Route injection accepted at {city} peer", "alert"),
    ("HASH", "SHA-256 verified — block {hex}", "success"),
    ("EXFIL", "SFTP transfer {n}MB → {city} relay", "warn"),
    ("PERSIST", "Cron persistence on {target}", "alert"),
    ("TRACE", "Hop {n}/12 — transit via {city}", "info"),
    ("SAT-LINK", "Downlink locked — {city} ground station", "info"),
    ("DNS", "Cache poison attempt on {domain} — mitigated", "warn"),
    ("FIREWALL", "Stateful inspection bypass on port {n}/tcp", "alert"),
    ("MTR", "Latency spike {n}ms — path via {city}", "info"),
]

METHODS = [
    "DNS tunneling",
    "ICMP covert channel",
    "MPLS label swap",
    "CVE-2026-{n} exploit",
    "GRE double-encap",
    "BGP hijack vector",
]

CITY_NAMES = [
    "Tokyo", "London", "Moscow", "New York", "Berlin", "Singapore", "Dubai",
    "Sydney", "São Paulo", "Reykjavik", "Seoul", "Mumbai", "Frankfurt",
]


def _ip() -> str:
    template = random.choice(TARGETS)
    return template.format(
        a=random.randint(1, 254),
        b=random.randint(1, 254),
        c=random.randint(1, 254),
        d=random.randint(1, 254),
    )


def generate_line() -> tuple[str, str]:
    action, template, tag = random.choice(ACTIONS)
    ts = datetime.now().strftime("%H:%M:%S")
    msg = f"{ts} [{action}] " + template.format(
        target=_ip(),
        domain=random.choice(DOMAINS),
        n=random.randint(1, 9999),
        hex="".join(random.choice("0123456789ABCDEF") for _ in range(8)),
        city=random.choice(CITY_NAMES),
        method=random.choice(METHODS).format(n=random.randint(1000, 9999)),
    )
    return msg, tag

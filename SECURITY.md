# Security Policy

## Intended use

Hacker Screen is a **local desktop simulation**. It does not:

- Scan networks or connect to real targets
- Execute exploits or run offensive security tools
- Transmit telemetry or user data to external services

All console activity (logs, maps, transfers, grid events) is **generated locally for display only**.

## Reporting issues

If you discover a security vulnerability in this repository (for example, unsafe deserialization or unexpected network calls), please open a [GitHub Security Advisory](https://github.com/AlanCalhoun/hacker-screen/security/advisories/new) or email the maintainer privately.

Do not open public issues for exploitable vulnerabilities until they are addressed.

## Windows builds

PyInstaller bundles may trigger antivirus heuristics. Build from source when possible, or verify release checksums published by the maintainer.

## Third-party assets

- OpenStreetMap data is used under the [ODbL](https://www.openstreetmap.org/copyright) where noted in the UI.
- Bank names and agency-style labels are fictional or text-only references for simulation — not official logos.

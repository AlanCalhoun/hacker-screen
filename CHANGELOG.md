# Changelog

All notable changes to this project are documented here.

## [1.1.0] - 2026-07-31

### Added

- Five themed ops consoles with distinct layouts: Net Defense, Threat Intercept, Orbital Surveillance, Financial Intel, Grid Operations
- Unified net-defense visual theme across all consoles
- Theme-specific maps and panels (world map, orbital ground track, IP geolocation, SCADA grid schematic)
- Financial Intel: Federal Reserve banner, correspondent banks, live FX rates, FedWire ticker
- Grid Operations: utility logo with cooling towers, blackout monitor, protection relay panel
- Orbital: tracked objects, ground station links, TLE readout
- Windows installer (Inno Setup) and portable onedir build
- Pip wheel build support

### Changed

- Repo reorganized into `app/`, `distributions/`, and `release/`
- Map panels resize correctly at fullscreen
- Performance improvements for animated map layers

## [1.0.0] - Initial release

- Single Net Defense Ops console
- Launcher, session log, world map, backbone panel, ops desk, video feeds

[1.1.0]: https://github.com/AlanCalhoun/hacker-screen/releases/tag/v1.1.0

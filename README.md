# LightFlipper

LightFlipper is an open-source Windows desktop companion for the Flipper Zero.

It aims to provide a clean interface for:
- device connection management
- USB and Bluetooth discovery
- remote control interaction
- file browsing and file management
- future firmware and app workflows

## Project status

The project is in active development. Core foundation work, USB/Bluetooth connectivity, remote control scaffolding, and file management basics are in place and validated with tests.

## Features

- Qt-based desktop shell with sidebar navigation
- SQLite-backed settings persistence
- Customizable accent, background, panel and text colors, font, and sidebar visibility
- Original pixel-art navigation and action icons
- USB serial detection and connection handling
- Bluetooth discovery and connection handling
- Remote-control controls gated behind an active connection
- File Manager entry gated behind a connection; live file transfer is not yet implemented
- Local `.dfu` firmware installation through the official qFlipper CLI over USB

## Getting started

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m lightflipper.app
```

## Windows release build

To generate a deployable Windows executable:

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts/build_release.py
```

This creates a standalone executable at `dist/LightFlipper.exe` and is also used by the GitHub release workflow.

When a version tag like `v0.1.3` is pushed, GitHub Actions builds the EXE, uploads it to the GitHub Release, and generates release notes comparing the tag with the previous release.

For local firmware installation, install qFlipper and select a compatible `.dfu` file in the Firmware page. LightFlipper requires an active USB connection and asks for confirmation before starting qFlipper CLI. Firmware updates have not yet been validated against physical hardware.

## Requirements

- Python 3.12+
- PySide6
- pyserial
- bleak
- pytest

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome. Please keep changes focused, testable, and aligned with the project goals.

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
- USB serial detection and connection handling
- Bluetooth discovery and connection handling
- Remote-control input surface
- File manager browsing and mock-safe filesystem workflows

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

When a version tag like `v0.1.0` is pushed, GitHub Actions builds the EXE automatically and uploads it to the GitHub Release.

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

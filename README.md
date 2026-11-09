# LightFlipper

A professional Windows desktop companion for Flipper Zero.

## Current status

This repository has passed the foundation and USB connectivity phases. A centralized status overview is available in [PROJECT_STATUS.md](PROJECT_STATUS.md).

See the project progress document for completed features, current blockers, and pending work.

## Local development

```bash
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m lightflipper.app
```

## Notes
- The application uses PySide6 / Qt and stores configuration in SQLite.
- Hardware connectivity and real device communication remain future phases.

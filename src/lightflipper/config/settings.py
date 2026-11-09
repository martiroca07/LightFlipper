from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class SettingsManager:
    """Persistent application settings stored in SQLite."""

    DEFAULTS: dict[str, Any] = {
        "window.width": 1280,
        "window.height": 820,
        "window.maximized": False,
        "theme.name": "Default",
        "theme.accent": "#FF7A24",
        "theme.background": "#111214",
        "theme.secondary_background": "#191B1F",
        "theme.panel": "#202329",
        "theme.text": "#F2F2F2",
        "theme.secondary_text": "#9298A2",
        "ui.dark_mode": True,
        "ui.font_family": "Segoe UI",
        "ui.font_size": 12,
        "ui.sidebar_visible": True,
        "device.connection": "disconnected",
        "device.model": "",
        "device.firmware": "",
    }

    def __init__(self, db_path: str | Path | None = None) -> None:
        if db_path is None:
            base = Path.home() / ".lightflipper"
            base.mkdir(parents=True, exist_ok=True)
            db_path = base / "settings.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self._conn.commit()

        for key, default in self.DEFAULTS.items():
            if self.get(key, default=None) is None:
                self.set(key, default)

    def set(self, key: str, value: Any) -> None:
        payload = json.dumps(value)
        self._conn.execute(
            "INSERT INTO settings(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, payload),
        )
        self._conn.commit()

    def get(self, key: str, default: Any = None) -> Any:
        row = self._conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        if row is None:
            return default

        value = json.loads(row["value"])
        return value

    def delete(self, key: str) -> None:
        self._conn.execute("DELETE FROM settings WHERE key = ?", (key,))
        self._conn.commit()

    def reset(self) -> None:
        self._conn.execute("DELETE FROM settings")
        for key, value in self.DEFAULTS.items():
            self.set(key, value)

    def close(self) -> None:
        self._conn.close()

    def __del__(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass

import sqlite3
from pathlib import Path

from lightflipper.config.settings import SettingsManager
from lightflipper.theme import ThemeManager, ThemePalette


def test_theme_palette_defaults():
    palette = ThemePalette()

    assert palette.accent == "#FF7A24"
    assert palette.background == "#111214"
    assert palette.secondary_background == "#191B1F"
    assert palette.text == "#F2F2F2"


def test_theme_manager_create_and_apply():
    manager = ThemeManager()
    theme = manager.create_theme("Custom", accent="#123456")

    assert theme.name == "Custom"
    assert theme.accent == "#123456"
    assert theme.is_dark is True
    assert manager.apply_theme(theme) is True


def test_settings_manager_persists_values(tmp_path):
    db_path = tmp_path / "settings.db"
    manager = SettingsManager(db_path)

    manager.set("window.width", 1400)
    manager.set("theme.name", "Midnight")
    manager.set("ui.accent", "#FF7A24")

    assert manager.get("window.width") == 1400
    assert manager.get("theme.name") == "Midnight"
    assert manager.get("ui.accent") == "#FF7A24"

    reload = SettingsManager(db_path)
    assert reload.get("window.width") == 1400
    assert reload.get("theme.name") == "Midnight"
    assert reload.get("ui.accent") == "#FF7A24"

    assert isinstance(manager.db_path, Path)
    assert manager.db_path == db_path
    assert sqlite3.connect(db_path).execute("SELECT 1").fetchone() == (1,)


def test_settings_manager_has_visual_customization_defaults(tmp_path):
    settings = SettingsManager(tmp_path / "visual-settings.db")

    assert settings.get("theme.accent") == "#FF7A24"
    assert settings.get("theme.background") == "#111214"
    assert settings.get("ui.font_size") == 12
    assert settings.get("ui.sidebar_visible") is True

    settings.close()

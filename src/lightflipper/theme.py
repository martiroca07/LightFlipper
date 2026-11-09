from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ThemePalette:
    """Theme palette used by the LightFlipper interface."""

    name: str = "Default"
    accent: str = "#FF7A24"
    background: str = "#111214"
    secondary_background: str = "#191B1F"
    panel: str = "#202329"
    text: str = "#F2F2F2"
    secondary_text: str = "#9298A2"
    border: str = "#2F343B"
    button: str = "#FF7A24"
    icon: str = "#F2F2F2"
    is_dark: bool = True
    font_family: str = "Segoe UI"
    font_size: int = 12
    border_radius: int = 12
    window_opacity: float = 1.0
    sidebar_visible: bool = True
    spacing: int = 12
    animation_speed: int = 180


class ThemeManager:
    """Manage available themes and the active theme state."""

    def __init__(self) -> None:
        self.themes: list[ThemePalette] = []
        self.current: ThemePalette | None = None
        self._bootstrap_default_themes()

    def _bootstrap_default_themes(self) -> None:
        default = ThemePalette(name="Default")
        dark = ThemePalette(name="Midnight", accent="#FF8A3D", background="#0F1114")
        light = ThemePalette(name="Light", is_dark=False, background="#F3F4F6", secondary_background="#E7E9EE", panel="#FFFFFF", text="#111214", secondary_text="#5D6772", border="#D7DCE3", button="#FF7A24", icon="#111214")

        self.themes = [default, dark, light]
        self.current = default

    def create_theme(self, name: str, **overrides: Any) -> ThemePalette:
        theme = ThemePalette(name=name)
        for key, value in overrides.items():
            if hasattr(theme, key):
                setattr(theme, key, value)
        self.themes.append(theme)
        return theme

    def apply_theme(self, theme: ThemePalette) -> bool:
        if theme not in self.themes:
            self.themes.append(theme)
        self.current = theme
        return True

    def get_theme(self, name: str) -> ThemePalette | None:
        for theme in self.themes:
            if theme.name == name:
                return theme
        return None

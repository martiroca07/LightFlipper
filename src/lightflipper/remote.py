from __future__ import annotations

from enum import Enum


class RemoteButton(str, Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    OK = "ok"
    BACK = "back"


class RemoteController:
    """Track user input and screen synchronization for the remote-control surface."""

    _BUTTONS = tuple(RemoteButton)

    def __init__(self) -> None:
        self._pressed: set[RemoteButton] = set()
        self.screen_buffer: str = ""
        self.screen_sync_enabled = True
        self.last_error: str | None = None

    @classmethod
    def normalize_button(cls, button: str | RemoteButton) -> RemoteButton | None:
        if isinstance(button, RemoteButton):
            return button
        if isinstance(button, str):
            value = button.strip().lower()
            for candidate in cls._BUTTONS:
                if candidate.value == value:
                    return candidate
        return None

    def press_button(self, button: str | RemoteButton) -> bool:
        normalized = self.normalize_button(button)
        if normalized is None:
            self.last_error = f"Unsupported remote button: {button!r}"
            return False
        self._pressed.add(normalized)
        self.last_error = None
        return True

    def release_button(self, button: str | RemoteButton) -> bool:
        normalized = self.normalize_button(button)
        if normalized is None:
            self.last_error = f"Unsupported remote button: {button!r}"
            return False
        self._pressed.discard(normalized)
        self.last_error = None
        return True

    def is_pressed(self, button: str | RemoteButton) -> bool:
        normalized = self.normalize_button(button)
        if normalized is None:
            return False
        return normalized in self._pressed

    def get_pressed_buttons(self) -> list[RemoteButton]:
        return [button for button in self._BUTTONS if button in self._pressed]

    def set_screen_buffer(self, screen_data: str) -> None:
        self.screen_buffer = screen_data
        self.screen_sync_enabled = True
        self.last_error = None

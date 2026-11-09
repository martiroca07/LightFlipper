from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass
class FlipperFileEntry:
    name: str
    path: str
    parent_path: str
    size: int = 0
    extension: str = ""
    is_directory: bool = False
    content: bytes = b""


class FlipperFileManager:
    """Manage a mock-safe view of the Flipper filesystem for browsing and transfers."""

    DEFAULT_DIRECTORIES = (
        "nfc",
        "subghz",
        "infrared",
        "rfid",
        "ibutton",
        "apps",
        "system",
    )

    def __init__(self) -> None:
        self._entries: dict[str, FlipperFileEntry] = {}
        self._seed_default_directories()

    def _seed_default_directories(self) -> None:
        for directory in self.DEFAULT_DIRECTORIES:
            self.create_directory(directory, "/")

    @staticmethod
    def _normalize_path(path: str | None) -> str:
        if path is None:
            return "/"
        cleaned = str(path).replace("\\", "/").strip()
        if not cleaned:
            return "/"
        if cleaned == ".":
            return "/"
        if not cleaned.startswith("/"):
            cleaned = "/" + cleaned
        if cleaned != "/":
            cleaned = cleaned.rstrip("/") or "/"
        return cleaned

    def _join_path(self, parent: str, name: str) -> str:
        clean_name = name.strip().strip("/")
        if not clean_name:
            return "/"
        if parent == "/":
            return f"/{clean_name}"
        return f"{parent.rstrip('/')}/{clean_name}"

    def _parent_path(self, path: str) -> str:
        normalized = self._normalize_path(path)
        if normalized == "/":
            return "/"
        parent = str(PurePosixPath(normalized).parent)
        return parent if parent else "/"

    def _ensure_directory_exists(self, path: str) -> bool:
        normalized = self._normalize_path(path)
        if normalized == "/":
            return True
        if normalized in self._entries and self._entries[normalized].is_directory:
            return True

        parent_path = self._parent_path(normalized)
        if parent_path != "/" and parent_path not in self._entries:
            self._ensure_directory_exists(parent_path)

        entry = FlipperFileEntry(
            name=PurePosixPath(normalized).name,
            path=normalized,
            parent_path=parent_path,
            is_directory=True,
            size=0,
        )
        self._entries[normalized] = entry
        return True

    def list_directory(self, path: str) -> list[FlipperFileEntry]:
        normalized = self._normalize_path(path)
        if normalized != "/" and normalized not in self._entries:
            return []

        entries = [
            entry for entry in self._entries.values() if entry.parent_path == normalized
        ]
        return sorted(entries, key=lambda item: (0 if item.is_directory else 1, item.name.lower()))

    def create_directory(self, name: str, parent: str) -> bool:
        cleaned = (name or "").strip()
        if not cleaned:
            return False
        parent_path = self._normalize_path(parent)
        if not self._ensure_directory_exists(parent_path):
            return False

        new_path = self._join_path(parent_path, cleaned)
        if new_path in self._entries:
            return True

        self._entries[new_path] = FlipperFileEntry(
            name=cleaned,
            path=new_path,
            parent_path=parent_path,
            is_directory=True,
            size=0,
        )
        return True

    def upload_file(self, path: str, data: bytes | str) -> bool:
        normalized = self._normalize_path(path)
        if normalized == "/":
            return False

        parent_path = self._parent_path(normalized)
        if not self._ensure_directory_exists(parent_path):
            return False

        file_name = PurePosixPath(normalized).name
        if not file_name:
            return False

        payload = data if isinstance(data, bytes) else str(data).encode("utf-8")
        entry = FlipperFileEntry(
            name=file_name,
            path=normalized,
            parent_path=parent_path,
            size=len(payload),
            extension=file_name.rsplit(".", 1)[1].lower() if "." in file_name else "",
            content=payload,
        )
        self._entries[normalized] = entry
        return True

    def get_file(self, path: str) -> FlipperFileEntry | None:
        normalized = self._normalize_path(path)
        entry = self._entries.get(normalized)
        if entry is None or entry.is_directory:
            return None
        return entry

    def read_file(self, path: str) -> bytes | None:
        entry = self.get_file(path)
        if entry is None:
            return None
        return entry.content

    def rename_file(self, path: str, new_name: str) -> bool:
        existing = self.get_file(path)
        if existing is None:
            return False
        cleaned = (new_name or "").strip()
        if not cleaned or "/" in cleaned:
            return False

        new_path = self._join_path(existing.parent_path, cleaned)
        if new_path in self._entries:
            return False

        del self._entries[existing.path]
        existing.name = cleaned
        existing.path = new_path
        existing.extension = cleaned.rsplit(".", 1)[1].lower() if "." in cleaned else ""
        self._entries[new_path] = existing
        return True

    def delete_file(self, path: str) -> bool:
        normalized = self._normalize_path(path)
        entry = self._entries.get(normalized)
        if entry is None:
            return False

        del self._entries[normalized]
        if entry.is_directory:
            for item_path in list(self._entries):
                if item_path.startswith(f"{normalized}/"):
                    del self._entries[item_path]
        return True

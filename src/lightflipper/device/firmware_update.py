from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Iterable


class FirmwareUpdateService:
    """Validate local DFU packages and prepare qFlipper CLI commands."""

    WRONG_FORMAT = "Choose a qFlipper-compatible .dfu file."
    MISSING_FILE = "The selected firmware file does not exist."
    EMPTY_FILE = "The selected firmware file is empty."

    @staticmethod
    def validate_dfu(file_path: str | Path) -> str | None:
        path = Path(file_path)
        if path.suffix.lower() != ".dfu":
            return FirmwareUpdateService.WRONG_FORMAT
        if not path.is_file():
            return FirmwareUpdateService.MISSING_FILE
        if path.stat().st_size == 0:
            return FirmwareUpdateService.EMPTY_FILE
        return None

    @staticmethod
    def find_qflipper_cli(candidates: Iterable[str | Path] | None = None) -> Path | None:
        if candidates is None:
            candidates = []
            executable = shutil.which("qFlipper-cli") or shutil.which("qFlipper-cli.exe")
            if executable:
                candidates = [executable]
            else:
                install_roots = (
                    os.environ.get("ProgramFiles"),
                    os.environ.get("ProgramFiles(x86)"),
                    os.environ.get("LOCALAPPDATA"),
                )
                candidates = [
                    Path(root) / "qFlipper" / "qFlipper-cli.exe"
                    for root in install_roots
                    if root
                ]

        for candidate in candidates:
            path = Path(candidate)
            if path.is_file():
                return path
        return None

    @staticmethod
    def build_install_command(cli_path: str | Path, firmware_path: str | Path) -> list[str]:
        return [str(Path(cli_path)), "firmware", str(Path(firmware_path))]

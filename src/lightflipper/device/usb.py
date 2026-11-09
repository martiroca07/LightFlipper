from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from lightflipper.device.rpc import FlipperRPCClient

try:
    import serial
    from serial.tools import list_ports
except ImportError:  # pragma: no cover - dependency is installed in project environment
    serial = None
    list_ports = None


_FLIPPER_VIDS = {0x0483}
_FLIPPER_PIDS = {0x5740, 0x5741, 0x5742, 0x5743}
_VALID_MOCK_PORTS = {"COM3", "COM4", "COM5", "COM7", "COM8", "COM9"}


@dataclass
class USBPortInfo:
    port_name: str
    description: str
    device: str = ""
    vid: int | None = None
    pid: int | None = None
    manufacturer: str = ""
    serial_number: str = ""
    is_flipper_candidate: bool = False
    is_mock: bool = False


class USBDeviceDetector:
    """Identify USB serial ports that look like Flipper Zero devices."""

    def detect_ports(self, ports: Sequence[object] | None = None) -> list[USBPortInfo]:
        candidates = ports if ports is not None else self._enumerate_system_ports()
        findings: list[USBPortInfo] = []

        for port in candidates:
            info = self._normalize_port(port)
            if info is None:
                continue
            if info.is_flipper_candidate:
                findings.append(info)

        return findings

    def _enumerate_system_ports(self) -> list[object]:
        if list_ports is None:
            return []
        try:
            return list(list_ports.comports())
        except Exception:
            return []

    def _normalize_port(self, port: object) -> USBPortInfo | None:
        name = getattr(port, "name", getattr(port, "device", ""))
        if not name:
            return None

        description = getattr(port, "description", "")
        hwid = getattr(port, "hwid", "")
        manufacturer = getattr(port, "manufacturer", "")
        vid = getattr(port, "vid", None)
        pid = getattr(port, "pid", None)
        serial_number = getattr(port, "serial_number", "")

        if vid is None and hwid:
            try:
                vid = int(hwid.split("VID_")[1][:4], 16)
            except (IndexError, ValueError, TypeError):
                vid = None

        if pid is None and hwid:
            try:
                pid = int(hwid.split("PID_")[1][:4], 16)
            except (IndexError, ValueError, TypeError):
                pid = None

        candidate = (
            ((vid in _FLIPPER_VIDS) and (pid in _FLIPPER_PIDS))
            or "flipper" in (description.lower() + manufacturer.lower() + hwid.lower())
            or "flipper" in name.lower()
        )

        info = USBPortInfo(
            port_name=str(name),
            description=str(description or name),
            device=str(getattr(port, "device", name)),
            vid=vid,
            pid=pid,
            manufacturer=str(manufacturer),
            serial_number=str(serial_number),
            is_flipper_candidate=candidate,
            is_mock=False,
        )
        return info


class USBConnectionManager:
    """Manage a USB serial connection to the Flipper Zero and gracefully degrade in tests."""

    def __init__(self) -> None:
        self.port_name: str | None = None
        self.is_connected = False
        self.connection_type = "disconnected"
        self.last_error: str | None = None
        self._serial_handle: object | None = None

    def connect(self, port_name: str, mock_mode: bool = False) -> bool:
        cleaned = (port_name or "").strip()
        if not cleaned:
            self.last_error = "USB port name is empty."
            return False

        if mock_mode:
            if cleaned.upper() not in _VALID_MOCK_PORTS:
                self.last_error = f"Mock USB connection rejected for {cleaned}."
                return False
            self.port_name = cleaned
            self.is_connected = True
            self.connection_type = "usb"
            self.last_error = None
            return True

        if serial is None:
            self.last_error = "pyserial is not installed."
            return False

        try:
            handle = serial.Serial(cleaned, 115200, timeout=1)
        except Exception as exc:  # pragma: no cover - platform dependent
            self.last_error = f"Could not open USB port {cleaned}: {exc}"
            return False

        self._serial_handle = handle
        self.port_name = cleaned
        self.is_connected = True
        self.connection_type = "usb"
        self.last_error = None
        return True

    def disconnect(self) -> None:
        if self._serial_handle is not None and hasattr(self._serial_handle, "close"):
            try:
                self._serial_handle.close()
            except Exception:
                pass
        self._serial_handle = None
        self.port_name = None
        self.is_connected = False
        self.connection_type = "disconnected"
        self.last_error = None

    def send_rpc(self, command: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.is_connected:
            return {"status": "error", "error": "USB connection is not active."}
        return FlipperRPCClient().send_command(command, payload)

    def get_device_info(self) -> dict[str, str]:
        if not self.is_connected:
            return {"model": "unavailable", "firmware": "unavailable", "connection_type": self.connection_type}
        return {
            "model": "Flipper Zero",
            "firmware": "unknown",
            "connection_type": "usb",
            "port": self.port_name or "unknown",
        }

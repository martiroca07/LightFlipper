from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from lightflipper.device.rpc import FlipperRPCClient

try:
    from bleak import BleakScanner, BleakClient
except ImportError:  # pragma: no cover - dependency is installed in project environment
    BleakScanner = None
    BleakClient = None


_VALID_MOCK_ADDRESSES = {
    "AA:BB:CC:DD:EE:02",
    "AA:BB:CC:DD:EE:03",
    "AA:BB:CC:DD:EE:04",
}


@dataclass
class BluetoothDeviceInfo:
    name: str
    address: str
    rssi: int
    is_flipper_candidate: bool = False
    is_paired: bool = False
    is_mock: bool = False


class BluetoothConnectionManager:
    """Manage BLE discovery and connections for Flipper Zero devices."""

    def __init__(self) -> None:
        self.device_address: str | None = None
        self.device_name: str | None = None
        self.is_connected = False
        self.connection_type = "disconnected"
        self.last_error: str | None = None
        self._client: object | None = None

    def filter_devices(self, devices: Sequence[BluetoothDeviceInfo]) -> list[BluetoothDeviceInfo]:
        return [device for device in devices if device.is_flipper_candidate]

    def connect(self, address: str, mock_mode: bool = False) -> bool:
        cleaned = (address or "").strip()
        if not cleaned:
            self.last_error = "Bluetooth address is empty."
            return False

        if mock_mode:
            if cleaned.upper() not in {item.upper() for item in _VALID_MOCK_ADDRESSES}:
                self.last_error = f"Mock Bluetooth connection rejected for {cleaned}."
                return False
            self.device_address = cleaned.upper()
            self.device_name = "Flipper Zero"
            self.is_connected = True
            self.connection_type = "bluetooth"
            self.last_error = None
            return True

        if BleakClient is None:
            self.last_error = "bleak is not installed."
            return False

        try:
            self._client = BleakClient(cleaned)
            self.device_address = cleaned.upper()
            self.device_name = "Flipper Zero"
            self.is_connected = True
            self.connection_type = "bluetooth"
            self.last_error = None
            return True
        except Exception as exc:  # pragma: no cover - platform dependent
            self.last_error = f"Could not connect to Bluetooth device {cleaned}: {exc}"
            return False

    def disconnect(self) -> None:
        if self._client is not None and hasattr(self._client, "disconnect"):
            try:
                self._client.disconnect()
            except Exception:
                pass
        self._client = None
        self.device_address = None
        self.device_name = None
        self.is_connected = False
        self.connection_type = "disconnected"
        self.last_error = None

    def send_rpc(self, command: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.is_connected:
            return {"status": "error", "error": "Bluetooth connection is not active."}
        return FlipperRPCClient().send_command(command, payload)

    def get_device_info(self) -> dict[str, str]:
        if not self.is_connected:
            return {"model": "unavailable", "firmware": "unavailable", "connection_type": self.connection_type}
        return {
            "model": "Flipper Zero",
            "firmware": "unknown",
            "connection_type": "bluetooth",
            "address": self.device_address or "unknown",
        }

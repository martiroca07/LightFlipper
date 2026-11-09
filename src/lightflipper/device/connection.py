from __future__ import annotations

from typing import Any

from lightflipper.device.bluetooth import BluetoothConnectionManager
from lightflipper.device.usb import USBConnectionManager


class DeviceConnectionManager:
    """Coordinate USB and Bluetooth device connections for the desktop shell."""

    def __init__(self) -> None:
        self.usb_manager = USBConnectionManager()
        self.bluetooth_manager = BluetoothConnectionManager()
        self.active_transport: str | None = None
        self.is_connected = False
        self.connection_type = "disconnected"
        self.last_error: str | None = None

    def connect_usb(self, port_name: str, mock_mode: bool = False) -> bool:
        if not self.usb_manager.connect(port_name, mock_mode=mock_mode):
            self.last_error = self.usb_manager.last_error
            self.active_transport = None
            self.is_connected = False
            self.connection_type = "disconnected"
            return False

        self.bluetooth_manager.disconnect()
        self.active_transport = "usb"
        self.is_connected = True
        self.connection_type = "usb"
        self.last_error = None
        return True

    def connect_bluetooth(self, address: str, mock_mode: bool = False) -> bool:
        if not self.bluetooth_manager.connect(address, mock_mode=mock_mode):
            self.last_error = self.bluetooth_manager.last_error
            self.active_transport = None
            self.is_connected = False
            self.connection_type = "disconnected"
            return False

        self.usb_manager.disconnect()
        self.active_transport = "bluetooth"
        self.is_connected = True
        self.connection_type = "bluetooth"
        self.last_error = None
        return True

    def disconnect(self) -> None:
        self.usb_manager.disconnect()
        self.bluetooth_manager.disconnect()
        self.active_transport = None
        self.is_connected = False
        self.connection_type = "disconnected"
        self.last_error = None

    def get_device_summary(self) -> dict[str, Any]:
        if self.active_transport == "usb":
            info = self.usb_manager.get_device_info()
        elif self.active_transport == "bluetooth":
            info = self.bluetooth_manager.get_device_info()
        else:
            return {
                "model": "None",
                "firmware": "unavailable",
                "connection_type": "disconnected",
            }

        return {
            "model": info.get("model", "Flipper Zero"),
            "firmware": info.get("firmware", "unknown"),
            "connection_type": self.connection_type,
            "port": info.get("port", info.get("address", "unknown")),
            "last_error": self.last_error,
        }

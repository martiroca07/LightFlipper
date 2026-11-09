from lightflipper.device.connection import DeviceConnectionManager


def test_device_connection_manager_tracks_summary_and_state():
    manager = DeviceConnectionManager()

    assert manager.connect_usb("COM7", mock_mode=True) is True
    assert manager.is_connected is True
    assert manager.connection_type == "usb"
    assert manager.get_device_summary()["connection_type"] == "usb"

    manager.disconnect()
    assert manager.is_connected is False
    assert manager.connection_type == "disconnected"


def test_device_connection_manager_supports_bluetooth_mock_connect():
    manager = DeviceConnectionManager()

    assert manager.connect_bluetooth("AA:BB:CC:DD:EE:02", mock_mode=True) is True
    assert manager.connection_type == "bluetooth"
    assert manager.get_device_summary()["model"] == "Flipper Zero"

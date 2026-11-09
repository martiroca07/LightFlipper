from lightflipper.device.bluetooth import BluetoothConnectionManager, BluetoothDeviceInfo


def test_bluetooth_detector_filters_flipper_devices():
    manager = BluetoothConnectionManager()
    devices = [
        BluetoothDeviceInfo(name="Laptop", address="AA:BB:CC:DD:EE:01", rssi=-48, is_flipper_candidate=False),
        BluetoothDeviceInfo(name="Flipper Zero", address="AA:BB:CC:DD:EE:02", rssi=-55, is_flipper_candidate=True),
        BluetoothDeviceInfo(name="Another Device", address="AA:BB:CC:DD:EE:03", rssi=-60, is_flipper_candidate=False),
    ]

    filtered = manager.filter_devices(devices)
    assert [item.address for item in filtered] == ["AA:BB:CC:DD:EE:02"]


def test_bluetooth_connection_manager_connects_and_tracks_state():
    manager = BluetoothConnectionManager()

    assert manager.connect("AA:BB:CC:DD:EE:02", mock_mode=True) is True
    assert manager.is_connected is True
    assert manager.connection_type == "bluetooth"
    assert manager.device_address == "AA:BB:CC:DD:EE:02"

    manager.disconnect()
    assert manager.is_connected is False
    assert manager.device_address is None


def test_bluetooth_connection_manager_rejects_unknown_address():
    manager = BluetoothConnectionManager()

    assert manager.connect("AA:BB:CC:DD:EE:99", mock_mode=True) is False
    assert manager.last_error is not None

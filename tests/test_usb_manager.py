from types import SimpleNamespace

from lightflipper.device.usb import USBConnectionManager, USBDeviceDetector


def _port(name: str, vid: int | None = None, pid: int | None = None, product: str = "") -> SimpleNamespace:
    return SimpleNamespace(
        device=name,
        name=name,
        description=product or f"Serial port {name}",
        hwid=f"USB\\VID_{vid:04X}&PID_{pid:04X}" if vid is not None and pid is not None else "",
        vid=vid,
        pid=pid,
        serial_number="",
    )


def test_usb_detector_identifies_flipper_ports():
    detector = USBDeviceDetector()
    ports = [
        _port("COM3", 0x0483, 0x5740, "Flipper Zero"),
        _port("COM4", 0x8086, 0x9a0d, "Intel Serial"),
        _port("COM5", 0x0483, 0x5741, "Flipper Zero Debug"),
    ]

    detected = detector.detect_ports(ports)

    assert [item.port_name for item in detected] == ["COM3", "COM5"]
    assert all(item.is_flipper_candidate for item in detected)


def test_usb_connection_manager_connects_and_tracks_state():
    manager = USBConnectionManager()
    port = "COM7"

    assert manager.connect(port, mock_mode=True) is True
    assert manager.is_connected is True
    assert manager.connection_type == "usb"
    assert manager.port_name == port

    manager.disconnect()
    assert manager.is_connected is False
    assert manager.port_name is None


def test_usb_connection_manager_rejects_invalid_port():
    manager = USBConnectionManager()

    assert manager.connect("COM999", mock_mode=True) is False
    assert manager.last_error is not None

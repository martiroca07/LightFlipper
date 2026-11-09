from lightflipper.device.rpc import FlipperRPCClient
from lightflipper.device.usb import USBConnectionManager


def test_rpc_client_builds_and_validates_requests():
    client = FlipperRPCClient()

    response = client.send_command("system.device_info", {"request": "status"})

    assert response["status"] == "ok"
    assert response["command"] == "system.device_info"
    assert response["payload"]["request"] == "status"


def test_usb_manager_can_send_mock_rpc_commands():
    manager = USBConnectionManager()

    assert manager.connect("COM7", mock_mode=True) is True
    response = manager.send_rpc("system.device_info", {"request": "status"})

    assert response["status"] == "ok"
    assert response["command"] == "system.device_info"
    assert manager.is_connected is True


def test_rpc_client_rejects_invalid_command_names():
    client = FlipperRPCClient()

    response = client.send_command("", {"request": "status"})

    assert response["status"] == "error"
    assert "command" in response["error"].lower()

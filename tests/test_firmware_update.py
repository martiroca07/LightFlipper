import os
from pathlib import Path

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QApplication

from lightflipper.device.connection import DeviceConnectionManager
from lightflipper.device.firmware_update import FirmwareUpdateService
from lightflipper.ui.main_window import FirmwarePage


def test_firmware_update_accepts_nonempty_dfu_file(tmp_path):
    firmware = tmp_path / "release.dfu"
    firmware.write_bytes(b"valid-looking DFU package")

    service = FirmwareUpdateService()

    assert service.validate_dfu(firmware) is None


def test_firmware_update_rejects_wrong_extension_and_missing_file(tmp_path):
    service = FirmwareUpdateService()

    wrong_extension = tmp_path / "firmware.tgz"
    wrong_extension.write_bytes(b"data")
    assert service.validate_dfu(wrong_extension) == "Choose a qFlipper-compatible .dfu file."
    assert service.validate_dfu(tmp_path / "missing.dfu") == "The selected firmware file does not exist."


def test_firmware_update_finds_cli_and_builds_official_command(tmp_path):
    cli = tmp_path / "qFlipper-cli.exe"
    cli.write_bytes(b"cli")
    firmware = tmp_path / "release.dfu"
    firmware.write_bytes(b"valid-looking DFU package")

    service = FirmwareUpdateService()

    assert service.find_qflipper_cli([cli]) == cli
    assert service.build_install_command(cli, firmware) == [
        str(cli),
        "firmware",
        str(firmware),
    ]


def test_firmware_page_requires_valid_dfu_and_usb(tmp_path):
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance() or QApplication([])
    manager = DeviceConnectionManager()
    page = FirmwarePage(manager, qflipper_cli="qFlipper-cli.exe")
    firmware = tmp_path / "release.dfu"
    firmware.write_bytes(b"valid-looking DFU package")
    page.file_path.setText(str(firmware))

    assert not page.install_button.isEnabled()
    page._confirm_install()
    assert page.process.state() == QProcess.ProcessState.NotRunning

    manager.connect_bluetooth("AA:BB:CC:DD:EE:02", mock_mode=True)
    page._refresh_state()
    assert not page.install_button.isEnabled()
    page._confirm_install()
    assert page.process.state() == QProcess.ProcessState.NotRunning

    manager.disconnect()
    manager.connect_usb("COM7", mock_mode=True)
    page._refresh_state()
    assert page.install_button.isEnabled()

    page.file_path.setText(str(tmp_path / "release.tgz"))
    assert not page.install_button.isEnabled()

    page.close()
    app.quit()
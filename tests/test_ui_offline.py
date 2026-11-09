import os

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from lightflipper.config.settings import SettingsManager
from lightflipper.ui.main_window import (
    MainWindow,
    RemoteControlPage,
    SettingsPage,
    ensure_system_fonts,
)


def get_application() -> QApplication:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance()
    return app if app is not None else QApplication([])


class EmptyUSBDetector:
    def detect_ports(self):
        return []


def test_remote_button_is_cleared_after_release(tmp_path):
    app = get_application()
    settings = SettingsManager(tmp_path / "remote-settings.sqlite")
    window = MainWindow(settings=settings)
    window.connection_manager.connect_usb("COM7", mock_mode=True)
    window._sync_connection_ui()
    window.show_page("Remote Control")
    page = window.page_stack.currentWidget()
    window.show()
    app.processEvents()

    ok_button = next(
        button for button in page.findChildren(QPushButton) if button.text() == "OK"
    )
    assert page.screen_label.text() == "No live device screen"
    assert page.status_label.text() == "Offline preview"
    assert "QPushButton:pressed" in ok_button.styleSheet()
    assert "background: #FF7A24" in ok_button.styleSheet()

    QTest.mousePress(ok_button, Qt.MouseButton.LeftButton)
    app.processEvents()
    assert ok_button.isDown()
    assert page.status_label.text() == "Preview: Ok"

    QTest.mouseRelease(ok_button, Qt.MouseButton.LeftButton)
    app.processEvents()
    assert not ok_button.isDown()
    assert page.status_label.text() == "Offline preview"

    window.close()
    settings.close()


def test_settings_does_not_offer_mock_connection_without_device():
    get_application()
    page = SettingsPage(usb_detector=EmptyUSBDetector())

    buttons = page.findChildren(QPushButton)
    assert not any("mock" in button.text().lower() for button in buttons)
    assert not page.connect_usb_button.isEnabled()
    assert page.connection_status.text() == "No Flipper USB device found"

    page.close()


def test_settings_page_persists_visual_customization(tmp_path):
    app = get_application()
    settings = SettingsManager(tmp_path / "customization.sqlite")
    page = SettingsPage(settings=settings, usb_detector=EmptyUSBDetector())
    page.show()
    app.processEvents()

    page.set_color("theme.accent", "#27A99A")
    page.font_size_spin.setValue(16)
    page.sidebar_toggle.setChecked(False)

    assert settings.get("theme.accent") == "#27A99A"
    assert settings.get("ui.font_size") == 16
    assert settings.get("ui.sidebar_visible") is False

    page.close()
    settings.close()


def test_main_window_marks_unavailable_pages_and_sample_files(tmp_path):
    app = get_application()
    settings = SettingsManager(tmp_path / "settings.sqlite")
    window = MainWindow(settings=settings)
    window.show()
    app.processEvents()

    assert window.status_panel.status_label.text() == "Disconnected"
    assert not window.nav_map["NFC"].isEnabled()
    assert window.nav_map["NFC"].toolTip() == "Not available yet"
    assert not window.nav_map["File Manager"].isEnabled()
    assert "Connect a Flipper" in window.nav_map["File Manager"].toolTip()
    assert not window.nav_map["Remote Control"].isEnabled()

    current_page = window.page_stack.currentIndex()
    window.show_page("File Manager")
    assert window.page_stack.currentIndex() == current_page

    window.connection_manager.connect_usb("COM7", mock_mode=True)
    window._sync_connection_ui()
    assert window.nav_map["Remote Control"].isEnabled()
    QTest.mouseClick(window.nav_map["Remote Control"], Qt.MouseButton.LeftButton)
    assert window.nav_map["Remote Control"].isChecked()
    assert not window.nav_map["Dashboard"].isChecked()

    QTest.mouseClick(window.nav_map["Dashboard"], Qt.MouseButton.LeftButton)
    assert window.nav_map["Dashboard"].isChecked()
    assert not window.nav_map["Remote Control"].isChecked()

    assert window.nav_map["File Manager"].isEnabled()
    QTest.mouseClick(window.nav_map["File Manager"], Qt.MouseButton.LeftButton)
    assert window.page_stack.currentIndex() == 2

    window.connection_manager.disconnect()
    window._sync_connection_ui()
    assert not window.nav_map["File Manager"].isEnabled()
    assert window.page_stack.currentIndex() == 0

    window.close()
    settings.close()


def test_sidebar_visibility_can_be_customized(tmp_path):
    app = get_application()
    settings = SettingsManager(tmp_path / "background.sqlite")
    window = MainWindow(settings=settings)
    window.show()
    app.processEvents()

    assert window.sidebar_widget.isVisible()
    window.settings_page.sidebar_toggle.setChecked(False)
    app.processEvents()
    assert not window.sidebar_widget.isVisible()
    assert settings.get("ui.sidebar_visible") is False

    window.settings_page.sidebar_toggle.setChecked(True)
    app.processEvents()
    assert window.sidebar_widget.isVisible()

    window.close()
    settings.close()


def test_navigation_and_device_actions_have_pixel_icons(tmp_path):
    app = get_application()
    settings = SettingsManager(tmp_path / "pixel-icons.sqlite")
    window = MainWindow(settings=settings)
    window.show()
    app.processEvents()

    for button in window.nav_map.values():
        assert not button.icon().isNull()
        assert button.iconSize().width() == 16
        assert button.iconSize().height() == 16

    for button in (
        window.settings_page.scan_usb_button,
        window.settings_page.connect_usb_button,
        window.settings_page.disconnect_button,
        window.firmware_page.browse_button,
        window.firmware_page.install_button,
    ):
        assert not button.icon().isNull()

    window.close()
    settings.close()


def test_main_window_restores_and_applies_custom_palette(tmp_path):
    app = get_application()
    settings = SettingsManager(tmp_path / "palette.sqlite")
    settings.set("theme.accent", "#27A99A")
    settings.set("theme.background", "#101820")
    window = MainWindow(settings=settings)
    window.show()
    app.processEvents()

    assert "#101820" in window.content_widget.styleSheet()
    assert "#27A99A" in window.nav_map["Dashboard"].styleSheet()

    window.settings_page.set_color("theme.accent", "#D95542")
    assert "#D95542" in window.nav_map["Dashboard"].styleSheet()
    assert "#D95542" in window.settings_page.connect_usb_button.styleSheet()

    window.close()
    settings.close()


def test_main_content_remains_visible(tmp_path):
    app = get_application()
    settings = SettingsManager(tmp_path / "layering.sqlite")
    window = MainWindow(settings=settings)
    window.show()
    app.processEvents()

    assert window.page_stack.currentWidget().isVisible()
    assert window.page_stack.parentWidget() is window.content_widget

    window.close()
    settings.close()


def test_firmware_navigation_requires_usb_and_qflipper_cli(tmp_path):
    app = get_application()
    settings = SettingsManager(tmp_path / "firmware-navigation.sqlite")
    window = MainWindow(settings=settings)
    window.firmware_page.qflipper_cli = None
    window._sync_connection_ui()
    assert not window.nav_map["Firmware"].isEnabled()

    window.connection_manager.connect_usb("COM7", mock_mode=True)
    window._sync_connection_ui()
    assert not window.nav_map["Firmware"].isEnabled()

    window.firmware_page.qflipper_cli = "qFlipper-cli.exe"
    window._sync_connection_ui()
    assert window.nav_map["Firmware"].isEnabled()
    window.show_page("Firmware")
    assert window.page_stack.currentWidget() is window.firmware_page

    window.connection_manager.disconnect()
    window._sync_connection_ui()
    assert not window.nav_map["Firmware"].isEnabled()
    assert window.page_stack.currentIndex() == 0

    window.close()
    settings.close()


def test_system_font_fallback_loads_before_customization():
    get_application()
    ensure_system_fonts()

    assert "Segoe UI" in QFontDatabase.families()
import os

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from lightflipper.config.settings import SettingsManager
from lightflipper.ui.main_window import MainWindow, RemoteControlPage


def get_application() -> QApplication:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QApplication.instance()
    return app if app is not None else QApplication([])


def test_remote_button_is_cleared_after_release():
    app = get_application()
    page = RemoteControlPage()
    page.show()
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

    page.close()


def test_main_window_marks_unavailable_pages_and_sample_files(tmp_path):
    app = get_application()
    settings = SettingsManager(tmp_path / "settings.sqlite")
    window = MainWindow(settings=settings)
    window.show()
    app.processEvents()

    assert window.status_panel.status_label.text() == "Disconnected"
    assert not window.nav_map["NFC"].isEnabled()
    assert window.nav_map["NFC"].toolTip() == "Not available yet"

    window.show_page("File Manager")
    labels = window.page_stack.currentWidget().findChildren(QLabel)
    assert any(label.text() == "Sample filesystem (offline preview)" for label in labels)

    window.close()
    settings.close()
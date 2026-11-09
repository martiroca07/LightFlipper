from __future__ import annotations

import os
from pathlib import Path

from PySide6.QtCore import QProcess, QSize, Qt, Signal
from PySide6.QtGui import QColor, QFont, QFontDatabase, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QColorDialog,
    QFontComboBox,
    QFormLayout,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from lightflipper.config.settings import SettingsManager
from lightflipper.device.connection import DeviceConnectionManager
from lightflipper.device.firmware_update import FirmwareUpdateService
from lightflipper.device.usb import USBDeviceDetector
from lightflipper.file_manager import FlipperFileManager
from lightflipper.remote import RemoteButton, RemoteController
from lightflipper.theme import ThemeManager


_SYSTEM_FONT_IDS: list[int] = []


def ensure_system_fonts() -> None:
    if QFontDatabase.families():
        return
    font_paths = [
        Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "segoeui.ttf",
        Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "arial.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    ]
    for path in font_paths:
        if path.is_file():
            font_id = QFontDatabase.addApplicationFont(str(path))
            if font_id >= 0:
                _SYSTEM_FONT_IDS.append(font_id)


PIXEL_GLYPHS = {
    "dashboard": ("........", ".######.", ".#....#.", ".#.##.#.", ".#....#.", ".######.", "........", "........"),
    "remote": ("...##...", "...##...", "..####..", ".##..##.", "...##...", "...##...", "........", "........"),
    "files": ("..####..", ".######.", ".##.....", ".######.", ".#....#.", ".#....#.", ".######.", "........"),
    "nfc": ("...##...", "..#..#..", ".#....#.", "#..##..#", "#..##..#", ".#....#.", "..#..#..", "...##..."),
    "subghz": ("#......#", ".#....#.", "..#..#..", "...##...", "...##...", "..#..#..", ".#....#.", "#......#"),
    "infrared": ("...##...", "..####..", "..####..", "...##...", "..####..", ".######.", "........", "........"),
    "rfid": (".######.", "#......#", "#..##..#", "#..##..#", "#......#", ".######.", "...##...", "...##..."),
    "apps": (".##..##.", "######.#", "#....###", "#....###", "######.#", ".##..##.", "........", "........"),
    "firmware": ("...##...", "..####..", ".######.", "...##...", "...##...", "...##...", "..####..", "........"),
    "wifi": ("...##...", "..#..#..", ".#....#.", "........", "...##...", "..#..#..", "...##...", "........"),
    "device": ("..####..", ".#....#.", "##....##", "##....##", "##....##", ".#....#.", "..####..", "........"),
    "settings": ("...##...", ".######.", "##.##.##", "########", "##.##.##", ".######.", "...##...", "........"),
    "scan": (".######.", "#......#", "#..##..#", "#.#..#.#", "#.#..#.#", "#..##..#", "#......#", ".######."),
    "connect": ("#.......", "##......", "###.....", "#######.", "#######.", "###.....", "##......", "#......."),
    "disconnect": ("#......#", ".#....#.", "..#..#..", "...##...", "...##...", "..#..#..", ".#....#.", "#......#"),
    "refresh": ("..####..", ".#....#.", "#.......", "#..###..", "#..###..", "...#....", ".#....#.", "..####.."),
    "folder": (".###....", "######..", "#....#..", "#....#..", "#....#..", "#....#..", "######..", "........"),
    "install": ("...##...", "...##...", "########", "..####..", "..####..", ".##..##.", "##....##", "........"),
    "browse": ("..####..", ".#....#.", "#..##..#", "#..##..#", "#......#", ".#....#.", "..####..", "........"),
    "reset": ("..####..", ".#....#.", "#..##..#", "#..##..#", "#......#", ".#....#.", "..####..", "........"),
    "up": ("...##...", "..####..", ".######.", "...##...", "...##...", "...##...", "...##...", "........"),
    "down": ("...##...", "...##...", "...##...", "...##...", ".######.", "..####..", "...##...", "........"),
    "left": ("....#...", "...##...", "..#####.", ".#######", "..#####.", "...##...", "....#...", "........"),
    "right": ("...#....", "...##...", ".#####..", "#######.", ".#####..", "...##...", "...#....", "........"),
    "ok": ("........", "......#.", ".....#..", "#...##..", ".#.#.#..", "..#..#..", "........", "........"),
    "back": ("...##...", "..#..#..", ".#...#..", "######..", ".#...#..", "..#..#..", "...##...", "........"),
}


def create_pixel_icon(name: str, accent: str, foreground: str) -> QIcon:
    pattern = PIXEL_GLYPHS[name]
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
    painter.setPen(Qt.PenStyle.NoPen)
    for y, row in enumerate(pattern):
        for x, pixel in enumerate(row):
            if pixel == ".":
                continue
            painter.fillRect(
                x * 2,
                y * 2,
                2,
                2,
                QColor(accent if pixel == "#" else foreground),
            )
    painter.end()
    return QIcon(pixmap)


def set_pixel_icon(button: QPushButton, name: str, accent: str, foreground: str) -> None:
    button.setProperty("pixelIconName", name)
    button.setProperty("pixelIconForeground", foreground)
    button.setIcon(create_pixel_icon(name, accent, foreground))
    button.setIconSize(QSize(16, 16))


class NavButton(QPushButton):
    def __init__(self, text: str, active: bool = False) -> None:
        super().__init__(text)
        self.setCheckable(True)
        self.setChecked(active)
        self.setMinimumHeight(36)

    def apply_palette(self, accent: str, text: str, sidebar: str) -> None:
        self.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                color: {text};
                border: 1px solid transparent;
                border-radius: 6px;
                padding: 8px 12px;
                text-align: left;
            }}
            QPushButton:checked {{
                background: {accent};
                color: #111214;
            }}
            QPushButton:hover {{
                background: {sidebar};
                border: 1px solid {accent};
            }}
            QPushButton:disabled {{
                background: transparent;
                color: #62666E;
                border: 1px solid transparent;
            }}
            """
        )
        icon_name = self.property("pixelIconName")
        if icon_name:
            set_pixel_icon(self, icon_name, accent, text)


class StatusPanel(QWidget):
    def __init__(self, connection_manager: DeviceConnectionManager | None = None) -> None:
        super().__init__()
        self.connection_manager = connection_manager or DeviceConnectionManager()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        self.status_label = QLabel("Disconnected")
        self.status_label.setProperty("appearanceRole", "title")
        self.status_label.setStyleSheet("color: #F2F2F2; font-weight: 600; font-size: 16px;")

        self.device_label = QLabel("Device: None")
        self.device_label.setProperty("appearanceRole", "secondaryText")

        self.firmware_label = QLabel("Firmware: unavailable")
        self.firmware_label.setProperty("appearanceRole", "secondaryText")

        layout.addWidget(self.status_label)
        layout.addWidget(self.device_label)
        layout.addWidget(self.firmware_label)
        self.refresh()

    def refresh(self) -> None:
        summary = self.connection_manager.get_device_summary()
        connection_type = summary.get("connection_type", "disconnected")
        if connection_type == "usb":
            label = "Connected via USB"
        elif connection_type == "bluetooth":
            label = "Connected via Bluetooth"
        elif connection_type == "connecting":
            label = "Connecting"
        else:
            label = "Disconnected"

        self.status_label.setText(label)
        self.device_label.setText(f"Device: {summary.get('model', 'None')}")
        self.firmware_label.setText(f"Firmware: {summary.get('firmware', 'unavailable')}")


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Dashboard")
        title.setProperty("appearanceRole", "pageTitle")
        layout.addWidget(title)

        subtitle = QLabel("Connected device status and quick actions")
        subtitle.setProperty("appearanceRole", "secondaryText")
        layout.addWidget(subtitle)

        summary = QLabel("USB, Bluetooth and device intelligence will appear here as connectivity modules are enabled.")
        summary.setWordWrap(True)
        summary.setProperty("appearanceRole", "surface")
        layout.addWidget(summary)


class RemoteControlPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.controller = RemoteController()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        title = QLabel("Remote Control")
        title.setProperty("appearanceRole", "pageTitle")
        layout.addWidget(title)

        screen = QLabel("No live device screen")
        screen.setAlignment(Qt.AlignCenter)
        screen.setMinimumHeight(180)
        screen.setProperty("appearanceRole", "surface")
        screen.setMinimumHeight(180)
        self.screen_label = screen
        layout.addWidget(screen)

        pad = QWidget()
        pad_layout = QGridLayout(pad)
        pad_layout.setSpacing(10)

        button_map = {
            (0, 1): (RemoteButton.UP, "Up"),
            (1, 0): (RemoteButton.LEFT, "Left"),
            (1, 1): (RemoteButton.OK, "OK"),
            (1, 2): (RemoteButton.RIGHT, "Right"),
            (2, 1): (RemoteButton.DOWN, "Down"),
            (3, 0): (RemoteButton.BACK, "Back"),
        }

        self.remote_buttons: list[QPushButton] = []
        for position, (button, label) in button_map.items():
            btn = QPushButton(label)
            btn.setMinimumSize(96, 48)
            btn.setProperty("pixelStyle", "remote")
            set_pixel_icon(btn, button.value, "#FF7A24", "#F2F2F2")
            btn.pressed.connect(lambda b=button: self._handle_press(b))
            btn.released.connect(lambda b=button: self._handle_release(b))
            pad_layout.addWidget(btn, *position)
            self.remote_buttons.append(btn)

        layout.addWidget(pad)

        status = QLabel("Offline preview")
        status.setProperty("appearanceRole", "secondaryText")
        self.status_label = status
        layout.addWidget(status)

        self.controller.set_screen_buffer("ready")
        self.update_status()

    def _handle_press(self, button: RemoteButton) -> None:
        self.controller.press_button(button)
        self.update_status()

    def _handle_release(self, button: RemoteButton) -> None:
        self.controller.release_button(button)
        self.update_status()

    def update_status(self) -> None:
        pressed = self.controller.get_pressed_buttons()
        if not pressed:
            self.status_label.setText("Offline preview")
            return
        names = ", ".join(button.value.title() for button in pressed)
        self.status_label.setText(f"Preview: {names}")


class FileManagerPage(QWidget):
    def __init__(
        self,
        manager: FlipperFileManager | None = None,
        connection_manager: DeviceConnectionManager | None = None,
    ) -> None:
        super().__init__()
        self.manager = manager or FlipperFileManager()
        self.connection_manager = connection_manager

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("File Manager")
        title.setProperty("appearanceRole", "pageTitle")
        layout.addWidget(title)

        self.availability_label = QLabel()
        self.availability_label.setWordWrap(True)
        self.availability_label.setProperty("appearanceRole", "secondaryText")
        self._refresh_availability()
        layout.addWidget(self.availability_label)

        toolbar = QHBoxLayout()
        refresh = QPushButton("Refresh")
        set_pixel_icon(refresh, "refresh", "#FF7A24", "#F2F2F2")
        refresh.setProperty("pixelStyle", "secondary")
        refresh.clicked.connect(self.refresh_view)
        self.refresh_button = refresh

        create_dir = QPushButton("Create folder")
        create_dir.setProperty("pixelStyle", "primary")
        set_pixel_icon(create_dir, "folder", "#FF7A24", "#111214")
        create_dir.clicked.connect(self.create_default_folder)
        self.create_folder_button = create_dir

        toolbar.addWidget(refresh)
        toolbar.addWidget(create_dir)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.list_widget = QListWidget()
        self.list_widget.setEnabled(False)
        self.list_widget.setProperty("appearanceRole", "surface")
        layout.addWidget(self.list_widget)
        self.refresh_view()

    def _refresh_availability(self) -> None:
        connected = bool(self.connection_manager and self.connection_manager.is_connected)
        if connected:
            message = "Connected, but live device file transfer is not available yet."
        else:
            message = "Connect a Flipper to access its files."
        self.availability_label.setText(message)

    def upload_file(self, path: str, payload: str) -> None:
        self.manager.upload_file(path, payload)

    def create_default_folder(self) -> None:
        self.manager.create_directory("custom", "/")
        self.refresh_view()

    def refresh_view(self) -> None:
        self.list_widget.clear()
        self._refresh_availability()
        self.refresh_button.setEnabled(False)
        self.create_folder_button.setEnabled(False)
        self.refresh_button.setToolTip("Live device file transfer is not available yet")
        self.create_folder_button.setToolTip("Live device file transfer is not available yet")


class SettingsPage(QWidget):
    connection_changed = Signal()
    appearance_changed = Signal()

    def __init__(
        self,
        connection_manager: DeviceConnectionManager | None = None,
        usb_detector: USBDeviceDetector | None = None,
        settings: SettingsManager | None = None,
    ) -> None:
        super().__init__()
        self.connection_manager = connection_manager or DeviceConnectionManager()
        self.usb_detector = usb_detector or USBDeviceDetector()
        self.settings = settings or SettingsManager()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Settings")
        title.setProperty("appearanceRole", "pageTitle")
        layout.addWidget(title)

        self.status_label = QLabel()
        self.status_label.setProperty("appearanceRole", "title")
        self.connection_status = self.status_label
        layout.addWidget(self.status_label)

        actions = QHBoxLayout()
        self.port_combo = QComboBox()
        self.scan_usb_button = QPushButton("Scan USB")
        set_pixel_icon(self.scan_usb_button, "scan", "#FF7A24", "#F2F2F2")
        self.connect_usb_button = QPushButton("Connect USB")
        self.connect_usb_button.setProperty("pixelStyle", "primary")
        set_pixel_icon(self.connect_usb_button, "connect", "#FF7A24", "#111214")
        self.disconnect_button = QPushButton("Disconnect")
        set_pixel_icon(self.disconnect_button, "disconnect", "#FF7A24", "#F2F2F2")

        self.scan_usb_button.clicked.connect(self.refresh_usb_ports)
        self.connect_usb_button.clicked.connect(self._connect_usb)
        self.disconnect_button.clicked.connect(self._disconnect)
        actions.addWidget(self.port_combo, 1)
        actions.addWidget(self.scan_usb_button)
        actions.addWidget(self.connect_usb_button)
        actions.addWidget(self.disconnect_button)
        layout.addLayout(actions)

        appearance_title = QLabel("Appearance")
        appearance_title.setProperty("appearanceRole", "sectionTitle")
        layout.addWidget(appearance_title)

        appearance_form = QFormLayout()
        appearance_form.setHorizontalSpacing(18)
        appearance_form.setVerticalSpacing(8)
        self.color_buttons: dict[str, QPushButton] = {}
        colors = (
            ("Accent", "theme.accent"),
            ("Window background", "theme.background"),
            ("Sidebar", "theme.secondary_background"),
            ("Panels", "theme.panel"),
            ("Primary text", "theme.text"),
            ("Secondary text", "theme.secondary_text"),
        )
        for label, key in colors:
            button = QPushButton()
            button.setFixedWidth(128)
            button.clicked.connect(lambda _checked=False, color_key=key: self._choose_color(color_key))
            self.color_buttons[key] = button
            appearance_form.addRow(label, button)
            self._refresh_color_button(key)

        self.font_family_combo = QFontComboBox()
        self.font_family_combo.setCurrentFont(QFont(str(self.settings.get("ui.font_family", "Segoe UI"))))
        self.font_family_combo.currentFontChanged.connect(self._set_font_family)
        appearance_form.addRow("Font", self.font_family_combo)

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(int(self.settings.get("ui.font_size", 12)))
        self.font_size_spin.valueChanged.connect(self._set_font_size)
        appearance_form.addRow("Font size", self.font_size_spin)

        self.sidebar_toggle = QCheckBox("Show navigation sidebar")
        self.sidebar_toggle.setChecked(bool(self.settings.get("ui.sidebar_visible", True)))
        self.sidebar_toggle.toggled.connect(self._set_sidebar_visible)
        appearance_form.addRow("Layout", self.sidebar_toggle)

        layout.addLayout(appearance_form)

        self.reset_appearance_button = QPushButton("Reset appearance")
        set_pixel_icon(self.reset_appearance_button, "reset", "#FF7A24", "#F2F2F2")
        self.reset_appearance_button.clicked.connect(self.reset_appearance)
        layout.addWidget(self.reset_appearance_button)
        layout.addStretch(1)

        self.refresh_usb_ports()

    def _refresh_color_button(self, key: str) -> None:
        color = str(self.settings.get(key))
        button = self.color_buttons[key]
        button.setText(color.upper())
        button.setStyleSheet(
            f"background: {color}; color: {'#111214' if QColor(color).lightness() > 145 else '#F2F2F2'};"
            "border: 1px solid #62666E; border-radius: 4px; padding: 5px;"
        )

    def _choose_color(self, key: str) -> None:
        color = QColorDialog.getColor(QColor(str(self.settings.get(key))), self)
        if color.isValid():
            self.set_color(key, color.name())

    def set_color(self, key: str, color: str) -> None:
        selected = QColor(color)
        if key not in self.color_buttons or not selected.isValid():
            return
        self.settings.set(key, selected.name().upper())
        self._refresh_color_button(key)
        self.appearance_changed.emit()

    def _set_font_family(self, font: QFont) -> None:
        self.settings.set("ui.font_family", font.family())
        self.appearance_changed.emit()

    def _set_font_size(self, size: int) -> None:
        self.settings.set("ui.font_size", size)
        self.appearance_changed.emit()

    def _set_sidebar_visible(self, visible: bool) -> None:
        self.settings.set("ui.sidebar_visible", visible)
        self.appearance_changed.emit()

    def reset_appearance(self) -> None:
        defaults = SettingsManager.DEFAULTS
        for key in self.color_buttons:
            self.settings.set(key, defaults[key])
            self._refresh_color_button(key)
        self.font_family_combo.setCurrentFont(QFont(defaults["ui.font_family"]))
        self.font_size_spin.setValue(defaults["ui.font_size"])
        self.sidebar_toggle.setChecked(defaults["ui.sidebar_visible"])
        self.appearance_changed.emit()

    def refresh_usb_ports(self) -> None:
        ports = self.usb_detector.detect_ports()
        self.port_combo.clear()
        for port in ports:
            self.port_combo.addItem(f"{port.port_name} - {port.description}", port.port_name)

        connected = self.connection_manager.is_connected
        self.connect_usb_button.setEnabled(bool(ports) and not connected)
        self.disconnect_button.setEnabled(connected)
        if connected:
            self.status_label.setText("Connected via USB")
        elif ports:
            self.status_label.setText(f"Found {len(ports)} Flipper USB device(s)")
        else:
            self.status_label.setText("No Flipper USB device found")

    def _connect_usb(self) -> None:
        port_name = self.port_combo.currentData()
        if not port_name:
            return
        if self.connection_manager.connect_usb(port_name, mock_mode=False):
            self.status_label.setText("Connected via USB")
        else:
            self.status_label.setText(self.connection_manager.last_error or "USB connection failed")
        self.refresh_usb_ports()
        self.connection_changed.emit()

    def _disconnect(self) -> None:
        self.connection_manager.disconnect()
        self.refresh_usb_ports()
        self.connection_changed.emit()


class FirmwarePage(QWidget):
    connection_changed = Signal()

    def __init__(
        self,
        connection_manager: DeviceConnectionManager,
        service: FirmwareUpdateService | None = None,
        qflipper_cli: str | None = None,
    ) -> None:
        super().__init__()
        self.connection_manager = connection_manager
        self.service = service or FirmwareUpdateService()
        self.qflipper_cli = qflipper_cli or self.service.find_qflipper_cli()
        self.process = QProcess(self)
        self.process.finished.connect(self._process_finished)
        self.process.errorOccurred.connect(self._process_error)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Firmware update")
        title.setProperty("appearanceRole", "pageTitle")
        layout.addWidget(title)

        self.device_status = QLabel()
        layout.addWidget(self.device_status)

        info = QLabel("Select a qFlipper-compatible .dfu firmware file. Keep the Flipper connected by USB and do not unplug it during installation.")
        info.setWordWrap(True)
        info.setProperty("appearanceRole", "secondaryText")
        layout.addWidget(info)

        file_row = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Choose a .dfu file")
        self.file_path.textChanged.connect(self._refresh_state)
        self.browse_button = QPushButton("Choose .dfu")
        set_pixel_icon(self.browse_button, "browse", "#FF7A24", "#F2F2F2")
        self.browse_button.clicked.connect(self._browse_file)
        file_row.addWidget(self.file_path, 1)
        file_row.addWidget(self.browse_button)
        layout.addLayout(file_row)

        self.file_status = QLabel("No firmware file selected")
        layout.addWidget(self.file_status)

        self.install_button = QPushButton("Install firmware")
        self.install_button.setProperty("pixelStyle", "primary")
        set_pixel_icon(self.install_button, "install", "#FF7A24", "#111214")
        self.install_button.clicked.connect(self._confirm_install)
        layout.addWidget(self.install_button)
        layout.addStretch(1)
        self._refresh_state()

    def _browse_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select firmware file",
            "",
            "Flipper firmware (*.dfu)",
        )
        if file_path:
            self.file_path.setText(file_path)

    def _refresh_state(self) -> None:
        error = self.service.validate_dfu(self.file_path.text()) if self.file_path.text() else None
        if not self.file_path.text():
            self.file_status.setText("No firmware file selected")
        elif error:
            self.file_status.setText(error)
        else:
            self.file_status.setText("DFU file ready")

        usb_connected = (
            self.connection_manager.is_connected
            and self.connection_manager.connection_type == "usb"
        )
        self.device_status.setText(
            "Connected via USB" if usb_connected else "Connect a Flipper over USB to install firmware"
        )
        self.install_button.setEnabled(
            usb_connected
            and error is None
            and bool(self.file_path.text())
            and bool(self.qflipper_cli)
            and self.process.state() == QProcess.ProcessState.NotRunning
        )
        self.install_button.setToolTip(
            "" if self.qflipper_cli else "Install qFlipper to use its official firmware installer"
        )

    def _confirm_install(self) -> None:
        error = self.service.validate_dfu(self.file_path.text())
        usb_connected = (
            self.connection_manager.is_connected
            and self.connection_manager.connection_type == "usb"
        )
        if error or not self.qflipper_cli or not usb_connected:
            self._refresh_state()
            return
        confirmation = QMessageBox.question(
            self,
            "Confirm firmware installation",
            "Firmware installation can take several minutes. Keep the Flipper connected and do not interrupt power. Continue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirmation != QMessageBox.StandardButton.Yes:
            return

        self.connection_manager.disconnect()
        command = self.service.build_install_command(
            self.qflipper_cli, self.file_path.text()
        )
        self.process.start(command[0], command[1:])
        self.file_status.setText("Starting qFlipper firmware installer...")
        self._refresh_state()
        self.connection_changed.emit()

    def _process_finished(self, exit_code: int, _exit_status) -> None:
        self.file_status.setText(
            "qFlipper installer finished successfully"
            if exit_code == 0
            else f"qFlipper installer exited with code {exit_code}"
        )
        self._refresh_state()

    def _process_error(self, _error) -> None:
        self.file_status.setText("Could not start qFlipper CLI. Check its installation.")
        self._refresh_state()

class MainWindow(QMainWindow):
    def __init__(self, settings: SettingsManager | None = None, theme_manager: ThemeManager | None = None) -> None:
        super().__init__()
        ensure_system_fonts()
        self.settings = settings or SettingsManager()
        self.theme_manager = theme_manager or ThemeManager()
        self.connection_manager = DeviceConnectionManager()

        self.setWindowTitle("LightFlipper")
        self.resize(self.settings.get("window.width", 1280), self.settings.get("window.height", 820))
        self.setMinimumSize(980, 640)

        container = QWidget()
        container.setObjectName("mainContainer")
        root = QHBoxLayout(container)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QWidget()
        self.sidebar_widget = sidebar
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 12, 12, 12)
        sidebar_layout.setSpacing(8)

        brand = QLabel("LightFlipper")
        brand.setObjectName("brandLabel")
        self.brand_label = brand
        sidebar_layout.addWidget(brand)

        pages = {
            "Dashboard": DashboardPage(),
            "Remote Control": RemoteControlPage(),
            "File Manager": FileManagerPage(connection_manager=self.connection_manager),
            "Firmware": FirmwarePage(self.connection_manager),
            "Settings": SettingsPage(
                connection_manager=self.connection_manager,
                settings=self.settings,
            ),
        }

        self.page_stack = QStackedWidget()
        for page in pages.values():
            self.page_stack.addWidget(page)

        nav_items = [
            "Dashboard",
            "Remote Control",
            "File Manager",
            "NFC",
            "Sub-GHz",
            "Infrared",
            "RFID",
            "Applications",
            "Firmware",
            "Wi-Fi Devboard",
            "Device Information",
            "Settings",
        ]

        self.nav_map = {}
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        self.firmware_page = pages["Firmware"]
        for index, item in enumerate(nav_items):
            button = NavButton(item, active=index == 0)
            nav_icons = {
                "Dashboard": "dashboard",
                "Remote Control": "remote",
                "File Manager": "files",
                "NFC": "nfc",
                "Sub-GHz": "subghz",
                "Infrared": "infrared",
                "RFID": "rfid",
                "Applications": "apps",
                "Firmware": "firmware",
                "Wi-Fi Devboard": "wifi",
                "Device Information": "device",
                "Settings": "settings",
            }
            set_pixel_icon(button, nav_icons[item], "#FF7A24", "#F2F2F2")
            self.nav_group.addButton(button)
            if item in pages:
                button.clicked.connect(lambda checked=False, name=item: self.show_page(name))
            else:
                button.setEnabled(False)
                button.setToolTip("Not available yet")
            if item == "File Manager":
                button.setEnabled(self.connection_manager.is_connected)
                if not button.isEnabled():
                    button.setToolTip("Connect a Flipper to use the file manager")
            if item == "Remote Control":
                button.setEnabled(self.connection_manager.is_connected)
                if not button.isEnabled():
                    button.setToolTip("Connect a Flipper to use remote control")
            if item == "Firmware":
                firmware_ready = (
                    self.connection_manager.connection_type == "usb"
                    and bool(self.firmware_page.qflipper_cli)
                )
                button.setEnabled(firmware_ready)
                if not firmware_ready:
                    button.setToolTip(
                        "Connect over USB and install qFlipper to update firmware"
                    )
            sidebar_layout.addWidget(button)
            self.nav_map[item] = button

        self.settings_page = pages["Settings"]
        self.settings_page.connection_changed.connect(self._sync_connection_ui)
        self.settings_page.appearance_changed.connect(self.apply_theme)
        self.firmware_page.connection_changed.connect(self._sync_connection_ui)

        sidebar_layout.addStretch()
        self.status_panel = StatusPanel(self.connection_manager)
        sidebar_layout.addWidget(self.status_panel)

        content = QWidget()
        self.content_widget = content
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.addWidget(self.page_stack)

        root.addWidget(sidebar, 1)
        root.addWidget(content, 5)
        self.setCentralWidget(container)
        self.show_page("Dashboard")
        self.apply_theme()

    def show_page(self, name: str) -> None:
        page_names = ["Dashboard", "Remote Control", "File Manager", "Firmware", "Settings"]
        if name not in page_names:
            return
        if name == "File Manager" and not self.connection_manager.is_connected:
            return
        if name == "Remote Control" and not self.connection_manager.is_connected:
            return
        if name == "Firmware" and not self.nav_map["Firmware"].isEnabled():
            return
        page_index = page_names.index(name)
        self.page_stack.setCurrentIndex(page_index)
        if hasattr(self, "nav_map") and name in self.nav_map:
            self.nav_map[name].setChecked(True)
        self.status_panel.refresh()

    def _sync_connection_ui(self) -> None:
        connected = self.connection_manager.is_connected
        file_manager_button = self.nav_map["File Manager"]
        file_manager_button.setEnabled(connected)
        file_manager_button.setToolTip(
            "" if connected else "Connect a Flipper to use the file manager"
        )
        remote_button = self.nav_map["Remote Control"]
        remote_button.setEnabled(connected)
        remote_button.setToolTip(
            "" if connected else "Connect a Flipper to use remote control"
        )
        self.page_stack.widget(2)._refresh_availability()
        self.firmware_page._refresh_state()
        firmware_ready = (
            self.connection_manager.connection_type == "usb"
            and bool(self.firmware_page.qflipper_cli)
        )
        firmware_button = self.nav_map["Firmware"]
        firmware_button.setEnabled(firmware_ready)
        firmware_button.setToolTip(
            "" if firmware_ready else "Connect over USB and install qFlipper to update firmware"
        )
        self.status_panel.refresh()
        if not connected and self.page_stack.currentIndex() in (1, 2, 3):
            self.show_page("Dashboard")

    def apply_theme(self) -> None:
        current = self.theme_manager.current
        if current is None:
            return
        current.accent = self.settings.get("theme.accent", current.accent)
        current.background = self.settings.get("theme.background", current.background)
        current.secondary_background = self.settings.get(
            "theme.secondary_background", current.secondary_background
        )
        current.panel = self.settings.get("theme.panel", current.panel)
        current.text = self.settings.get("theme.text", current.text)
        current.secondary_text = self.settings.get(
            "theme.secondary_text", current.secondary_text
        )
        current.font_family = self.settings.get("ui.font_family", current.font_family)
        current.font_size = int(self.settings.get("ui.font_size", current.font_size))

        self.setStyleSheet(
            f"""
            QMainWindow {{
                background: {current.background};
                color: {current.text};
            }}
            QWidget {{
                color: {current.text};
                font-family: '{current.font_family}';
                font-size: {current.font_size}pt;
            }}
            QLabel#brandLabel {{
                color: {current.accent};
                font-size: 22pt;
                font-weight: 700;
                padding: 8px 8px 16px 8px;
            }}
            QLabel[appearanceRole="pageTitle"] {{
                font-size: 28pt;
                font-weight: 600;
            }}
            QLabel[appearanceRole="sectionTitle"] {{
                font-size: 19pt;
                font-weight: 600;
            }}
            QLabel[appearanceRole="secondaryText"] {{
                color: {current.secondary_text};
            }}
            QLabel[appearanceRole="surface"] {{
                color: {current.text};
                background: {current.panel};
                border: 1px solid {current.border};
                border-radius: 6px;
                padding: 12px;
            }}
            """
        )
        self.sidebar_widget.setStyleSheet(
            f"background: {current.secondary_background}; border-right: 1px solid {current.panel};"
        )
        for button in self.nav_map.values():
            button.apply_palette(
                current.accent, current.text, current.secondary_background
            )
        for button in self.findChildren(QPushButton):
            icon_name = button.property("pixelIconName")
            if icon_name and not isinstance(button, NavButton):
                is_primary = button.property("pixelStyle") == "primary"
                foreground = (
                    "#111214"
                    if QColor(current.accent).lightness() > 145
                    else "#F2F2F2"
                )
                set_pixel_icon(
                    button,
                    icon_name,
                    current.accent,
                    foreground if is_primary else current.text,
                )
                if button not in self.settings_page.color_buttons.values():
                    role = button.property("pixelStyle")
                    if role == "remote":
                        background = current.panel
                        text_color = current.text
                        radius = 4
                    else:
                        background = current.accent if is_primary else current.panel
                        text_color = foreground if is_primary else current.text
                        radius = 5
                    button.setStyleSheet(
                        f"QPushButton {{ background: {background}; color: {text_color}; "
                        f"border: 1px solid {current.border}; border-radius: {radius}px; padding: 7px 10px; }} "
                        f"QPushButton:hover {{ border-color: {current.accent}; }} "
                        f"QPushButton:pressed {{ background: {current.accent}; color: {foreground}; }} "
                        "QPushButton:disabled { color: #777B82; background: #292C31; }"
                    )
        self.page_stack.widget(2).list_widget.setStyleSheet(
            f"background: {current.panel}; color: {current.text}; border: 1px solid {current.border}; border-radius: 6px; padding: 8px;"
        )
        self.sidebar_widget.setVisible(
            bool(self.settings.get("ui.sidebar_visible", True))
        )
        self.content_widget.setStyleSheet(f"background: {current.background};")

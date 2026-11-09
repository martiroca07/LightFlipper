from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from lightflipper.config.settings import SettingsManager
from lightflipper.file_manager import FlipperFileManager
from lightflipper.remote import RemoteButton, RemoteController
from lightflipper.theme import ThemeManager


class NavButton(QPushButton):
    def __init__(self, text: str, active: bool = False) -> None:
        super().__init__(text)
        self.setCheckable(True)
        self.setChecked(active)
        self.setMinimumHeight(36)
        self.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                color: #F2F2F2;
                border: 1px solid transparent;
                border-radius: 10px;
                padding: 8px 12px;
                text-align: left;
            }
            QPushButton:checked {
                background: #FF7A24;
                color: #111214;
            }
            QPushButton:hover {
                background: rgba(255, 122, 36, 0.12);
                border: 1px solid rgba(255, 122, 36, 0.35);
            }
            """
        )


class StatusPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        self.status_label = QLabel("Disconnected")
        self.status_label.setStyleSheet("color: #F2F2F2; font-weight: 600; font-size: 16px;")

        self.device_label = QLabel("Device: None")
        self.device_label.setStyleSheet("color: #9298A2;")

        self.firmware_label = QLabel("Firmware: unavailable")
        self.firmware_label.setStyleSheet("color: #9298A2;")

        layout.addWidget(self.status_label)
        layout.addWidget(self.device_label)
        layout.addWidget(self.firmware_label)


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Dashboard")
        title.setStyleSheet("color: #F2F2F2; font-size: 28px; font-weight: 600;")
        layout.addWidget(title)

        subtitle = QLabel("Connected device status and quick actions")
        subtitle.setStyleSheet("color: #9298A2;")
        layout.addWidget(subtitle)

        summary = QLabel("USB, Bluetooth and device intelligence will appear here as connectivity modules are enabled.")
        summary.setWordWrap(True)
        summary.setStyleSheet("color: #F2F2F2; background: #202329; border-radius: 12px; padding: 16px;")
        layout.addWidget(summary)


class RemoteControlPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.controller = RemoteController()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        title = QLabel("Remote Control")
        title.setStyleSheet("color: #F2F2F2; font-size: 28px; font-weight: 600;")
        layout.addWidget(title)

        screen = QLabel("Screen sync ready")
        screen.setAlignment(Qt.AlignCenter)
        screen.setMinimumHeight(180)
        screen.setStyleSheet("background: #202329; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; color: #F2F2F2; font-size: 16px;")
        self.screen_label = screen
        layout.addWidget(screen)

        pad = QWidget()
        pad_layout = QGridLayout(pad)
        pad_layout.setSpacing(10)

        button_map = {
            (0, 1): (RemoteButton.UP, "↑"),
            (1, 0): (RemoteButton.LEFT, "←"),
            (1, 1): (RemoteButton.OK, "OK"),
            (1, 2): (RemoteButton.RIGHT, "→"),
            (2, 1): (RemoteButton.DOWN, "↓"),
            (3, 0): (RemoteButton.BACK, "Back"),
        }

        for position, (button, label) in button_map.items():
            btn = QPushButton(label)
            btn.setMinimumSize(96, 48)
            btn.setStyleSheet(
                """
                QPushButton {
                    background: #202329;
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 10px;
                    color: #F2F2F2;
                    font-weight: 600;
                }
                QPushButton:pressed {
                    background: #FF7A24;
                    color: #111214;
                }
                """
            )
            btn.pressed.connect(lambda b=button: self._handle_press(b))
            btn.released.connect(lambda b=button: self._handle_release(b))
            pad_layout.addWidget(btn, *position)

        layout.addWidget(pad)

        status = QLabel("No buttons pressed")
        status.setStyleSheet("color: #9298A2;")
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
            self.status_label.setText("No buttons pressed")
            return
        names = ", ".join(button.value.title() for button in pressed)
        self.status_label.setText(f"Pressed: {names}")


class FileManagerPage(QWidget):
    def __init__(self, manager: FlipperFileManager | None = None) -> None:
        super().__init__()
        self.manager = manager or FlipperFileManager()
        self.upload_file("/nfc/demo.txt", "demo payload")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("File Manager")
        title.setStyleSheet("color: #F2F2F2; font-size: 28px; font-weight: 600;")
        layout.addWidget(title)

        toolbar = QHBoxLayout()
        refresh = QPushButton("Refresh")
        refresh.setStyleSheet("background: #202329; border-radius: 8px; padding: 8px 12px; color: #F2F2F2;")
        refresh.clicked.connect(self.refresh_view)

        create_dir = QPushButton("Create folder")
        create_dir.setStyleSheet("background: #FF7A24; color: #111214; border-radius: 8px; padding: 8px 12px; font-weight: 600;")
        create_dir.clicked.connect(self.create_default_folder)

        toolbar.addWidget(refresh)
        toolbar.addWidget(create_dir)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(
            """
            QListWidget {
                background: #202329;
                border-radius: 12px;
                padding: 8px;
                color: #F2F2F2;
            }
            """
        )
        layout.addWidget(self.list_widget)
        self.refresh_view()

    def upload_file(self, path: str, payload: str) -> None:
        self.manager.upload_file(path, payload)

    def create_default_folder(self) -> None:
        self.manager.create_directory("custom", "/")
        self.refresh_view()

    def refresh_view(self) -> None:
        self.list_widget.clear()
        entries = self.manager.list_directory("/")
        for entry in entries:
            item = QListWidgetItem(f"{entry.name}  ({'folder' if entry.is_directory else entry.extension or 'file'})")
            self.list_widget.addItem(item)


class MainWindow(QMainWindow):
    def __init__(self, settings: SettingsManager | None = None, theme_manager: ThemeManager | None = None) -> None:
        super().__init__()
        self.settings = settings or SettingsManager()
        self.theme_manager = theme_manager or ThemeManager()

        self.setWindowTitle("LightFlipper")
        self.resize(self.settings.get("window.width", 1280), self.settings.get("window.height", 820))
        self.setMinimumSize(980, 640)

        self.setStyleSheet(
            """
            QMainWindow {
                background: #111214;
                color: #F2F2F2;
            }
            QWidget {
                color: #F2F2F2;
                font-family: 'Segoe UI';
            }
            """
        )

        container = QWidget()
        container.setObjectName("mainContainer")
        root = QHBoxLayout(container)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QWidget()
        sidebar.setStyleSheet("background: #191B1F; border: 1px solid rgba(255,255,255,0.04);")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 12, 12, 12)
        sidebar_layout.setSpacing(8)

        brand = QLabel("LightFlipper")
        brand.setStyleSheet("color: #FF7A24; font-size: 22px; font-weight: 700; padding: 8px 8px 16px 8px;")
        sidebar_layout.addWidget(brand)

        pages = {
            "Dashboard": DashboardPage(),
            "Remote Control": RemoteControlPage(),
            "File Manager": FileManagerPage(),
            "Settings": DashboardPage(),
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
        for index, item in enumerate(nav_items):
            button = NavButton(item, active=index == 0)
            if item in pages:
                button.clicked.connect(lambda checked=False, name=item: self.show_page(name))
            sidebar_layout.addWidget(button)
            self.nav_map[item] = button

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(StatusPanel())

        content = QWidget()
        content.setStyleSheet("background: #111214;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.addWidget(self.page_stack)

        root.addWidget(sidebar, 1)
        root.addWidget(content, 5)
        self.setCentralWidget(container)
        self.show_page("Dashboard")

    def show_page(self, name: str) -> None:
        page_names = ["Dashboard", "Remote Control", "File Manager", "Settings"]
        if name not in page_names:
            return
        page_index = page_names.index(name)
        self.page_stack.setCurrentIndex(page_index)

    def apply_theme(self) -> None:
        current = self.theme_manager.current
        if current is None:
            return
        self.setStyleSheet(
            f"""
            QMainWindow {{
                background: {current.background};
                color: {current.text};
            }}
            QWidget {{
                color: {current.text};
                font-family: '{current.font_family}';
            }}
            """
        )

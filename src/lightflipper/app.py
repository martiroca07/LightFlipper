from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from lightflipper.config.settings import SettingsManager
from lightflipper.logging_config import configure_logging
from lightflipper.theme import ThemeManager
from lightflipper.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("LightFlipper")
    app.setOrganizationName("LightFlipper")

    settings = SettingsManager()
    theme_manager = ThemeManager()
    logger = configure_logging()
    logger.info("LightFlipper started")

    window = MainWindow(settings=settings, theme_manager=theme_manager)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

# --- WaveLength DAW - Main File --- #

import sys
import constants
from tilingmanager import WindowManager
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

style_path = constants.FILEPATH / "style" / "style.css"
stylesheet = ""

try:
    stylesheet = style_path.read_text(encoding="utf-8")
except OSError as exception:
    print("Stylesheet file not found: ", exception)

class WavelengthWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Widget Attributes --- #
        self.setObjectName("WavelengthMainWindow")
        self.setStyleSheet(stylesheet)
        self.setWindowTitle(f"{constants.APP_NAME} {constants.VERSION}")

        # --- QStackedWidget Setup --- #
        self.page_container = QStackedWidget()
        self.page_container.setCurrentIndex(0)
        self.setCentralWidget(self.page_container)

        self.wm = WindowManager()
        self.setCentralWidget(self.wm)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setApplicationName(f"{constants.APP_NAME}")
    app.setOrganizationName(f"{constants.ORGANIZATION}")

    main_window = WavelengthWindow()
    main_window.showMaximized()

    sys.exit(app.exec())
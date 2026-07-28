from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMenu, QToolButton
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon
from constants import PanelType
import constants

# --- Base Subwindow --- #
class SubWindowButtons(QWidget):

    type_changed = Signal(object)

    def __init__(self):
        super().__init__()

        self.setObjectName("SubWindowButtonContainer")
        self.setAttribute(Qt.WA_StyledBackground, True)

        # --- Close Button --- #
        self.titlebar_close = QToolButton()
        self.titlebar_close.setIcon(QIcon(rf"{constants.FILEPATH.parent}\data\assets\button_icons\close_icon.png")) # Icons are color #AAAAAA
        self.titlebar_close.setIconSize(QSize(16, 16))
        self.titlebar_close.setObjectName("SubWindowCloseButton")

        # --- Menu Button and Dropdown --- #
        self.titlebar_menu = QToolButton()
        self.titlebar_menu.setIcon(QIcon(rf"{constants.FILEPATH.parent}\data\assets\button_icons\menu_icon.png")) # Icons are color #AAAAAA
        self.titlebar_menu.setIconSize(QSize(12, 12))
        self.titlebar_menu.setObjectName("SubWindowMenuButton")

        self.dropdown_menu = QMenu(self.titlebar_menu)
        self.build_menu()
        self.titlebar_menu.setMenu(self.dropdown_menu)
        self.titlebar_menu.setPopupMode(QToolButton.InstantPopup)

        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(8, 4, 8, 0)
        self.button_layout.addWidget(self.titlebar_menu)
        self.button_layout.addWidget(self.titlebar_close)

        self.setLayout(self.button_layout)

    def build_menu(self):
        self.dropdown_menu.clear()
        self.dropdown_menu.setWindowFlags(self.dropdown_menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        split_horizontal_action = self.dropdown_menu.addAction("Split Horizontally")
        split_vertical_action = self.dropdown_menu.addAction("Split Vertically")
        self.dropdown_menu.addSeparator()
        window_type_menu = self.dropdown_menu.addMenu("Window Type")
        window_type_menu.setWindowFlags(self.dropdown_menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        for p_type in PanelType:
            action = window_type_menu.addAction(p_type.name.replace("_", " ").title())
            action.triggered.connect(lambda checked=False, t=p_type: self.type_changed.emit(t))
        
class SubWindow(QWidget):

    type_changed = Signal(object)

    def __init__(self, title):
        super().__init__()

        self.title = title

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.titlebar_title = QLabel(self.title)
        self.titlebar_title.setObjectName("SubWindowTitle")

        self.titlebar_buttons = SubWindowButtons()
        self.titlebar_buttons.type_changed.connect(self.type_changed.emit)

        self.titlebar_layout = QHBoxLayout()
        self.titlebar_layout.addWidget(self.titlebar_title)
        self.titlebar_layout.addStretch()
        self.titlebar_layout.addWidget(self.titlebar_buttons)
        self.titlebar_layout.setSpacing(0)

        self.main_layout.addLayout(self.titlebar_layout)

        self.content_widget = QWidget()
        self.content_widget.setObjectName("SubWindowBase")

        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(4, 4, 4, 4)
        self.content_layout.setSpacing(4)

        self.main_layout.addWidget(self.content_widget, stretch=1)

    def set_title(self, title: str):
        self.title = title
        self.titlebar_title.setText(title)
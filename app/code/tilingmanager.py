from enum import Enum, auto
import constants
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QHBoxLayout, QPushButton, QToolButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class PanelType(Enum):
    SIDEBAR = auto()
    BROWSER = auto()
    TIMELINE = auto()
    MIXER = auto()
    BEAT_EDITOR = auto()
    SONG_EDITOR = auto()
    PLUGIN_VIEW = auto()
    TEST_WINDOW = auto()

# --- Base Subwindow --- #
class SubWindowButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("SubWindowButtonContainer")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.titlebar_close = QToolButton()
        self.titlebar_close.setIcon(QIcon(rf"{constants.FILEPATH.parent}\data\assets\button_icons\close_icon.png")) # Icons are color #FFFFFF
        self.titlebar_close.setIconSize(QSize(16, 16))
        self.titlebar_close.setObjectName("SubWindowCloseButton")
        
        self.titlebar_menu = QPushButton("▼")
        self.titlebar_menu.setObjectName("SubWindowMenuButton")

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.titlebar_menu)
        self.button_layout.addWidget(self.titlebar_close)

        self.setLayout(self.button_layout)

        
class SubWindow(QWidget):
    def __init__(self, title):
        super().__init__()

        self.title = title

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.titlebar_title = QLabel(self.title)
        self.titlebar_title.setObjectName("SubWindowTitle")

        self.titlebar_buttons = SubWindowButtons()

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

# --- Specific Windows --- #

# Test Window
class TestWindow(SubWindow):
    def __init__(self, title):
        super().__init__(title)

        label = QLabel("WaveLength Test Window :o")
        self.content_layout.addWidget(label)

# Sidebar Window
class SidebarWindow(SubWindow):
    def __init__(self, title):
        super().__init__(title)

        label = QLabel("WaveLength Sidebar :o")
        self.content_layout.addWidget(label)

# --- Tiling Manager --- #
class PanelRegistry:
    panels = {
        PanelType.TEST_WINDOW: {
            "title": "Test Window",
            "widget": TestWindow,
            "minimum_size": QSize(250, 300),
            "maximum_size": QSize(2000, constants.MAX_SIZE),
        },
        PanelType.SIDEBAR: {
            "title": "Sidebar",
            "widget": SidebarWindow,
            "minimum_size": QSize(350, 300),
            "maximum_size": QSize(350, constants.MAX_SIZE),
        },
    }

    @staticmethod
    def create(panel_type):
        data = PanelRegistry.panels[panel_type]

        panel = data["widget"](data["title"])

        panel.setMinimumSize(data["minimum_size"])
        panel.setMaximumSize(data["maximum_size"])

        return panel
    
class WindowManager(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)

        self.root_split = QSplitter(Qt.Horizontal)
        self.root_split.setChildrenCollapsible(False)

        self.main_layout.addWidget(self.root_split)
        self.main_layout.setContentsMargins(6, 6, 6, 6)

        self.add_panel(PanelType.TEST_WINDOW)
        self.add_panel(PanelType.SIDEBAR)

    def add_panel(self, panel_type):
        panel = PanelRegistry.create(panel_type)
        self.root_split.addWidget(panel)
from enum import Enum, auto
import constants
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QHBoxLayout, QVBoxLayout, QToolButton, QMenu
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction

# --- Tree Setup --- #
class SplitDirection(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()

class PanelNode:
    def __init__(self, panel_type):
        self.panel_type = panel_type

class SplitNode:
    def __init__(self, direction, ratio=0.5):
        self.direction = direction
        self.ratio = ratio
        self.first = None
        self.second = None

# --- Window Types --- #
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

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(4, 4, 4, 4)

        self.root = SplitNode(SplitDirection.HORIZONTAL)
        self.root.first = PanelNode(PanelType.TEST_WINDOW)

        self.right = SplitNode(SplitDirection.VERTICAL)
        self.right.first = PanelNode(PanelType.SIDEBAR)
        self.right.second = PanelNode(PanelType.TEST_WINDOW)

        self.root.second = self.right

        self.widget_tree = build(self.root)

        self.layout.addWidget(self.widget_tree)

def build(node):
    if isinstance(node, PanelNode):
        return PanelRegistry.create(node.panel_type)

    orientation = (
        Qt.Horizontal
        if node.direction == SplitDirection.HORIZONTAL
        else Qt.Vertical
    )

    splitter = QSplitter(orientation)
    splitter.setChildrenCollapsible(False)

    splitter.addWidget(build(node.first))
    splitter.addWidget(build(node.second))

    return splitter
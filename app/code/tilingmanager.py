from enum import Enum, auto
import constants
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QHBoxLayout, QVBoxLayout, QToolButton, QMenu
from PySide6.QtCore import Qt, QSize
from subwindows import testwindow, sidebar
from constants import PanelType

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

# --- Tiling Manager --- #
class PanelRegistry:
    panels = {
        PanelType.TEST_WINDOW: {
            "title": "Test Window",
            "widget": testwindow.TestWindow,
            "minimum_size": QSize(250, 300),
            "maximum_size": QSize(2000, constants.MAX_SIZE),
        },
        PanelType.SIDEBAR: {
            "title": "Sidebar",
            "widget": sidebar.SidebarWindow,
            "minimum_size": QSize(350, 300),
            "maximum_size": QSize(350, constants.MAX_SIZE),
        },
    }

    @staticmethod
    def create(node: PanelNode, window_manager):
        data = PanelRegistry.panels[node.panel_type]
        panel = data["widget"](data["title"])

        panel.setMinimumSize(data["minimum_size"])
        panel.setMaximumSize(data["maximum_size"])

        panel.type_changed.connect(
            lambda new_type: window_manager.change_panel_type(node, new_type)
        )

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

        self.widget_tree = self.build(self.root)

        self.layout.addWidget(self.widget_tree)

        self.refresh_layout()

    def refresh_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.widget_tree = self.build(self.root)
        self.layout.addWidget(self.widget_tree)

    def build(self, node):
        if isinstance(node, PanelNode):
            return PanelRegistry.create(node, self)

        orientation = (
            Qt.Horizontal
            if node.direction == SplitDirection.HORIZONTAL
            else Qt.Vertical
        )

        splitter = QSplitter(orientation)
        splitter.setChildrenCollapsible(False)

        splitter.addWidget(self.build(node.first))
        splitter.addWidget(self.build(node.second))

        return splitter

    def change_panel_type(self, node: PanelNode, new_type: PanelType):
        if node.panel_type == new_type:
            return

        node.panel_type = new_type
        self.refresh_layout()
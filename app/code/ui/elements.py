from PySide6.QtWidgets import QListWidget, QStackedWidget, QListWidgetItem, QLabel, QWidget, QHBoxLayout, QStyledItemDelegate
from PySide6.QtCore import Qt, QRectF, QSize
from PySide6.QtGui import QPainter

class VerticalTabSection(QWidget):
    def __init__(self, items: dict, default_index: int, parent=None):
        super().__init__(parent)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.tab_selector = QListWidget()
        self.tab_selector.setFixedWidth(80)
        self.tab_selector.setObjectName("SidebarTabSelector")

        self.panel_stack = QStackedWidget()
        self.pages = items

        for tab_name, widget_page in self.pages.items():
            item = QListWidgetItem(tab_name)
            item.setTextAlignment(Qt.AlignCenter)
            self.tab_selector.addItem(item)
            self.panel_stack.addWidget(widget_page)

        self.tab_selector.currentRowChanged.connect(self.panel_stack.setCurrentIndex)

        if 0 <= default_index < len(self.pages):
            self.tab_selector.setCurrentRow(default_index)

        # --- Connect Tab Switching --- #
        self.tab_selector.currentRowChanged.connect(self.panel_stack.setCurrentIndex)
        self.tab_selector.setCurrentRow(default_index)

        # --- Add to Layout --- #
        self.main_layout.addWidget(self.tab_selector)
        self.main_layout.addWidget(self.panel_stack, stretch=1)
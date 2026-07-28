from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QStackedWidget, QLabel, QToolButton, QButtonGroup, QFrame
)
from PySide6.QtCore import Qt, QSize
from subwindow import SubWindow
from ui import elements

class SidebarWindow(SubWindow):
    def __init__(self, title):
        super().__init__(title)

        self.toolbar_tabs = elements.HorizontalTabSection(
            items={
                "Select": QLabel("Song Settings"),
                "Draw": QLabel("Output Settings"),
                "Erase": QLabel("Track Inspector"),
            },
            default_index=0
        )

        self.main_tabs = elements.VerticalTabSection(
            items={
                "Song": QLabel("Song Settings"),
                "Output": QLabel("Output Settings"),
                "Track": QLabel("Track Inspector"),
                "Effects": QLabel("FX Chain"),
            },
            default_index=0
        )

        # --- Assemble Layout --- #
        self.content_layout.addWidget(self.toolbar_tabs, stretch=0)
        self.content_layout.addWidget(self.main_tabs, stretch=1)
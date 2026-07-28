from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QStackedWidget, QLabel, QToolButton, QButtonGroup, QFrame
)
from PySide6.QtCore import Qt, QSize
from subwindow import SubWindow
import ui.elements

class SidebarWindow(SubWindow):
    def __init__(self, title):
        super().__init__(title)

        self.tool_bar = QWidget()
        tool_layout = QHBoxLayout(self.tool_bar)
        tool_layout.setContentsMargins(4, 4, 4, 4)
        tool_layout.setSpacing(4)

        self.tool_group = QButtonGroup(self)
        self.tool_group.setExclusive(True)

        tools = [("Select", "pointer"), ("Draw", "pencil"), ("Erase", "eraser")]
        for tool_name, icon_name in tools:
            btn = QToolButton()
            btn.setText(tool_name)
            btn.setCheckable(True)
            btn.setToolTip(f"{tool_name} Tool")
            # btn.setIcon(QIcon(f".../{icon_name}.png")) # Uncomment when assets are ready

            self.tool_group.addButton(btn)
            tool_layout.addWidget(btn)

        if self.tool_group.buttons():
            self.tool_group.buttons()[0].setChecked(True)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)

        self.tabs = ui.elements.VerticalTabSection(
            items={
                "Song": QLabel("Song Settings"),
                "Output": QLabel("Output Settings"),
                "Track": QLabel("Track Inspector"),
                "Effects": QLabel("FX Chain"),
            },
            default_index=0
        )

        # --- Assemble Layout --- #
        self.content_layout.addWidget(self.tool_bar)
        self.content_layout.addWidget(divider)
        self.content_layout.addWidget(self.tabs, stretch=1)
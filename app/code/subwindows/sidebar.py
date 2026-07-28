from PySide6.QtWidgets import QLabel
from subwindow import SubWindow

class SidebarWindow(SubWindow):
    def __init__(self, title):
        super().__init__(title)

        label = QLabel("WaveLength Sidebar :o")
        self.content_layout.addWidget(label)
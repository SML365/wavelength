from PySide6.QtWidgets import QLabel
from subwindow import SubWindow

class TestWindow(SubWindow):
    def __init__(self, title):
        super().__init__(title)

        label = QLabel("Timeline")
        self.content_layout.addWidget(label)
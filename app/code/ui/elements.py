from PySide6.QtWidgets import QListWidget, QStackedWidget, QListWidgetItem, QLabel, QWidget, QHBoxLayout, QStyledItemDelegate, QStyle
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPainter

class VerticalTextDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        opt = option
        opt.text = ""

        option.widget.style().drawControl(
            QStyle.CE_ItemViewItem,
            opt,
            painter,
            option.widget
        )

        painter.save()
        painter.translate(option.rect.center())
        painter.rotate(-90)
        text = index.data(Qt.DisplayRole)
        if text:
            rect = QRect(-option.rect.height() // 2, -option.rect.width() // 2, 
                         option.rect.height(), option.rect.width())
            painter.drawText(rect, Qt.AlignCenter, text)
            
        painter.restore()

class VerticalTabSection(QWidget):
    def __init__(self, items: dict, default_index: int, parent=None):
        super().__init__(parent)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.tab_selector = QListWidget()
        self.tab_selector.setFixedWidth(30)
        self.tab_selector.setObjectName("SidebarTabSelector")

        self.tab_selector.setItemDelegate(VerticalTextDelegate(self.tab_selector))

        self.panel_stack = QStackedWidget()
        self.pages = items

        for tab_name, widget_page in self.pages.items():
            item = QListWidgetItem(tab_name)
            item.setTextAlignment(Qt.AlignCenter)
            item.setSizeHint(QSize(28, 60))
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
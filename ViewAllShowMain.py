import json
import os.path
from cProfile import label

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt6.QtWidgets import QLabel, QVBoxLayout

from ViewAll.view_all_core import ViewAllShow, base_path, ViewContent


class ViewAllShowMain(ViewContent):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.label = QLabel('将文件拖入此处', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet('color: white;')
        self.label.hide()
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            self.set_background_color(255, 255, 255, 0.1)
            self.label.show()
            event.accept()

    def dropEvent(self, event: QDropEvent):
        self.set_background_color(255, 255, 255, 0)
        self.label.hide()
        self.parent.dropEvent(event)

    def dragLeaveEvent(self, a0):
        self.set_background_color(255, 255, 255, 0)
        self.label.hide()




if __name__ == '__main__':
    show = ViewAllShow()
    main = ViewAllShowMain(show)
    show.set_content(main)


    show.run()



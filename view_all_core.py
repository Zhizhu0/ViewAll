import sys
import warnings

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QFileDialog


class ViewAllShow(QMainWindow):
    def __init__(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict.*")
        self.args = sys.argv
        self.app = QApplication(self.args)
        super().__init__()
        # 设置接受拖动应用
        self.setAcceptDrops(True)
        # 设置窗口标题
        self.base_title = "ViewAll"
        self.title = ''
        # 创建菜单栏
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        # 创建文件菜单
        self.file_menu = QMenu("文件", self)
        menubar.addMenu(self.file_menu)

        # 添加打开菜单项
        self.open_action = QAction("打开", self)
        self.open_action.triggered.connect(self.open_file)
        self.file_menu.addAction(self.open_action)


    def run(self):
        self.show()
        self.app.exec()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                print(url)

    def set_title(self, title):
        self.title = title
        self.setWindowTitle(self.base_title + ' - ' + self.title)

    @pyqtSlot()
    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            for file in selected_files:
                print(f"打开的文件：{file}")




if __name__ == '__main__':
    ViewAllShow().run()

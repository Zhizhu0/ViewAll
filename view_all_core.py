import sys
import warnings

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPainter, QBrush, QColor, \
    QMouseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget


# 自定义标题栏
class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: #ffffff;"
                           "color: #ffffff;"
                           "width: 100%;")
        self.mouse_press_pos = None
        self.mouse_press_d = None

        # # 创建标题标签
        # self.title_label = QLabel("Custom Title Bar", self)
        # self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #
        # # 创建最小化按钮
        # self.minimize_button = QPushButton(self)
        # # self.minimize_button.setIcon(QIcon("minimize_icon.png"))  # 替换为实际的图标路径
        # self.minimize_button.clicked.connect(self.parent.showMinimized)
        #
        # # 创建最大化/还原按钮
        # self.maximize_button = QPushButton(self)
        # # self.maximize_button.setIcon(QIcon("maximize_icon.png"))  # 替换为实际的图标路径
        # self.maximize_button.clicked.connect(self.toggleMaximize)
        #
        # # 创建关闭按钮
        # self.close_button = QPushButton(self)
        # # self.close_button.setIcon(QIcon("close_icon.png"))  # 替换为实际的图标路径
        # self.close_button.setStyleSheet("background-color: #ff0000; color: #ffffff;")
        # self.close_button.clicked.connect(self.parent.close)

        # 创建布局并添加控件
        # layout = QHBoxLayout(self)
        # layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        # layout.setContentsMargins(0, 0, 0, 0)

    # def toggleMaximize(self):
    #     if self.parent.isMaximized():
    #         self.parent.showNormal()
    #     else:
    #         self.parent.showMaximized()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_press_pos = event.globalPosition()
            self.mouse_press_d = event.pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.mouse_press_pos = event.globalPosition()
            self.parent.move(int(self.mouse_press_pos.x() - self.mouse_press_d.x()),
                             int(self.mouse_press_pos.y() - self.mouse_press_d.y()))
            event.accept()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setFixedWidth(self.parent.width())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setOpacity(0.1)
        painter.drawRoundedRect(self.rect(), 10, 10)

class ViewAllShow(QMainWindow):
    def __init__(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict.*")
        self.args = sys.argv
        self.app = QApplication(self.args)
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("border: 2px solid #000000;"
                           "border-radius: 10px;")
        self.title_bar = CustomTitleBar(self)

        # 设置接受拖动应用
        self.setAcceptDrops(True)
        # 设置窗口标题
        self.base_title = "ViewAll"
        self.title = ''
        # 创建菜单栏
        # menubar = QMenuBar(self)
        # self.setMenuBar(menubar)

        # 创建文件菜单
        # self.file_menu = QMenu("文件", self)
        # menubar.addMenu(self.file_menu)

        # 添加打开菜单项
        # self.open_action = QAction("打开", self)
        # self.open_action.triggered.connect(self.open_file)
        # self.file_menu.addAction(self.open_action)


    def run(self):
        self.show()
        self.app.exec()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if self.pre_drop_event(url.toString()):
                    return
                print(url.toString())

    def pre_drop_event(self, url):
        return False

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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(34, 35, 33)))
        painter.drawRoundedRect(self.rect(), 10, 10)




if __name__ == '__main__':
    ViewAllShow().run()

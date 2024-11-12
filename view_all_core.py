import sys
import warnings

from PyQt6.QtCore import pyqtSlot, Qt, QSize
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPainter, QBrush, QColor, \
    QMouseEvent, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QHBoxLayout, QLabel, QPushButton

def get_path(request):
    if getattr(sys, 'frozen', False):
        # 打包后的可执行文件
        resources_path = sys._MEIPASS + "/" # type: ignore
    else:
        # 开发环境中
        resources_path = "./"
    return resources_path + request

# 自定义标题栏
class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(50)
        self.mouse_press_pos = None
        self.mouse_press_d = None

        # 创建布局并添加控件
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        left_layout = QHBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(left_layout)

        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(center_layout)

        right_layout = QHBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(right_layout)

        self.title_label = QLabel(self)
        self.title_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.title_label.setText('ViewAll')
        center_layout.addWidget(self.title_label)

        # 创建最小化按钮
        self.minimize_button = QPushButton(self)
        self.minimize_button.setIcon(QIcon(get_path('icons/minimize.png')))
        self.minimize_button.setIconSize(QSize(10, 10))
        self.minimize_button.setStyleSheet("""
                                            QPushButton {
                                                color: #ffffff;
                                                width: 50px;
                                                height: 50px;
                                                margin: 0px;
                                                border: none;
                                            }
                                            QPushButton:hover {
                                                background-color: rgb(55, 55, 55);
                                            }
                                        """)
        # self.minimize_button.clicked.connect(self.parent.showMinimized)
        right_layout.addWidget(self.minimize_button)

        # 创建最大化/还原按钮
        self.maximize_button = QPushButton(self)
        self.maximize_button.setIcon(QIcon(get_path('icons/maximize.png')))
        self.maximize_button.setIconSize(QSize(10, 10))
        self.maximize_button.setStyleSheet("""
                                            QPushButton {
                                                color: #ffffff;
                                                width: 50px;
                                                height: 50px;
                                                margin: 0px;
                                                border: none;
                                            }
                                            QPushButton:hover {
                                                background-color: rgb(55, 55, 55);
                                            }
                                        """)
        self.maximize_button.clicked.connect(self.toggle_maximize) # type: ignore
        right_layout.addWidget(self.maximize_button)

        # 创建关闭按钮
        self.close_button = QPushButton(self)
        self.close_button.setIcon(QIcon(get_path('icons/close.png')))
        self.close_button.setIconSize(QSize(10, 10))
        self.close_button.setStyleSheet("""
                                            QPushButton {
                                                color: #ffffff;
                                                width: 50px;
                                                height: 50px;
                                                margin: 0px;
                                                border-top-right-radius: 10px;
                                            }
                                            QPushButton:hover {
                                                background-color: #ff0000;
                                            }
                                        """)
        right_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.parent.close) # type: ignore
        left_layout.addWidget(QPushButton("A"), 0, Qt.AlignmentFlag.AlignCenter)

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
        self.setFixedWidth(self.parent.width())

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
        # self.setStyleSheet("border: 2px solid #000000;"
        #                    "border-radius: 10px;")
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
        self.title_bar.title_label.setText(self.base_title + ' - ' + self.title)

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

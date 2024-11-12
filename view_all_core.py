import sys
import warnings

from PyQt6.QtCore import pyqtSlot, Qt, QSize, QPropertyAnimation, QEvent
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPainter, QBrush, QColor, \
    QMouseEvent, QIcon, QGuiApplication, QEnterEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QHBoxLayout, QLabel, QPushButton

from ViewAllQSS import close_btn_normal, close_btn_maximize, important_btn


def get_path(request):
    if getattr(sys, 'frozen', False):
        # 打包后的可执行文件
        resources_path = sys._MEIPASS + "/"  # type: ignore
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
        self.minimize_button.setStyleSheet(important_btn)
        self.minimize_button.clicked.connect(self.parent.showMinimized)  # type: ignore
        right_layout.addWidget(self.minimize_button)

        # 创建最大化/还原按钮
        self.maximize_button = QPushButton(self)
        self.maximize_button.setIcon(QIcon(get_path('icons/maximize.png')))
        self.maximize_button.setIconSize(QSize(10, 10))
        self.maximize_button.setStyleSheet(important_btn)
        self.maximize_button.clicked.connect(self.toggle_maximize)  # type: ignore
        right_layout.addWidget(self.maximize_button)

        # 创建关闭按钮
        self.close_button = QPushButton(self)
        self.close_button.setIcon(QIcon(get_path('icons/close.png')))
        self.close_button.setIconSize(QSize(10, 10))
        self.close_button.setStyleSheet(close_btn_normal)
        right_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.parent.close)  # type: ignore
        left_layout.addWidget(QPushButton("A"), 0, Qt.AlignmentFlag.AlignCenter)

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.close_button.setStyleSheet(close_btn_normal)
        else:
            self.parent.showMaximized()
            self.close_button.setStyleSheet(close_btn_maximize)
        self.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_press_pos = event.globalPosition()
            self.mouse_press_d = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.mouse_press_pos and self.mouse_press_d:
            self.mouse_press_pos = event.globalPosition()
            self.parent.move(int(self.mouse_press_pos.x() - self.mouse_press_d.x()),
                             int(self.mouse_press_pos.y() - self.mouse_press_d.y()))
            self.close_button.setStyleSheet(close_btn_normal)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_press_pos = None
            self.mouse_press_d = None

    def enterEvent(self, event: QEnterEvent):
        self.parent.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()
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
        if self.parent.isMaximized():
            painter.drawRect(self.rect())
        else:
            painter.drawRoundedRect(self.rect(), 10, 10)


class ViewAllShow(QMainWindow):
    def __init__(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict.*")
        self.args = sys.argv
        self.app = QApplication(self.args)
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.animation = None
        self.side = 10
        self.min_width = 400
        self.min_height = 300

        self.cur_x = 0
        self.cur_y = 0
        self.pre_width = 0
        self.pre_height = 0
        self.left_drag = False
        self.right_drag = False
        self.bottom_drag = False
        self.left_bottom_drag = False
        self.right_bottom_drag = False
        self.last_geometry = self.geometry()

        self.title_bar = CustomTitleBar(self)
        self.setMouseTracking(True)
        self.installEventFilter(self)

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

    def eventFilter(self, obj, event):
        if isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseMove:
            self.handle_mouse_move(event)
        return super(ViewAllShow, self).eventFilter(obj, event)

    def handle_mouse_move(self, event: QMouseEvent):
        if self.isMaximized() or not event.buttons() == Qt.MouseButton.NoButton:
            return
        window_width = self.geometry().width()
        window_height = self.geometry().height()
        x = event.pos().x()
        y = event.pos().y()
        if x < self.side and y > window_height - self.side:
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif y > window_height - self.side and x > window_width - self.side:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif x < self.side:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif y > window_height - self.side:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif x > window_width - self.side:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self.pre_width = self.geometry().width()
            self.pre_height = self.geometry().height()
            self.last_geometry = self.geometry()
            self.cur_x = event.globalPosition().x()
            self.cur_y = event.globalPosition().y()
            x = pos.x()
            y = pos.y()
            if x < self.side and y > self.pre_height - self.side:
                self.left_bottom_drag = True
            elif y > self.pre_height - self.side and x > self.pre_width - self.side:
                self.right_bottom_drag = True
            elif x < self.side:
                self.left_drag = True
            elif y > self.pre_height - self.side:
                self.bottom_drag = True
            elif x > self.pre_width - self.side:
                self.right_drag = True

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_drag = False
            self.right_drag = False
            self.bottom_drag = False
            self.left_bottom_drag = False
            self.right_bottom_drag = False

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            if self.left_drag:
                self.setGeometry(min(int(self.last_geometry.x() + event.globalPosition().x() - self.cur_x),
                                     self.last_geometry.x() + self.last_geometry.width() - self.min_width),
                                 int(self.last_geometry.y()),
                                 max(int(self.pre_width - event.globalPosition().x() + self.cur_x),
                                     self.min_width),
                                 int(self.pre_height))
            if self.right_drag:
                self.resize(max(int(event.globalPosition().x() - self.cur_x + self.pre_width), self.min_width), int(self.pre_height))
            if self.bottom_drag:
                self.resize(int(self.pre_width), max(int(event.globalPosition().y() - self.cur_y + self.pre_height), self.min_height))
            if self.left_bottom_drag:
                self.setGeometry(min(int(self.last_geometry.x() + event.globalPosition().x() - self.cur_x),
                                     self.last_geometry.x() + self.last_geometry.width() - self.min_width),
                                 int(self.last_geometry.y()),
                                 max(int(self.pre_width - event.globalPosition().x() + self.cur_x),
                                     self.min_width),
                                 max(int(self.pre_height + event.globalPosition().y() - self.cur_y),
                                     self.min_height))
            if self.right_bottom_drag:
                self.resize(max(int(event.globalPosition().x() - self.cur_x + self.pre_width), self.min_width),
                            max(int(event.globalPosition().y() - self.cur_y + self.pre_height), self.min_height))
            self.title_bar.setFixedWidth(self.geometry().width())


    def set_title(self, title):
        self.title = title
        self.setWindowTitle(self.base_title + ' - ' + self.title)
        self.title_bar.title_label.setText(self.base_title + ' - ' + self.title)

    def resize_animation(self, start_rect, end_rect, finish_func=None):
        if self.animation:
            self.animation.stop()
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(100)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.valueChanged.connect(lambda x: self.title_bar.setFixedWidth(x.width()))  # type: ignore
        self.animation.start()
        if finish_func:
            self.animation.finished.connect(finish_func) # type: ignore

    def showMaximized(self):
        screen = QGuiApplication.primaryScreen()
        self.last_geometry = self.geometry()
        if screen:
            # 获取屏幕的可用几何形状
            screen_rect = screen.availableGeometry()
            self.resize_animation(self.geometry(), screen_rect, super().showMaximized)
        else:
            super().showMaximized()

    def showNormal(self):
        self.resize_animation(self.geometry(), self.last_geometry, super().showNormal)

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
        if self.isMaximized():
            painter.drawRect(self.rect())
        else:
            painter.drawRoundedRect(self.rect(), 10, 10)


if __name__ == '__main__':
    ViewAllShow().run()

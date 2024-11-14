import json
import os.path
import sys
import warnings
import logging
from logging.handlers import TimedRotatingFileHandler

from PyQt6.QtCore import pyqtSlot, Qt, QSize, QPropertyAnimation, QEvent, QRect, QPoint
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPainter, QBrush, QColor, \
    QMouseEvent, QIcon, QGuiApplication, QEnterEvent, QHoverEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QHBoxLayout, QLabel, QPushButton, \
    QToolButton

from ViewAll.ViewAllQSS import close_btn_normal, close_btn_maximize, important_btn, view_tool_btn

dev_path = './'
base_path = './'
if getattr(sys, 'frozen', False):
    # 打包后的可执行文件
    base_path = os.path.dirname(sys.executable)
view_config_filename = 'view_config.json'
view_config = {
    'x': 0,
    'y': 0,
    'width': 500,
    'height': 300,
}
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_dir = os.path.join(base_path, 'log')
log_format = '%(asctime)s - %(levelname)s - %(message)s'

if not os.path.exists(log_dir):
    os.mkdir(log_dir)
file_handler = TimedRotatingFileHandler(os.path.join(log_dir, 'view_all.log'), when='D', interval=1, backupCount=10)
file_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(file_handler)


warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict.*")
view_config_path = os.path.join(base_path, view_config_filename)
if os.path.exists(view_config_path):
    with open(view_config_path, 'r') as f:
        try:
            json_data = json.load(f)
            view_config = json_data
            logging.info('载入JSON数据成功')
        except json.decoder.JSONDecodeError:
            logging.warning('载入JSON数据失败，已使用默认设置')

def get_path(request):
    if getattr(sys, 'frozen', False):
        # 打包后的可执行文件
        resources_path = sys._MEIPASS + "/"
    else:
        # 开发环境中
        resources_path = dev_path
    res = resources_path + request
    logging.debug(f'获取资源路径：{res}')
    return res


# 自定义标题栏
class ViewTitleBar(QWidget):
    def __init__(self, parent):
        logging.debug('初始化ViewTitleBar开始')
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(50)

        # 创建布局并添加控件
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.left_layout = QHBoxLayout()
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.left_layout)

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
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        right_layout.addWidget(self.minimize_button)

        # 创建最大化/还原按钮
        self.maximize_button = QPushButton(self)
        self.maximize_button.setIcon(QIcon(get_path('icons/maximize.png')))
        self.maximize_button.setIconSize(QSize(10, 10))
        self.maximize_button.setStyleSheet(important_btn)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        right_layout.addWidget(self.maximize_button)

        # 创建关闭按钮
        self.close_button = QPushButton(self)
        self.close_button.setIcon(QIcon(get_path('icons/close.png')))
        self.close_button.setIconSize(QSize(10, 10))
        self.close_button.setStyleSheet(close_btn_normal)
        right_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.parent.close)

        logging.debug('初始化ViewTitleBar结束')

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.close_button.setStyleSheet(close_btn_normal)
        else:
            self.parent.showMaximized()
            self.close_button.setStyleSheet(close_btn_maximize)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()
            event.accept()


    def paintEvent(self, event):
        logging.debug('绘制标题栏')
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.setOpacity(0.1)
        if self.parent.isMaximized():
            painter.drawRect(self.rect())
            logging.debug('正在重绘标题栏: 全屏模式')
        else:
            painter.drawRoundedRect(self.rect(), 10, 10)
            logging.debug('正在重绘标题栏: 窗口模式')


# 按钮
class ViewToolBtn(QPushButton):
    def __init__(self, parent, icon=None, tooltip=''):
        super().__init__(parent)
        self.setStyleSheet(view_tool_btn)
        self.setIconSize(QSize(20, 20))
        if icon:
            self.setIcon(QIcon(icon))
        if tooltip:
            self.setToolTip(tooltip)

# 主要内容
class ViewContent(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.margin = 20
        self.r = 255
        self.g = 255
        self.b = 255
        self.a = 0

    def set_background_color(self, r, g, b, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(self.r, self.g, self.b)))
        painter.setOpacity(self.a)
        if self.parent.isMaximized():
            painter.drawRect(self.rect())
        else:
            painter.drawRoundedRect(self.rect(), 10, 10)

class ViewAllShow(QMainWindow):
    def __init__(self):
        logging.debug('初始化ViewAllShow开始')
        self.app = QApplication([])
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.animation = None
        self.side = 10
        self.min_width = 400
        self.min_height = 300

        self.title_bar_height = 50
        self.mouse_press_pos = None
        self.mouse_press_d = None

        self.cur_x = 0
        self.cur_y = 0
        self.pre_width = 0
        self.pre_height = 0
        self.top_drag = False
        self.left_drag = False
        self.right_drag = False
        self.bottom_drag = False
        self.left_bottom_drag = False
        self.right_bottom_drag = False
        self.move_drag = False
        self.last_geometry = self.geometry()

        self.setGeometry(view_config['x'], view_config['y'], view_config['width'], view_config['height'])

        self.title_bar = ViewTitleBar(self)
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.content = None

        # 设置接受拖动应用
        self.setAcceptDrops(True)
        # 设置窗口标题
        self.base_title = "ViewAll"
        self.title = ''

        # 打开文件按钮
        self.open_btn = ViewToolBtn(self, get_path('icons/open_file.png'), '打开')
        self.title_bar.left_layout.addWidget(self.open_btn)
        self.open_btn.clicked.connect(self.open_file)

        # 设置按钮
        self.setting_btn = ViewToolBtn(self, get_path('icons/setting.png'), '设置')
        self.title_bar.left_layout.addWidget(self.setting_btn)
        # self.setting_btn.clicked.connect(self.open_file)

        logging.debug('初始化ViewAllShow结束')


    def run(self):
        self.show()
        self.app.exec()
        logging.debug('程序执行结束')

    def close(self):
        logging.debug('执行主窗口close代码')
        geometry = self.geometry()
        view_config['x'] = geometry.x()
        view_config['y'] = geometry.y()
        view_config['width'] = geometry.width()
        view_config['height'] = geometry.height()
        with open(os.path.join(base_path, view_config_filename), 'w') as write_file:
            write_file.write(json.dumps(view_config))
        super().close()

    def set_content(self, content):
        self.content = content
        self.after_paint()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if self.pre_drop_event(url.toString()):
                    return
                logging.info(f'拖入文件：{url.toString()}')
                print(url.toString())

    def pre_drop_event(self, url):
        return False

    def eventFilter(self, obj, event):
        if isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseMove\
                or isinstance(event, QHoverEvent) and event.type() == QEvent.Type.HoverMove:
            self.handle_mouse_move(event)
        return super(ViewAllShow, self).eventFilter(obj, event)

    def handle_mouse_move(self, event: QMouseEvent | QHoverEvent):
        if self.isMaximized() or not event.buttons() == Qt.MouseButton.NoButton:
            return
        window_width = self.geometry().width()
        window_height = self.geometry().height()
        x = event.position().x()
        y = event.position().y()
        if x < self.side and y > window_height - self.side:
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif y > window_height - self.side and x > window_width - self.side:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif y < self.side:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
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
            pre_width = self.geometry().width()
            pre_height = self.geometry().height()
            if not self.isMaximized():
                self.last_geometry = self.geometry()
            self.cur_x = event.globalPosition().x()
            self.cur_y = event.globalPosition().y()
            x = pos.x()
            y = pos.y()
            if x < self.side and y > pre_height - self.side:
                self.left_bottom_drag = True
            elif y > pre_height - self.side and x > pre_width - self.side:
                self.right_bottom_drag = True
            elif y < self.side:
                self.top_drag = True
            elif x < self.side:
                self.left_drag = True
            elif y > pre_height - self.side:
                self.bottom_drag = True
            elif x > pre_width - self.side:
                self.right_drag = True
            elif y < self.title_bar_height:
                self.mouse_press_pos = event.globalPosition()
                self.mouse_press_d = event.pos()
                self.move_drag = True

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.top_drag = False
            self.left_drag = False
            self.right_drag = False
            self.bottom_drag = False
            self.left_bottom_drag = False
            self.right_bottom_drag = False
            self.move_drag = False

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            pre_width = self.last_geometry.width()
            pre_height = self.last_geometry.height()
            if self.top_drag and not self.isMaximized():
                self.setGeometry(int(self.last_geometry.x()),
                                 min(int(self.last_geometry.y() + event.globalPosition().y() - self.cur_y),
                                     self.last_geometry.y() + self.last_geometry.height() - self.min_height),
                                 int(pre_width),
                                 max(int(pre_height - event.globalPosition().y() + self.cur_y),
                                     self.min_height))
            if self.left_drag and not self.isMaximized():
                self.setGeometry(min(int(self.last_geometry.x() + event.globalPosition().x() - self.cur_x),
                                     self.last_geometry.x() + self.last_geometry.width() - self.min_width),
                                 int(self.last_geometry.y()),
                                 max(int(pre_width - event.globalPosition().x() + self.cur_x),
                                     self.min_width),
                                 int(pre_height))
            if self.right_drag and not self.isMaximized():
                self.resize(max(int(event.globalPosition().x() - self.cur_x + pre_width), self.min_width),
                            int(pre_height))
            if self.bottom_drag and not self.isMaximized():
                self.resize(int(pre_width),
                            max(int(event.globalPosition().y() - self.cur_y + pre_height), self.min_height))
            if self.left_bottom_drag and not self.isMaximized():
                self.setGeometry(min(int(self.last_geometry.x() + event.globalPosition().x() - self.cur_x),
                                     self.last_geometry.x() + self.last_geometry.width() - self.min_width),
                                 int(self.last_geometry.y()),
                                 max(int(pre_width - event.globalPosition().x() + self.cur_x),
                                     self.min_width),
                                 max(int(pre_height + event.globalPosition().y() - self.cur_y),
                                     self.min_height))
            if self.right_bottom_drag and not self.isMaximized():
                self.resize(max(int(event.globalPosition().x() - self.cur_x + pre_width), self.min_width),
                            max(int(event.globalPosition().y() - self.cur_y + pre_height), self.min_height))
            if self.move_drag and self.mouse_press_pos and self.mouse_press_d:
                if self.isMaximized():
                    self.cur_x = event.globalPosition().x()
                    self.cur_y = event.globalPosition().y()
                    self.setGeometry(int(self.cur_x - (self.last_geometry.width() / 2)), 0,
                                     int(self.last_geometry.width()), int(self.last_geometry.height()))
                    self.mouse_press_d = QPoint(int(self.last_geometry.width() / 2), self.mouse_press_d.y())
                    self.title_bar.close_button.setStyleSheet(close_btn_normal)
                else:
                    self.mouse_press_pos = event.globalPosition()
                    self.move(int(self.mouse_press_pos.x() - self.mouse_press_d.x()),
                                     int(self.mouse_press_pos.y() - self.mouse_press_d.y()))
                # self.showNormal(False)

    def set_title(self, title):
        self.title = title
        self.setWindowTitle(self.base_title + ' - ' + self.title)
        self.title_bar.title_label.setText(self.base_title + ' - ' + self.title)

    def resize_animation(self, start_rect, end_rect, finish_func=None):
        logging.debug('执行窗口变化动画')
        if self.animation:
            self.animation.stop()
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(100)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()
        if finish_func:
            self.animation.finished.connect(finish_func)

    def showMaximized(self):
        logging.debug('最大化窗口')
        screen = QGuiApplication.primaryScreen()
        self.last_geometry = self.geometry()
        if screen:
            # 获取屏幕的可用几何形状
            screen_rect = screen.availableGeometry()
            self.resize_animation(self.geometry(), screen_rect, super().showMaximized)
        else:
            super().showMaximized()

    def showNormal(self, need_animation=True):
        logging.debug('还原窗口')
        if need_animation:
            self.resize_animation(self.geometry(), self.last_geometry, super().showNormal)
        else:
            self.setGeometry(self.last_geometry)

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            for file in selected_files:
                logging.info(f'打开的文件：{file}')
                print(f"打开的文件：{file}")

    def after_paint(self):
        self.title_bar.setFixedWidth(self.geometry().width())
        self.title_bar.setFixedHeight(self.title_bar_height)

        if self.content:
            self.content.setFixedWidth(self.geometry().width() - 2 * self.content.margin)
            self.content.setFixedHeight(self.geometry().height() - self.title_bar_height - 2 * self.content.margin)
            self.content.move(self.content.margin, self.title_bar_height + self.content.margin)



    def paintEvent(self, event):
        logging.debug('主窗口绘制')
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(34, 35, 33)))
        if self.isMaximized():
            painter.drawRect(self.rect())
        else:
            painter.drawRoundedRect(self.rect(), 10, 10)
        self.after_paint()

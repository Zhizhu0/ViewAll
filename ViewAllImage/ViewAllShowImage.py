import logging

from PyQt6.QtCore import Qt, QEvent, QPropertyAnimation
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

import ViewAll
from ViewAll.view_all_core import ViewContent


class ViewAllShowImageBottom(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        logging.debug('初始化ViewAllShowImageBottom')



class ViewAllShowImage(ViewContent):
    def __init__(self, parent, url):
        super().__init__(parent)
        logging.debug('初始化ViewAllShowImage')

        self.parent.set_title('image')
        self.show()
        self.img_label = QLabel(self)
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(self)
        layout.addWidget(self.img_label)

        self.img = QPixmap(url)
        self.url = url
        self.scale = 1
        self.animation = QPropertyAnimation(self, b"img_scale")
        self.animation.setDuration(200)
        self.animation.valueChanged.connect(self.zoom)

        self.installEventFilter(self)
        self.show_img()

    def show_img(self):
        logging.debug(f'显示图片：{self.url}')

        if self.url:
            self.scale = 1
            self.img = QPixmap(self.url)
            self.img_label.setPixmap(self.img)
            self.parent.set_title('image ' + self.url.split('/')[-1])
            # self.image_label.setScaledContents(True)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            self.handle_mouse_wheel(event)
            return True
        return super().eventFilter(obj, event)

    def handle_mouse_wheel(self, event):
        logging.debug(f'接受到滚轮角度：{event.angleDelta().y()}')

        angle_delta = event.angleDelta()
        to_scale = self.scale + angle_delta.y() / 500 * self.scale
        self.zoom_animation(self.scale, to_scale)
        self.scale = to_scale

    def zoom(self, scale):
        logging.debug(f'改变图片大小, 当前scale值: {scale}')

        if self.img:
            new_width = int(self.img.width() * scale)
            new_height = int(self.img.height() * scale)
            new_pixmap = self.img.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)
            self.img_label.setPixmap(new_pixmap)

    def zoom_animation(self, start_scale, end_scale):
        logging.debug(f'执行图片变化动画, start_scale={start_scale}, end_scale={end_scale}')

        if self.animation:
            self.animation.stop()
        self.animation.setStartValue(start_scale)
        self.animation.setEndValue(end_scale)
        self.animation.start()

    def pre_drop_event(self, url):
        if url.startswith('file:///'):
            file = url[8:]
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.webp'):
                logging.info(f'切换为另一图片, url: {file}')

                self.url = file
                self.show_img()
                return True
        return False

    def paintEvent(self, event):
        super().paintEvent(event)


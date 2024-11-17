import logging

from PyQt6.QtCore import Qt, QEvent, QPropertyAnimation
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QSlider, QLineEdit

import ViewAll
from ViewAll.view_all_core import ViewContent


class ViewAllShowImage(ViewContent):
    def __init__(self, parent, url):
        super().__init__(parent)
        logging.debug('初始化ViewAllShowImage')

        self.parent.set_title('image')
        self.show()
        self.img_label = QLabel(self)
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.img_label)

        self.img = QPixmap(url)
        self.url = url
        self.scale = 1
        self.animation = QPropertyAnimation(self, b"img_scale")
        self.animation.setDuration(200)
        self.animation.valueChanged.connect(self.zoom)

        self.parent.bottom_bar_height = 50

        self.scale_label = QLineEdit()
        # 使用样式表设置QLineEdit的样式
        style_sheet = """
                    QLineEdit {
                        background-color: rgba(133, 133, 133, 0.1); /* 设置背景色为浅灰色 */
                        border-radius: 8px; /* 设置边框圆角半径 */
                        padding: 5px; /* 设置文本内容与边框的间距 */
                        font-size: 14px; /* 设置字体大小 */
                        color: #ffffff; /* 设置文本颜色 */
                    }
                    QLineEdit:hover {
                        background-color: rgba(133, 133, 133, 0.3);
                    }
                    QLineEdit:focus {
                        background-color: rgba(10, 11, 12, 0.2);
                    }
                """
        self.scale_label.setStyleSheet(style_sheet)
        self.scale_label.setFixedWidth(50)
        self.scale_label.setText('100%')
        self.scale_label.returnPressed.connect(self.scale_label_return_pressed)
        self.scale_label.editingFinished.connect(self.scale_label_editing_finished)
        self.bottom_right_widgets.append(self.scale_label)

        # 创建滑动条
        self.slider = QSlider()
        # 设置滑动条的方向为水平方向（也可以设置为垂直方向，使用Qt.Vertical）
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 800)
        self.slider.setValue(100)
        # 使用样式表设置滑动条样式
        style_sheet = """
                    QSlider::groove:horizontal {
                        height: 8px; /* 水平轨道高度 */
                        background: #ccc; /* 水平轨道颜色 */
                        border-radius: 4px;
                    }
                    QSlider::handle:horizontal {
                        background-color: #007bff; /* 滑块颜色 */
                        width: 12px; /* 滑块宽度 */
                        height: 12px; /* 滑块高度 */
                        border-radius: 6px;
                        margin: -4px 0; /* 调整滑块垂直方向位置 */
                    }
                    QSlider::handle:horizontal:hover {
                        background-color: #0047bb; /* 滑块颜色 */
                    }
                """
        self.slider.setStyleSheet(style_sheet)
        self.slider.setFixedWidth(200)
        self.slider.valueChanged.connect(self.change_slide)
        self.bottom_right_widgets.append(self.slider)

        self.installEventFilter(self)
        self.show_img()

    def show_img(self):
        logging.debug(f'显示图片：{self.url}')

        if self.url:
            self.scale = 1
            self.scale_label.setText('100%')
            self.slider.setValue(100)
            self.img = QPixmap(self.url)
            self.img_label.setPixmap(self.img)
            self.parent.set_title('image ' + self.url.split('/')[-1])
            # self.image_label.setScaledContents(True)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            self.handle_mouse_wheel(event)
            return True
        return super().eventFilter(obj, event)

    def change_zoom(self, to_scale):
        if to_scale > 8:
            to_scale = 8
        if to_scale < 0.01:
            to_scale = 0.01
        self.zoom_animation(self.scale, to_scale)
        self.scale = to_scale
        self.slider.blockSignals(True)
        self.scale_label.setText(f'{int(self.scale * 100)}%')
        self.slider.setValue(int(self.scale * 100))
        self.slider.blockSignals(False)

    def handle_mouse_wheel(self, event):
        logging.debug(f'接受到滚轮角度：{event.angleDelta().y()}')

        angle_delta = event.angleDelta()
        to_scale = self.scale + angle_delta.y() / 500 * self.scale
        self.change_zoom(to_scale)

    def scale_label_return_pressed(self):
        self.scale_label.clearFocus()

    def scale_label_editing_finished(self):
        text = self.scale_label.text()
        if text.endswith('%'):
            text = text[:-1]
        if text.isdigit() and 800 >= int(text) > 0:
            self.change_zoom(int(text) / 100)
            self.scale_label.setText(text + '%')
        else:
            self.change_zoom(1)
            self.scale_label.setText('100%')


    def change_slide(self, value):
        logging.debug(f'滑动条值改变, value = {value}')

        self.change_zoom(value / 100)

    def zoom(self, scale):
        logging.debug(f'改变图片大小, 当前scale值: {scale}')

        if self.img and scale is not None:
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

    def pre_close(self):
        return False



import logging

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

import ViewAll
from ViewAll.view_all_core import ViewContent


class ViewAllShowImage(ViewContent):
    def __init__(self, parent, url=None):
        super().__init__(parent)
        logging.debug('初始化ViewAllShowImage')

        self.parent.set_title('image')
        self.show()
        if url:
            img = QPixmap(url)
            img_label = QLabel(self)
            img_label.setPixmap(img)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout = QVBoxLayout(self)
            layout.addWidget(img_label)

        # self.img_url = ''
        # self.scale = 1
        # self.pixmap = None
        # self.set_title('image')
        # # self.setStyleSheet('background-color: black;color: white;')
        # # 创建一个 QLabel 组件来显示图片
        # self.image_label = QLabel(self)
        # # self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #
        # # 创建一个 QVBoxLayout 布局，并将 QLabel 添加到布局中
        # layout = QVBoxLayout()
        # layout.addWidget(self.image_label)
        #
        # # 创建一个 QWidget 作为主窗口的中心组件，并设置布局
        # central_widget = QWidget(self)
        # central_widget.setLayout(layout)
        # self.setCentralWidget(central_widget)
        # self.image_label.installEventFilter(self)
        # if len(self.args) > 1:
        #     self.img_url = self.args[1]
        #     self.show_img()

    # def show_img(self):
    #     if self.img_url:
    #         self.scale = 1
    #         self.pixmap = QPixmap(self.img_url)
    #         self.image_label.setPixmap(self.pixmap)
    #         # self.image_label.setScaledContents(True)
    #
    # def eventFilter(self, obj, event):
    #     # if obj == self.image_label and event.type() == QEvent.Type.Wheel:
    #     #     self.handle_mouse_wheel(event)
    #     #     return True
    #     return super().eventFilter(obj, event)
    #
    # def handle_mouse_wheel(self, event):
    #     # # 获取滚轮滚动的角度
    #     # print(event.angleDelta().y())
    #     # print(event.angleDelta().x())
    #     # # 获取物理设备
    #     # print(event.device().type())
    #     angle_delta = event.angleDelta()
    #     if angle_delta.y() > 0:
    #         # 滚轮向前滚动，放大图片
    #         self.zoom_in()
    #     else:
    #         # 滚轮向后滚动，缩小图片
    #         self.zoom_out()
    #
    # def zoom_in(self):
    #     # 放大图片
    #     if self.pixmap and self.scale < 8:
    #         self.scale += 0.1
    #         new_width = int(self.pixmap.width() * self.scale)
    #         new_height = int(self.pixmap.height() * self.scale)
    #         new_pixmap = self.pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)
    #         self.image_label.setPixmap(new_pixmap)
    #
    # def zoom_out(self):
    #     # 缩小图片
    #     if self.pixmap and self.scale > 0.1:
    #         self.scale -= 0.1
    #         new_width = int(self.pixmap.width() * self.scale)
    #         new_height = int(self.pixmap.height() * self.scale)
    #         new_pixmap = self.pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)
    #         self.image_label.setPixmap(new_pixmap)
    # def pre_drop_event(self, url):
    #     if url.startswith('file:///'):
    #         url = url[8:]
    #         if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg') or url.endswith('.webp'):
    #             self.img_url = url
    #             self.show_img()
    #             return True
    #     return False

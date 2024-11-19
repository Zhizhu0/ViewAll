import logging

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QLabel, QPushButton, QMenu, QFileDialog, QComboBox, QMessageBox
import chardet

from ViewAll.view_all_core import ViewContent, ViewToolBtn


class ViewAllShowText(ViewContent):
    def __init__(self, parent, url):
        super().__init__(parent)
        logging.debug('初始化ViewAllShowText')

        self.url = url
        self.text = ''
        self.encoding = 'UTF-8'
        self.parent.set_title('text')
        self.show()

        self.have_changed = False

        menu = QMenu(self)

        style_sheet = '''
                      QMenu {
                        background-color: rgb(17, 17, 16);
                        color: rgb(198, 189, 197);
                        padding: 5px;
                        border-radius: 6px;
                      }
                      QMenu::item {
                          padding: 5px 20px 5px 20px;
                          border: 1px solid transparent;
                          border-radius: 4px;
                      }
                      QMenu::item:selected {
                          background-color: rgb(47, 47, 46);
                      }
        '''
        menu.setStyleSheet(style_sheet)

        # 创建菜单项
        action1 = QAction('保存', self)
        action2 = QAction('另存为', self)

        # 将菜单项添加到菜单中
        menu.addAction(action1)
        menu.addAction(action2)

        # 连接菜单项的信号到槽函数
        action1.triggered.connect(self.save)
        action2.triggered.connect(self.save_as)

        self.save_btn = QPushButton()
        style_sheet = '''
                      QPushButton {
                          width: 50px;
                          height: 40px;
                          border-radius: 10px; /* 圆角 */
                          border-color: beige; /* 边框颜色 */
                      }
                      QPushButton:hover {
                          background-color: rgb(55, 55, 55); /* 鼠标悬停时的背景颜色 */
                      }
                      QPushButton:pressed {
                          background-color: rgb(22, 23, 21); /* 按钮按下时的背景颜色 */
                          border-style: inset; /* 按钮按下时的边框样式 */
                      }
        '''
        self.save_btn.setStyleSheet(style_sheet)
        self.save_btn.setIconSize(QSize(20, 20))
        self.save_btn.setIcon(QIcon('ViewAllText/icons/save.png'))
        self.save_btn.setMenu(menu)

        self.title_left_widgets.append(self.save_btn)

        self.parent.bottom_bar_height = 50

        self.text_edit = QTextEdit(self)
        style_sheet = '''
                         QTextEdit {
                            background-color: rgba(0, 0, 0, 0);
                            color: rgb(192, 194, 196);
                            border: none;
                         }
        '''

        self.text_edit.setStyleSheet(style_sheet)
        style_sheet = """
                        QScrollBar:vertical {
                            background: transparent;  /* 设置滚动条背景透明 */
                            width: 6px;
                            margin: 0px 0px 0px 0px;
                        }
                        QScrollBar::handle:vertical {
                            background: #888888;
                            min-height: 20px;
                            border-radius: 3px;
                        }
                        QScrollBar::handle:vertical:hover {
                            background: #989898;
                        }
                        QScrollBar::add-line:vertical {
                            background: transparent;
                            height: 0px;
                        }
                        QScrollBar::sub-line:vertical {
                            background: transparent;
                            height: 0px;
                        }
                        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                            background: transparent;
                        }
                        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                            background: transparent;
                        }
                        """
        self.text_edit.verticalScrollBar().setStyleSheet(style_sheet)
        self.text_edit.textChanged.connect(self.text_change)
        self.text_edit.cursorPositionChanged.connect(self.cursor_position_changed)

        self.encoding_label = QComboBox()
        self.encoding_label.addItem('UTF-8')
        self.encoding_label.addItem('ISO-8859-1')
        self.encoding_label.addItem('UTF-16')
        self.encoding_label.addItem('UTF-32')
        self.encoding_label.addItem('GBK')
        self.encoding_label.addItem('GB18030')
        self.encoding_label.addItem('ISO-2022-JP')
        self.encoding_label.addItem('Shift_JIS')
        self.encoding_label.addItem('EUC-JP')
        self.encoding_label.addItem('BIG5')
        self.encoding_label.addItem('ISO-8859-2')
        self.encoding_label.addItem('ISO-8859-3')
        self.encoding_label.addItem('ISO-8859-4')
        self.encoding_label.addItem('ISO-8859-5')
        self.encoding_label.addItem('ISO-8859-6')
        self.encoding_label.addItem('ISO-8859-7')
        self.encoding_label.addItem('ISO-8859-8')
        self.encoding_label.addItem('ISO-8859-9')
        self.encoding_label.addItem('ISO-8859-10')
        self.encoding_label.addItem('ISO-8859-13')
        self.encoding_label.addItem('ISO-8859-14')
        self.encoding_label.addItem('ISO-8859-15')
        self.encoding_label.addItem('ISO-8859-16')
        style_sheet = '''
                      QComboBox {
                        background-color: rgba(0, 0, 0, 0);
                        color: rgb(211, 210, 212);
                        width: 80px;
                        height: 40px;
                        border-radius: 6px;
                        margin-right: 20px;
                        font-size: 14px;
                      }
                      QComboBox::down-arrow {
                            image: none;
                            width: 0;
                            padding: 0;
                        }
                      QComboBox QListView {
                            background-color: rgb(23, 23, 24);
                            border: none;
                        }
                      QComboBox QListView::item {
                            background-color: rgb(34, 33, 35);
                            color: rgb(190, 189, 192);
                            border: 2px;
                        }
                        QComboBox QListView::item:hover {
                            background-color: rgb(43, 44, 45);
                            border: 2px;
                        }
                        QComboBox QScrollBar:vertical { 
                            width: 0px; 
                        }
        '''
        self.encoding_label.setStyleSheet(style_sheet)
        self.encoding_label.currentTextChanged.connect(self.on_combo_box_changed)

        self.bottom_right_widgets.append(self.encoding_label)

        self.cursor_label = QLabel()
        style_sheet = '''
                      QLabel {
                        color: rgb(211, 210, 212);
                        margin-left: 10px;
                        font-size: 14px;
                      }
        '''
        self.cursor_label.setStyleSheet(style_sheet)
        self.bottom_left_widgets.append(self.cursor_label)

        self.characters_count_label = QLabel()
        style_sheet = '''
                      QLabel {
                        color: rgb(211, 210, 212);
                        font-size: 14px;
                      }
        '''
        self.characters_count_label.setStyleSheet(style_sheet)
        self.bottom_left_widgets.append(self.characters_count_label)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text_edit)

        self.show_text()

    def save_as(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            # 如果用户选择了文件名，则保存文本到文件
            self.url = file_name
            self.save()

    def save(self):
        logging.info(f'保存文件，位置为{self.url}, 编码为{self.encoding}')
        with open(self.url, 'w', encoding=self.encoding) as file:
            text = self.text_edit.toPlainText()
            file.write(text)
        self.have_changed = False

    def show_confirmation_message(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("确认操作")
        msg_box.setText("您有未保存的更改，是否保存？")
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Cancel)

        msg_box.button(QMessageBox.StandardButton.Save).setText("保存")
        msg_box.button(QMessageBox.StandardButton.Discard).setText("不保存")
        msg_box.button(QMessageBox.StandardButton.Cancel).setText("取消")

        return msg_box.exec()

    def on_combo_box_changed(self):
        selected_item = self.encoding_label.currentText()
        logging.debug(f'切换为{selected_item} 编码格式')

        self.encoding = selected_item

    def show_text(self):
        if self.url:
            try:
                with open(self.url, 'r', encoding='utf-8') as f:
                    self.text = f.read()
            except UnicodeDecodeError:
                logging.info('使用utf-8读取文件失败，正在尝试其他编码')

                with open(self.url, 'rb') as f:
                    t = f.read(1024)
                    self.encoding = chardet.detect(t)['encoding']
                with open(self.url, 'r', encoding=self.encoding) as f:
                    self.text = f.read()
            self.text_edit.setText(self.text)
            self.encoding_label.setCurrentText(self.encoding)
            self.have_changed = False

    def text_change(self):
        logging.debug('text_changed')

        self.text = self.text_edit.toPlainText()
        self.characters_count_label.setText(str(len(self.text)))
        self.have_changed = True

    def cursor_position_changed(self):
        cursor = self.text_edit.textCursor()
        block = cursor.block()
        line = block.blockNumber() + 1
        col = cursor.positionInBlock() + 1
        self.cursor_label.setText(f'{line}:{col}')

        logging.debug(f'cursor_position_changed, line={line}, col={col}')

    def pre_drop_event(self, url):
        if url.startswith('file:///'):
            file = url[8:]
            if file.endswith('.txt'):
                logging.info(f'切换为另一文本, url: {file}')

                self.url = file
                self.show_text()
                return True
        return False

    def pre_close(self):
        if self.have_changed:
            ri = self.show_confirmation_message()
            if ri == QMessageBox.StandardButton.Save:
                self.save()
            if ri == QMessageBox.StandardButton.Cancel:
                return True
        return super().pre_close()

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout
import chardet

from ViewAll.view_all_core import ViewContent


class ViewAllShowText(ViewContent):
    def __init__(self, parent, url):
        super().__init__(parent)
        logging.debug('初始化ViewAllShowText')
        self.url = url
        self.text = ''
        with open(url, 'rb') as f:
            t = f.read()
            encoding = chardet.detect(t)['encoding']
        with open(url, 'r', encoding=encoding) as f:
            self.text = f.read()
        self.parent.set_title('text')
        self.show()
        self.text_edit = QTextEdit(self)
        style_sheet = '''
                         QTextEdit {
                            background-color: rgba(0, 0, 0, 0);
                            color: rgb(192, 194, 196);
                            border: none;
                         }
        '''
        self.text_edit.setStyleSheet(style_sheet)
        self.text_edit.setText(self.text)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.text_edit)
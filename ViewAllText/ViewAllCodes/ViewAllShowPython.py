import logging

from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont

from ViewAll.ViewAllText.ViewAllShowText import ViewAllShowText

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)
        self.highlightingRules = []

        # 关键字高亮
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda",
            "None", "nonlocal", "not", "or", "pass", "raise", "return",
            "True", "try", "while", "with", "yield"
        ]
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor('#CF8E6D'))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        for keyword in keywords:
            pattern = QRegularExpression(f"\\b{keyword}\\b")
            rule = (pattern, keyword_format)
            self.highlightingRules.append(rule)

        # 字符串高亮
        string_format = QTextCharFormat()
        string_format.setForeground(QColor('#6AAB73'))
        self.highlightingRules.append((QRegularExpression(r"\".*\""), string_format))
        self.highlightingRules.append((QRegularExpression(r"'.*'"), string_format))

        # 注释高亮
        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.GlobalColor.gray)
        self.highlightingRules.append((QRegularExpression(r"#[^\n]*"), comment_format))

        self_format = QTextCharFormat()
        self_format.setForeground(QColor(147, 82, 107))
        self.highlightingRules.append((QRegularExpression(r"\bself\b"), self_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            i = expression.globalMatch(text)
            while i.hasNext():
                match = i.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)



class ViewAllShowPython(ViewAllShowText):
    def __init__(self, parent, url):
        ViewAllShowText.__init__(self, parent, url)
        logging.debug('初始化ViewAllShowPython')

        self.highlighter = PythonHighlighter(self.text_edit.document())


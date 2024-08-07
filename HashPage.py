from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QLabel, QSpacerItem, QSizePolicy
from qfluentwidgets import VBoxLayout, TextEdit

import webbrowser

from widget.function import basicFunc


class HashPage:
    def __init__(self):
        self.widget = QWidget()
        self.widget.setObjectName("HashPage")
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.spacer = QSpacerItem(1000, 1000, hData=QSizePolicy.Maximum, vData=QSizePolicy.Maximum)
        self.run()

    def addTextLine(self, text: str, idName: str = None, alignment=Qt.AlignLeft):
        textLine = QLabel(text=text)
        if idName:
            textLine.setObjectName(idName)
        self.layout.addWidget(textLine, alignment=alignment)

    def run(self):
        self.addTextLine("哈希值校验工具", "Title")
        textEdit_tip = TextEdit(self.widget)
        textEdit_tip.setMarkdown(basicFunc.readFile("data\\hash_tip.md"))
        textEdit_tip.setEnabled(False)
        textEdit_tip.setMinimumHeight(120)
        self.layout.addWidget(textEdit_tip)

        self.layout.addSpacerItem(self.spacer)

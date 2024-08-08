from PySide2 import QtCore
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QLabel, QSpacerItem, QSizePolicy
from qfluentwidgets import VBoxLayout, TextEdit, TitleLabel, FluentLabelBase, BodyLabel, SingleDirectionScrollArea

import webbrowser

from widget.function import basicFunc


class HashPage:
    def __init__(self):
        self.widget = QWidget()
        self.widget.setObjectName("HashPage")
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.spacer = QSpacerItem(200, 200, hData=QSizePolicy.Expanding, vData=QSizePolicy.Expanding)

        self.scrollArea = SingleDirectionScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setObjectName("HashPage")
        self.scrollArea.setWidgetResizable(True)
        self.run()

    def addTextLine(self, text: str, labelType: str = "Body"):
        if labelType == "Title":
            label = TitleLabel()
        else:
            label = BodyLabel()
        label.setText(text)
        self.layout.addWidget(label)

    def run(self):
        self.addTextLine("哈希值校验工具", "Title")
        textEdit_tip = TextEdit(self.widget)
        textEdit_tip.setMarkdown(basicFunc.readFile("data\\hash_tip.md"))
        textEdit_tip.setEnabled(False)
        textEdit_tip.setMinimumHeight(120)
        self.layout.addWidget(textEdit_tip)

        self.layout.addSpacerItem(self.spacer)

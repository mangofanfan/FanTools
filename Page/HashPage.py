import logging

from PySide2 import QtCore
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QFrame, QWidget, QVBoxLayout, QBoxLayout
from qfluentwidgets import VBoxLayout, TextEdit, TitleLabel, BodyLabel, SingleDirectionScrollArea

from widget.function import basicFunc

logger = logging.getLogger("FanTools.HashPage")


class HashPage:
    def __init__(self):
        self.bodyWidget = QWidget()
        self.bodyWidget.setObjectName("HashPage")
        self._layout = QVBoxLayout()
        self.bodyWidget.setLayout(self._layout)
        self._layout.setContentsMargins(0, 5, 0, 0)

        self.widget = QFrame()
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)

        self.scrollArea = SingleDirectionScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setWidgetResizable(True)

        self.addTextLine("哈希值校验工具", "Title", self._layout)
        self._layout.addWidget(self.scrollArea)

        self.run()

        logger.debug("页面初始化完毕。")


    def addTextLine(self, text: str, labelType: str = "Body", layout: QBoxLayout = None):
        if labelType == "Title":
            label = TitleLabel()
            label.setAlignment(Qt.AlignCenter)
        else:
            label = BodyLabel()
        label.setText(text)
        label.setWordWrap(True)
        if layout:
            layout.addWidget(label)
        else:
            self.layout.addWidget(label)
        return None

    def run(self):
        textEdit_tip = TextEdit(self.widget)
        textEdit_tip.setMarkdown(basicFunc.readFile("/data/hash_tip.md"))
        textEdit_tip.setEnabled(False)
        textEdit_tip.setMinimumHeight(120)
        self.layout.addWidget(textEdit_tip)

        self.layout.addStretch()

import logging

from PySide2 import QtCore
from PySide2.QtWidgets import QFrame
from qfluentwidgets import VBoxLayout, TextEdit, TitleLabel, BodyLabel, SingleDirectionScrollArea

from widget.function import basicFunc

logger = logging.getLogger("FanTools.HashPage")


class HashPage:
    def __init__(self):
        self.widget = QFrame()
        self.widget.setObjectName("HashPage")
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)

        self.scrollArea = SingleDirectionScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setObjectName("HashPage")
        self.scrollArea.setWidgetResizable(True)
        self.run()
        logger.debug("页面初始化完毕。")


    def addTextLine(self, text: str, labelType: str = "Body"):
        if labelType == "Title":
            label = TitleLabel()
        else:
            label = BodyLabel()
        label.setText(text)
        label.setWordWrap(True)
        self.layout.addWidget(label)

    def run(self):
        self.addTextLine("哈希值校验工具", "Title")
        textEdit_tip = TextEdit(self.widget)
        textEdit_tip.setMarkdown(basicFunc.readFile("/data/hash_tip.md"))
        textEdit_tip.setEnabled(False)
        textEdit_tip.setMinimumHeight(120)
        self.layout.addWidget(textEdit_tip)

        self.layout.addStretch()

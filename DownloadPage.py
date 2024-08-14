from PySide2 import QtCore
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QLabel, QSpacerItem, QSizePolicy
from PySide2.QtWidgets import QVBoxLayout as VBoxLayout
from qfluentwidgets import TitleLabel, BodyLabel, SingleDirectionScrollArea

from widget.DownloadCard import Card as DownloadCard

import webbrowser
import logging

logger = logging.getLogger("FanTools.DownloadPage")


class DownloadPage:
    def __init__(self):
        self.widget = QWidget()
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.spacer = QSpacerItem(20, 400, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.downloadCard = DownloadCard(self.widget)

        self.scrollArea = SingleDirectionScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setObjectName("DownloadPage")
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
        self.layout.addWidget(label, 1)

    def run(self):
        self.addTextLine("下载工具", labelType="Title")
        self.addTextLine("本工具将使用开源工具 aria2c 执行下载任务，aria2c 已经放置在程序目录中。")
        self.addTextLine("在下方粘贴待下载文件的链接，点击按钮后 aria2c 将立即开始下载。")
        self.addTextLine("提示：本工具仅支持单个文件下载，如有大量文件下载需求……我也不知道 TT 😱")

        self.layout.addWidget(self.downloadCard.widget)

        self.layout.addSpacerItem(self.spacer)




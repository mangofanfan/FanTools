from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QLabel, QSpacerItem, QSizePolicy
from qfluentwidgets import VBoxLayout

import webbrowser

from widget.DownloadCard import Card as DownloadCard


class DownloadPage:
    def __init__(self):
        self.widget = QWidget()
        self.widget.setObjectName("DownloadPage")
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.spacer = QSpacerItem(1000, 1000, hData=QSizePolicy.Maximum, vData=QSizePolicy.Maximum)
        self.downloadCard = DownloadCard(self.widget)
        self.run()

    def addTextLine(self, text: str, idName: str = None, alignment=Qt.AlignLeft):
        textLine = QLabel(text=text)
        if idName:
            textLine.setObjectName(idName)
        self.layout.addWidget(textLine, alignment=alignment)

    def run(self):
        self.addTextLine("下载工具", idName="Title")
        self.addTextLine("本工具将使用开源工具 aria2c 执行下载任务，aria2c 已经放置在程序目录中。")
        self.addTextLine("在下方粘贴待下载文件的链接，点击按钮后 aria2c 将立即开始下载。")
        self.addTextLine("提示：本工具仅支持单个文件下载，如有大量文件下载需求……我也不知道 TT 😱")

        self.layout.addWidget(self.downloadCard.widget)

        self.layout.addSpacerItem(self.spacer)




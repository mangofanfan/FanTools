import logging
import subprocess

from PySide2 import QtCore
from PySide2.QtCore import QObject, QThread, Signal
from PySide2.QtWidgets import QFrame
from PySide2.QtWidgets import QVBoxLayout as VBoxLayout
from qfluentwidgets import TitleLabel, BodyLabel, SingleDirectionScrollArea, InfoBar, InfoBarPosition

from widget.DownloadCard import Card as DownloadCard
from widget.function import basicFunc

logger = logging.getLogger("FanTools.DownloadPage")


class DownloadPage:
    def __init__(self):
        self.widget = QFrame()
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
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
        self.layout.addWidget(label)

    def run(self):
        self.addTextLine("下载工具", labelType="Title")
        self.addTextLine("本工具将使用开源工具 aria2c 执行下载任务，aria2c 已经放置在程序目录中。")
        self.addTextLine("在下方粘贴待下载文件的链接，点击按钮后 aria2c 将立即开始下载。")
        self.addTextLine("提示：本工具仅支持单个文件下载，如有大量文件下载需求……我也不知道 TT 😱")

        self.layout.addWidget(self.downloadCard.widget)
        self.downloadCard.PrimaryToolButton_Download.clicked.connect(lambda: self.downloadSingleFile(self.downloadCard.LineEdit_DownloadUrl.text(), self.downloadCard.LineEdit_SavePath.text()))

        self.layout.addStretch()

        return None

    def downloadSingleFile(self, url: str, path: str):
        Thread = QThread(self.widget)
        Worker = Worker_SingleDownload(url, path)
        Worker.moveToThread(Thread)
        Thread.start()
        Worker.run()
        return None


class Worker_SingleDownload(QObject):
    def __init__(self, url: str, path: str):
        super().__init__()
        self.url = url
        self.path = path

    def run(self):
        p = basicFunc.getAria2cPath()
        command = f"{p} {self.url} --dir={self.path}"
        result = subprocess.Popen(command)
        return result




import logging
import subprocess

import aria2p
from PySide2 import QtCore
from PySide2.QtCore import QObject, QThread, Signal
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QFrame, QWidget, QVBoxLayout, QBoxLayout
from PySide2.QtWidgets import QVBoxLayout as VBoxLayout
from qfluentwidgets import TitleLabel, BodyLabel, SingleDirectionScrollArea, SubtitleLabel

import widget.function_setting as funcS
from widget.DownloadCard import Aria2cManageCard, SingleDownloadCard, StatsCard
from widget.function import basicFunc
from widget.function_download import Manager
from widget.function_message import DownloadIB as IB

logger = logging.getLogger("FanTools.DownloadPage")


class DownloadPage:
    def __init__(self):
        self.bodyWidget = QWidget()
        self.bodyWidget.setObjectName("DownloadPage")
        self._layout = QVBoxLayout()
        self.bodyWidget.setLayout(self._layout)
        self._layout.setContentsMargins(0, 5, 0, 0)

        self.widget = QFrame()
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.aric2cManageCard = Aria2cManageCard(self.widget)
        self.singleDownloadCard = SingleDownloadCard(self.widget)
        self.statsCard = StatsCard(self.widget)

        self.scrollArea = SingleDirectionScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setWidgetResizable(True)

        self.addTextLine("下载工具", "Title", self._layout)
        self._layout.addWidget(self.scrollArea)

        self.run()

        self.manager = Manager()

        self.Thread_Time = None
        self.Thread_sDownloadUpdate = None

        logger.debug("页面初始化完毕。")

    def addTextLine(self, text: str, labelType: str = "Body", layout: QBoxLayout = None):
        if labelType == "Title":
            label = TitleLabel()
            label.setAlignment(Qt.AlignCenter)
        elif labelType == "Subtitle":
            label = SubtitleLabel()
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
        self.addTextLine("本工具将使用开源工具 aria2c 执行下载任务，aria2c 已经放置在程序目录中。")
        self.addTextLine("在下方粘贴待下载文件的链接，点击按钮后 aria2c 将立即开始下载。")
        self.addTextLine("提示：本工具仅支持单个文件下载，如有大量文件下载需求……我也不知道 TT 😱")

        self.layout.addWidget(self.aric2cManageCard)
        self.aric2cManageCard.setOff()

        self.layout.addWidget(self.singleDownloadCard.widget)
        self.singleDownloadCard.PrimaryToolButton_Download.clicked.connect(lambda: self.downloadSingleFileStart(self.singleDownloadCard.LineEdit_DownloadUrl.text(), self.singleDownloadCard.LineEdit_SavePath.text()))

        self.layout.addWidget(self.statsCard)

        self.layout.addStretch()

        self.aric2cManageCard.PushButton_ON.clicked.connect(self.startAria2c)
        self.aric2cManageCard.PushButton_OFF.clicked.connect(self.killAria2c)

        return None

    def startAria2c(self):
        p = basicFunc.getAria2cPath()
        command = f"{p} --enable-rpc"
        self.popen = subprocess.Popen(command)
        self.manager.aria2_run()
        self.aric2cManageCard.setOn()
        IB.msgAria2cStart(self.bodyWidget)
        logger.debug("Aria2 进程已经启动。")

        self.Thread_Time = QThread()
        self.Worker_Time = Worker_Time()
        self.Worker_Time.moveToThread(self.Thread_Time)
        self.Worker_Time.updateStats.connect(self.updateTextEdit)
        self.Thread_Time.start()
        self.Worker_Time.runSignal.emit()

        return None

    def killAria2c(self):
        if self.Thread_Time:
            self.Thread_Time.terminate()
        if self.Thread_sDownloadUpdate:
            self.Thread_sDownloadUpdate.terminate()
        self.manager.aria2_exit()
        logger.debug("已经停止对 aria2c 的一切监听。")

        self.popen.kill()
        logger.debug("已经终止 aria2c 程序进程，")

        self.statsCard.TextEdit_std.clear()
        self.aric2cManageCard.setOff()
        IB.msgAria2cKill(self.bodyWidget)
        logger.info("Aria2c 已经结束运行。")
        return None

    def updateTextEdit(self):
        Stats = self.manager.getStatus()
        text = (f"下载速度：{Stats.download_speed}B\n"
                f"上传速度：{Stats.upload_speed}B\n"
                f"活动项目：{Stats.num_active}个\n"
                f"暂停项目：{Stats.num_waiting}个\n"
                f"结束项目：{Stats.num_stopped}个\n"
                f"共计停止项目：{Stats.num_stopped_total}个")
        self.statsCard.TextEdit_std.setText(text)
        return None

    def downloadSingleFileStart(self, url: str, path: str):
        sDownload = self.manager.addUrls([url], path)
        self.singleDownloadCard.setOff()

        self.Thread_sDownloadUpdate = QThread()
        self.Worker_sDownloadUpdate = Worker_sDownloadUpdate(self.manager.get_download(sDownload.gid))
        self.Worker_sDownloadUpdate.moveToThread(self.Thread_sDownloadUpdate)
        self.Worker_sDownloadUpdate.progressIntSignal.connect(self.singleDownloadCard.ProgressBar.setValue)
        self.Worker_sDownloadUpdate.successSignal.connect(self.downloadSingleFileSuccess)
        self.Thread_sDownloadUpdate.start()
        self.Worker_sDownloadUpdate.runSignal.emit()

        IB.msgDownloadStart(self.bodyWidget)

        return None

    def downloadSingleFileSuccess(self, is_success: bool):
        if is_success:
            IB.msgDownloadSuccess(self.bodyWidget)
        else:
            IB.msgDownloadFail(self.bodyWidget)
        self.singleDownloadCard.setOn()
        return None


class Worker_Time(QObject):
    """定时发送更新信号，提醒主线程更新下载进度"""
    updateStats = Signal()
    runSignal = Signal()

    # noinspection PyUnresolvedReferences
    def __init__(self):
        super().__init__()
        self.runSignal.connect(self.run)

    def run(self):
        from time import sleep
        while True:
            self.updateStats.emit()
            logger.debug("更新一次下载状态面板。")
            sleep(funcS.qconfig.get(funcS.cfg.DownloadStatsTimeSleep) * 0.1)


class Worker_sDownloadUpdate(QObject):
    runSignal = Signal()
    progressIntSignal = Signal(int)
    successSignal = Signal(bool)

    def __init__(self, download: aria2p.downloads.Download):
        super().__init__()
        self.runSignal.connect(self.run)
        self.download = download

    def run(self):
        from time import sleep
        while True:
            self.download.update()
            progress = self.download.progress
            gid = self.download.gid
            self.progressIntSignal.emit(progress)
            logger.debug(f"更新一次单文件下载进度条：[{gid}] {progress}%")
            if self.download.is_complete:
                logger.info("一个单独的文件已经下载完成。")
                if self.download.has_failed:
                    logger.warning("似乎出现下载失败，请检查文件是否完成下载。")
                    self.successSignal.emit(False)
                else:
                    self.successSignal.emit(True)
                return None
            sleep(funcS.qconfig.get(funcS.cfg.DownloadStatsTimeSleep) * 0.1)


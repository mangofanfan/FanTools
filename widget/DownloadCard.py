from PySide2.QtGui import Qt
from PySide2.QtWidgets import QGridLayout, QLabel, QWidget
from qfluentwidgets import CardWidget, LineEdit, ToolButton, PrimaryToolButton, InfoBar, InfoBarPosition
from qfluentwidgets import FluentIcon as FIC
import subprocess

from widget.function import basicFunc


class Card:
    def __init__(self, parent: QWidget):
        self.parent = parent
        self.widget = CardWidget()
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)

        self.layout.addWidget(QLabel("下载链接🔗："), 0, 0)
        self.layout.addWidget(QLabel("保存路径📂："), 1, 0)

        self.LineEdit_DownloadUrl = LineEdit()
        self.layout.addWidget(self.LineEdit_DownloadUrl, 0, 1, 1, 2)

        self.LineEdit_SavePath = LineEdit()
        self.layout.addWidget(self.LineEdit_SavePath, 1, 1)

        ToolButton_SavePath = ToolButton()
        ToolButton_SavePath.setIcon(FIC.EDIT)
        ToolButton_SavePath.clicked.connect(self.getPath)
        self.layout.addWidget(ToolButton_SavePath, 1, 2)

        self.layout.addWidget(QLabel("注意您无法指定下载所得的文件名///准备妥当后点击右边按钮立即开始下载！👉"),
                              2, 0, 1, 2, alignment=Qt.AlignRight)
        self.layout.addWidget(QLabel("下载过程中本程序进程可能被阻塞，如下载文件较大可能导致无响应，系正常现象，请勿惊慌😊"),
                              3, 0, 1, 3)

        PrimaryToolButton_Download = PrimaryToolButton()
        PrimaryToolButton_Download.setIcon(FIC.DOWNLOAD)
        PrimaryToolButton_Download.clicked.connect(self.download)
        self.layout.addWidget(PrimaryToolButton_Download, 2, 2)

    def download(self):
        p = basicFunc.getAria2cPath()
        url = self.LineEdit_DownloadUrl.text()
        path = self.LineEdit_SavePath.text()
        command = f"{p} {url} --dir={path}"
        result = subprocess.Popen(command)

        InfoBar.success(title="下载任务已启动😆",
                        content="下载过程中程序进程将被阻塞，请不要急于操作……",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.BOTTOM_RIGHT,
                        duration=4000,
                        parent=self.widget)

        result.wait()
        if result.returncode == 0:
            InfoBar.success(title="下载任务已完成🥳",
                            content="您可以在下载目录中查看该文件~",
                            orient=Qt.Horizontal,
                            isClosable=True,
                            position=InfoBarPosition.TOP_RIGHT,
                            duration=4000,
                            parent=self.parent)
        else:
            InfoBar.error(title="下载失败😭",
                          content=f"aria2c 进程返回错误代码 {result.returncode}",
                          orient=Qt.Horizontal,
                          isClosable=True,
                          position=InfoBarPosition.TOP_RIGHT,
                          duration=4000,
                          parent=self.parent)

    def getPath(self):
        p = basicFunc.openDirDialog(caption="选择一个文件夹用来存放下载的文件叭😊", basedPath=basicFunc.getHerePath())
        self.LineEdit_SavePath.setText(p)

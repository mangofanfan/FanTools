from PySide2.QtCore import QObject
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QGridLayout, QWidget
from qfluentwidgets import CardWidget, LineEdit, ToolButton, PrimaryToolButton, InfoBar, InfoBarPosition, BodyLabel
from qfluentwidgets import FluentIcon as FIC
import subprocess

from widget.function import basicFunc


class Card:
    def __init__(self, parent: QWidget):
        self.parent = parent
        self.widget = CardWidget()
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)

        BodyLabel_1 = BodyLabel()
        BodyLabel_1.setText("下载链接🔗：")
        self.layout.addWidget(BodyLabel_1, 0, 0)
        BodyLabel_2 = BodyLabel()
        BodyLabel_2.setText("保存路径📂：")
        self.layout.addWidget(BodyLabel_2, 1, 0)

        self.LineEdit_DownloadUrl = LineEdit()
        self.layout.addWidget(self.LineEdit_DownloadUrl, 0, 1, 1, 2)

        self.LineEdit_SavePath = LineEdit()
        self.layout.addWidget(self.LineEdit_SavePath, 1, 1)

        self.ToolButton_SavePath = ToolButton()
        self.ToolButton_SavePath.setIcon(FIC.EDIT)
        self.ToolButton_SavePath.clicked.connect(self.getPath)
        self.layout.addWidget(self.ToolButton_SavePath, 1, 2)

        BodyLabel_3 = BodyLabel()
        BodyLabel_3.setText("注意您无法指定下载所得的文件名///准备妥当后点击右边按钮立即开始下载！👉")
        BodyLabel_4 = BodyLabel()
        BodyLabel_4.setText("下载过程中本程序进程可能被阻塞，如下载文件较大可能导致无响应，系正常现象，请勿惊慌😊")
        self.layout.addWidget(BodyLabel_3, 2, 0, 1, 2, alignment=Qt.AlignRight)
        self.layout.addWidget(BodyLabel_4, 3, 0, 1, 3)

        self.PrimaryToolButton_Download = PrimaryToolButton()
        self.PrimaryToolButton_Download.setIcon(FIC.DOWNLOAD)
        self.layout.addWidget(self.PrimaryToolButton_Download, 2, 2)

    def getPath(self):
        p = basicFunc.openDirDialog(caption="选择一个文件夹用来存放下载的文件叭😊", basedPath=basicFunc.getHerePath())
        self.LineEdit_SavePath.setText(p)

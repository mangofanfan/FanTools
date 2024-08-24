import logging
from functools import partial

from PySide2 import QtCore
from PySide2.QtCore import QUrl
from PySide2.QtGui import QDesktopServices, Qt
from PySide2.QtWidgets import QFrame, QGridLayout, QWidget, QVBoxLayout, QBoxLayout
from qfluentwidgets import VBoxLayout, TitleLabel, BodyLabel, SingleDirectionScrollArea, SubtitleLabel

from widget.SimpleCard import LinkCard, ToolCard, EndlessCard
from widget.function import PIC

logger = logging.getLogger("FanTools.AboutPage")


class AboutPage:
    def __init__(self):
        self.bodyWidget = QWidget()
        self.bodyWidget.setObjectName("AboutPage")
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

        self.addTextLine("关于芒果工具箱", "Title", self._layout)
        self._layout.addWidget(self.scrollArea)

        self.run()
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
        if layout:
            layout.addWidget(label)
        else:
            self.layout.addWidget(label)
        return None

    def run(self):
        self.addTextLine("前置科技树", "Subtitle")
        self.layout.addWidget(LinkCard(PIC.IconPython, "Python", "我从小学到大（？）的高级语言", "https://www.python.org/", "官网"))
        self.layout.addWidget(LinkCard(PIC.IconQt, "PySide", "Qt库的Python版本，可以用Python创建高级的窗口应用程序", "https://www.qt.io/zh-cn/qt-for-python", "官网"))
        self.layout.addWidget(LinkCard(PIC.IconQFluentWidgets, "QFluentWidgets", "开箱即用的WinUI3风格Qt组件库，用的都说好", "https://qfluentwidgets.com/zh/", "官网"))

        self.addTextLine("本程序配套的在线资源或链接", "Subtitle")
        ToolCardLayout = QGridLayout()
        self.layout.addLayout(ToolCardLayout)
        ToolCardLayout.addWidget(ToolCard(PIC.IconGitHub, "代码仓库", "芒果工具箱是开源项目\n您随时可以查看最新的源码以学习或进行改进", partial(QDesktopServices.openUrl, (QUrl("https://github.com/mangofanfan/FanTools")))), 0, 0)
        ToolCardLayout.addWidget(ToolCard(PIC.IconWriterSide, "在线文档", "在线文档包含用户文档和开发文档\n为什么不来看看呢？", partial(QDesktopServices.openUrl, ("https://docs.mangofanfan.cn/fantools/"))), 0, 1)

        ContributorCard = EndlessCard("鸣谢名单", "对芒果工具箱项目做出贡献的人们！")
        self.layout.addWidget(ContributorCard)
        ContributorCard.add("MangoFanFan_", "主要开发者与负责人")

        self.layout.addStretch()
        return None

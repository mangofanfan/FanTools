import logging
from functools import partial

from PySide2 import QtCore
from PySide2.QtCore import QUrl, QSize
from PySide2.QtGui import QDesktopServices, Qt
from PySide2.QtWidgets import QFrame, QGridLayout, QWidget, QVBoxLayout, QBoxLayout, QHBoxLayout
from qfluentwidgets import VBoxLayout, TitleLabel, BodyLabel, SingleDirectionScrollArea, SubtitleLabel, \
    SimpleCardWidget, ImageLabel

from widget.SimpleCard import LinkCard, ToolCard, EndlessCard
from widget.function import PIC, basicFunc

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
        label.setWordWrap(True)
        if layout:
            layout.addWidget(label)
        else:
            self.layout.addWidget(label)
        return None

    def run(self):
        ProgramCard = SimpleCardWidget()
        self.layout.addWidget(ProgramCard)
        pcLayout = QHBoxLayout()
        ProgramCard.setLayout(pcLayout)
        pcContentLayout = QVBoxLayout()
        pcLayout.addLayout(pcContentLayout)
        self.addTextLine("工具箱信息", "Subtitle", pcContentLayout)
        self.addTextLine("芒果工具箱是一个很无厘头的项目……工具箱能从芒果的垃圾桶里死而复生，很大的因素是因为芒果需要在两天的时间内搞出一个能用的翻译工具……", layout=pcContentLayout)
        self.addTextLine("但是工具箱的使命还没有完成：我又花了超过三个星期的时间来让翻译工具变得真正可用，然后继续编写下载工具……", layout=pcContentLayout)
        self.addTextLine("总之，希望工具箱的存在对您有所帮助，那样的话我就满意辽！awa", layout=pcContentLayout)
        imageLabel = ImageLabel()
        imageLabel.setImage(basicFunc.getHerePath() + "/data/two_mango_es.png")
        imageLabel.setFixedSize(QSize(120, 120))
        pcLayout.addWidget(imageLabel)

        self.addTextLine("前置科技树", "Subtitle")
        self.layout.addWidget(LinkCard(PIC.IconPython, "Python", "我从小学到大（？）的高级语言", "https://www.python.org/", "官网"))
        self.layout.addWidget(LinkCard(PIC.IconQt, "PySide", "Qt库的Python版本，可以用Python创建高级的窗口应用程序", "https://www.qt.io/zh-cn/qt-for-python", "官网"))
        self.layout.addWidget(LinkCard(PIC.IconQFluentWidgets, "QFluentWidgets", "开箱即用的WinUI3风格Qt组件库，用的都说好", "https://qfluentwidgets.com/zh/", "官网"))

        self.addTextLine("本程序配套的在线资源或链接", "Subtitle")
        ToolCardLayout = QGridLayout()
        self.layout.addLayout(ToolCardLayout)
        ToolCardLayout.addWidget(ToolCard(PIC.IconGitHub, "代码仓库", "芒果工具箱是开源项目\n您随时可以查看最新的源码以学习或进行改进\n同时这里也是漏洞追踪器！", partial(QDesktopServices.openUrl, (QUrl(basicFunc.getInfo()["github"])))), 0, 0)
        ToolCardLayout.addWidget(ToolCard(PIC.IconWriterSide, "在线文档", "在线文档包含用户文档和开发文档\n为什么不来看看呢？", partial(QDesktopServices.openUrl, QUrl(basicFunc.getInfo()["docs"]))), 0, 1)

        ContributorCard = EndlessCard("鸣谢名单", "对芒果工具箱项目做出贡献的人们！")
        self.layout.addWidget(ContributorCard)
        ContributorCard.add("MangoFanFan_", "主要开发者与负责人", "https://mangofanfan.cn/")
        ContributorCard.add("芒果的同学们", "每天被芒果摁着听他发牢骚（不我没有）")

        ModuleCard = EndlessCard("依赖项目", "芒果工具箱的今天还离不开下列项目提供的轮子！（下方卡片可以点击）")
        self.layout.addWidget(ModuleCard)
        ModuleCard.add("aria2", "开源的高速下载器", "https://github.com/aria2/aria2")
        ModuleCard.add("aria2p", "提供通过Python+JsonRPC操作aria2的方法", "https://github.com/pawamoy/aria2p")
        ModuleCard.add("requests", "非转基因高级网络库（？）", "https://requests.readthedocs.io/projects/cn/zh-cn/latest/")
        ModuleCard.add("Hitokoto", "一言", "https://hitokoto.cn/")

        self.layout.addStretch()
        return None

from pathlib import Path

from PySide2 import QtCore
from PySide2.QtCore import QSize, QUrl
from PySide2.QtGui import Qt, QDesktopServices
from PySide2.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout, QWidget, QBoxLayout
from qfluentwidgets import MessageBox, VBoxLayout, PushButton, PrimaryPushButton, TitleLabel, BodyLabel, \
    SingleDirectionScrollArea, ToolTipFilter, HorizontalFlipView, SimpleCardWidget, SubtitleLabel, \
    DisplayLabel
from qfluentwidgets import FluentIcon as FIC

import logging

from widget.SimpleCard import ToolCard, YiYanCard
from widget.function import basicFunc, PIC

logger = logging.getLogger("FanTools.HomePage")

class HomePage:

    def __init__(self, parent=None):
        self.bodyWidget = QWidget()
        self.parent = parent
        self.bodyWidget.setObjectName("HomePage")
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

        TitleLayout = QHBoxLayout()
        self._layout.addLayout(TitleLayout)
        self.addTextLine("芒果工具箱", "Display", TitleLayout)
        self.addTextLine(f"FanTools v-{basicFunc.getInfo()['v']}", "Title", TitleLayout)
        TitleLayout.addStretch()
        self._layout.addWidget(self.scrollArea)

        self.run()
        logger.debug("页面初始化完毕。")

    def addTextLine(self, text: str, labelType: str = "Body", layout: QBoxLayout = None):
        if labelType == "Display":
            label = DisplayLabel()
            label.setAlignment(Qt.AlignCenter)
        elif labelType == "Title":
            label = TitleLabel()
            label.setAlignment(Qt.AlignCenter)
        elif labelType == "Subtitle":
            label = SubtitleLabel()
        else:
            label = BodyLabel()
        label.setText(text)
        label.setWordWrap(True)
        if not layout:
            self.layout.addWidget(label)
        else:
            layout.addWidget(label)
        return None

    def showMessageBox(self):
        w = MessageBox("支持作者🙏",
                       "芒果帆帆的第一个正式作品，希望能得到您的肯定！QAQ🙏🩷😘",
                       self.parent)
        w.yesButton.setText("帆域网站🛜")
        w.yesButton.setToolTip("前往帆域网站上本程序（芒果工具箱）的发布页😊")
        w.yesButton.installEventFilter(ToolTipFilter(w.yesButton))
        w.yesSignal.connect(lambda: QDesktopServices.openUrl(QUrl(basicFunc.getInfo()["publish"])))
        w.cancelButton.setText("我知道啦👋")
        w.cancelButton.setToolTip("关闭弹窗并无事发生🤫")
        w.cancelButton.installEventFilter(ToolTipFilter(w.cancelButton))
        logger.info("激活「芒果帆帆」消息框。")
        if w.exec_():
            logger.info("在「芒果帆帆」消息框中打开了程序发布页面。")

    def run(self):
        self.flipView = HorizontalFlipView()
        # 按序读取所有图片
        i = 1
        while True:
            fileName = basicFunc.getHerePath() + f"/data/image/myPicture ({i}).png"
            if Path(fileName).exists():
                self.flipView.addImage(fileName)
                i += 1
                continue
            else:
                logger.debug(f"加载了{i-1}张图片作为首页轮播图。")
                break
        self.flipView.setFixedHeight(162)
        self.flipView.setItemSize(QSize(288, 162))
        self.flipView.setItemAlignment(Qt.AlignCenter)
        self.flipView.setBorderRadius(10)
        self.layout.addWidget(self.flipView)

        CardViewLayout = QHBoxLayout()
        Card_Version = SimpleCardWidget()
        Card_Version_Layout = QVBoxLayout()
        Card_Version.setLayout(Card_Version_Layout)
        self.addTextLine("技术信息", "Subtitle", Card_Version_Layout)
        self.addTextLine(f"目前版本：{basicFunc.getInfo()['v']} 早期技术验证", layout=Card_Version_Layout)
        self.addTextLine("现在不保证任何意义上的稳定性与实用性。", layout=Card_Version_Layout)
        CardViewLayout.addWidget(Card_Version)
        Card_Author = SimpleCardWidget()
        Card_Author_Layout = QVBoxLayout()
        Card_Author.setLayout(Card_Author_Layout)
        self.addTextLine("作者信息", "Subtitle", Card_Author_Layout)
        self.addTextLine("芒果帆帆w🥭", layout=Card_Author_Layout)
        buttonLayout = QHBoxLayout()
        pushButton_about = PushButton()
        pushButton_about.setText("关于本程序")
        pushButton_about.clicked.connect(self.showMessageBox)
        buttonLayout.addWidget(pushButton_about, alignment=Qt.AlignLeft)
        pushButton_author = PrimaryPushButton()
        pushButton_author.setText("关于芒果帆帆")
        pushButton_author.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://mangofanfan.cn/")))
        buttonLayout.addWidget(pushButton_author, alignment=Qt.AlignLeft)
        buttonLayout.addStretch()
        Card_Author_Layout.addLayout(buttonLayout)
        CardViewLayout.addWidget(Card_Author)
        CardViewLayout.setStretch(0, 1)
        CardViewLayout.setStretch(1, 1)
        self.layout.addLayout(CardViewLayout)

        CardToolLayout = QHBoxLayout()
        self.ToolCard_Download = ToolCard(PIC.IconDownload, "下载工具", "基于 Aria2c 的简易下载器")
        self.ToolCard_Hash = ToolCard(PIC.IconHash, "文件工具", "文件哈希值校验与多种工具")
        self.ToolCard_Translate = ToolCard(PIC.IconTranslate, "翻译工具", "基于文本的自研简陋翻译器")
        CardToolLayout.addWidget(self.ToolCard_Download)
        CardToolLayout.addWidget(self.ToolCard_Hash)
        CardToolLayout.addWidget(self.ToolCard_Translate)
        self.layout.addLayout(CardToolLayout)

        self.YiYanCard = YiYanCard()
        self.layout.addWidget(self.YiYanCard)

        self.layout.addStretch()


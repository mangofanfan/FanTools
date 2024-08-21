from pathlib import Path

from PySide2 import QtCore
from PySide2.QtCore import QSize
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QSpacerItem, QSizePolicy, QHBoxLayout, QFrame, QVBoxLayout
from qfluentwidgets import MessageBox, VBoxLayout, PushButton, PrimaryPushButton, TitleLabel, BodyLabel, \
    SingleDirectionScrollArea, ToolTipFilter, ImageLabel, FlipView, HorizontalFlipView, SimpleCardWidget, SubtitleLabel, \
    DisplayLabel

import webbrowser
import logging

from widget.function import basicFunc

logger = logging.getLogger("FanTools.MainPage")

class MainPage:
    def __init__(self):
        self.widget = QFrame()
        self.widget.setObjectName("MainPage")
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)

        self.scrollArea = SingleDirectionScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setObjectName("MainPage")
        self.scrollArea.setWidgetResizable(True)
        self.run()
        logger.debug("页面初始化完毕。")

    def addTextLine(self, text: str, labelType: str = "Body", layout: QVBoxLayout = None):
        if labelType == "Display":
            label = DisplayLabel()
        elif labelType == "Title":
            label = TitleLabel()
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

    def showMessageBox(self):
        w = MessageBox("支持作者🙏",
                       "芒果帆帆的第一个正式作品，希望能得到您的肯定！QAQ🙏🩷😘",
                       self.widget)
        w.yesButton.setText("帆域网站🛜")
        w.yesButton.setToolTip("前往帆域网站上本程序（芒果工具箱）的发布页😊")
        w.yesButton.installEventFilter(ToolTipFilter(w.yesButton))
        w.cancelButton.setText("我知道啦👋")
        w.cancelButton.setToolTip("关闭弹窗并无事发生🤫")
        w.cancelButton.installEventFilter(ToolTipFilter(w.cancelButton))
        logger.info("激活「芒果帆帆」消息框。")
        if w.exec_():
            webbrowser.open("https://mangofanfan.cn/")
            logger.info("在「芒果帆帆」消息框中打开了芒果的网站。")

    def run(self):
        TitleLayout = QHBoxLayout()
        self.layout.addLayout(TitleLayout)
        self.addTextLine("芒果工具箱", "Display", TitleLayout)
        self.addTextLine("FanTools v-0.0.0", "Title", TitleLayout)
        TitleLayout.addStretch()

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
        self.addTextLine("目前版本：0.0.0 早期技术验证", layout=Card_Version_Layout)
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
        pushButton_author.clicked.connect(lambda: webbrowser.open("https://mangofanfan.cn/"))
        buttonLayout.addWidget(pushButton_author, alignment=Qt.AlignLeft)
        buttonLayout.addStretch()
        Card_Author_Layout.addLayout(buttonLayout)
        CardViewLayout.addWidget(Card_Author)
        CardViewLayout.setStretch(0, 1)
        CardViewLayout.setStretch(1, 1)
        self.layout.addLayout(CardViewLayout)

        self.layout.addStretch()


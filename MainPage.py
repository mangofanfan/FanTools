from PySide2 import QtCore
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from qfluentwidgets import MessageBox, VBoxLayout, PushButton, PrimaryPushButton, TitleLabel, BodyLabel, \
    SingleDirectionScrollArea

import webbrowser


class MainPage:
    def __init__(self):
        self.widget = QWidget()
        self.widget.setObjectName("MainPage")
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.buttonLayout = QHBoxLayout(self.widget)
        self.spacer = QSpacerItem(200, 200, hData=QSizePolicy.Expanding, vData=QSizePolicy.Expanding)

        self.scrollArea = SingleDirectionScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setObjectName("MainPage")
        self.scrollArea.setWidgetResizable(True)
        self.run()

    def addTextLine(self, text: str, labelType: str = "Body"):
        if labelType == "Title":
            label = TitleLabel()
        else:
            label = BodyLabel()
        label.setText(text)
        self.layout.addWidget(label)

    def showMessageBox(self):
        w = MessageBox("支持作者🙏",
                       "芒果帆帆的第一个正式作品，希望能得到您的肯定！QAQ🙏🩷😘",
                       self.widget)
        w.yesButton.setText("帆域网站🛜")
        w.yesButton.setToolTip("前往帆域网站上本程序（芒果工具箱）的发布页😊")
        w.cancelButton.setText("我知道啦👋")
        w.cancelButton.setToolTip("关闭弹窗并无事发生🤫")
        if w.exec_():
            webbrowser.open("https://ifanspace.top/")

    def run(self):
        self.addTextLine("欢迎使用芒果工具箱（FanTools）！", "Title")
        self.addTextLine("本工具箱中包含的功能可从程序左侧边栏快速访问~")
        self.addTextLine("作者：芒果帆帆w🥭")

        pushButton_about = PushButton()
        pushButton_about.setText("关于本程序")
        pushButton_about.clicked.connect(self.showMessageBox)
        self.buttonLayout.addWidget(pushButton_about, alignment=Qt.AlignLeft)
        pushButton_author = PrimaryPushButton()
        pushButton_author.setText("关于芒果帆帆")
        pushButton_author.clicked.connect(lambda: webbrowser.open("https://mangofanfan.cn/"))
        self.buttonLayout.addWidget(pushButton_author, alignment=Qt.AlignLeft)
        self.buttonLayout.addSpacerItem(self.spacer)
        self.layout.addLayout(self.buttonLayout)

        self.layout.addSpacerItem(self.spacer)


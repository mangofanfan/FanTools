# 开发文档 | Develop Guide

这里会对工具箱的编码逻辑、基本结构等进行介绍说明。

在继续下去之前，请再次阅读工具箱项目的开发依赖：

* Python 3.8.19（conda 环境）
* PySide2 5.15.2.1
* qfluentwidgets（通俗的说是 Qt 界面美化库）

个别工具的个别依赖会在工具的文档中介绍。

## 工具页面基本结构

为确保程序所有界面的观感统一，我为工具箱的每个页面定义了其基本结构和基本函数。

### 文本标签

首先，页面顶部必须有一个标题，使用自qfluentwidgets中导入的TitleLabel。同时为了便于在页面中添加较多的文字语句时简化编码，我在每个页面中定义了一个相同的函数。

<code-block lang="python">
    def addTextLine(self, text: str, labelType: str = "Body"):
        if labelType == "Title":
            label = TitleLabel()
        else:
            label = BodyLabel()
        label.setText(text)
        self.layout.addWidget(label)
</code-block>

此函数接收简单的两个参数，一个`text`是显示文本，后面的`labelType`是文本类型。如果类型为「标题」，则使用TitleLabel显示文本，否则则为「内容」，用BodyLabel显示。

在早期的版本中我使用QLabel+id选择器+QSS的方式来实现类似功能，但是由于qfluentwidgets的新组件都能够自动跟随qfluentwidgets的亮色、暗色模式，自己写的话还要重新造轮子，遂更改。

## 下载工具

下载工具通过 aria2c 开源工具实现下载功能，目前已经且近实现了单文件下载。

由于这段代码在编写时本人技术不佳，没有真正实现多线程或多进程，反正导致下载过程中GUI会假死，下载大文件时会有点难受。

### 技术细节

工具页面中的那个卡片并非嵌入在页面的源码中，而是在外部实现后 import 并实例化的。

<code-block lang="python">
    from widget.DownloadCard import Card as DownloadCard
    class DownloadPage:
        def __init__(self):
            self.widget = QWidget()
            self.layout = VBoxLayout(self.widget)
            self.widget.setLayout(self.layout)
            self.spacer = QSpacerItem(200, 200, hData=QSizePolicy.Expanding, vData=QSizePolicy.Expanding)
            self.downloadCard = DownloadCard(self.widget)
            self.scrollArea = SingleDirectionScrollArea()
            self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.scrollArea.setWidget(self.widget)
            self.scrollArea.setObjectName("DownloadPage")
            self.scrollArea.setWidgetResizable(True)
            self.run()
        def addTextLine(self, text: str, labelType: str = "Body"):
            if labelType == "Title":
                label = TitleLabel()
            else:
                label = BodyLabel()
            label.setText(text)
            self.layout.addWidget(label)
        def run(self):
            self.addTextLine("下载工具", labelType="Title")
            self.addTextLine("本工具将使用开源工具 aria2c 执行下载任务，aria2c 已经放置在程序目录中。")
            self.addTextLine("在下方粘贴待下载文件的链接，点击按钮后 aria2c 将立即开始下载。")
            self.addTextLine("提示：本工具仅支持单个文件下载，如有大量文件下载需求……我也不知道 TT 😱")
            self.layout.addWidget(self.downloadCard.widget)
            self.layout.addSpacerItem(self.spacer)
</code-block>

解释一下代码中跟`DownloadCard`有关的部分。

* 我们在外部定义了`DownloadCard`，然后将其导入后实例化为`self.downloadCard`，父对象设置成`self.widget`；
* 然后在剩下的页面代码中完全不再操作`self.downloadCard`，因为后者的结构、外观，以及信号和下载函数绑定都已经另外完成了。
* 这样做的好处是可以实现代码解耦，以及复用。如果程序中有不止一个页面需要提供简单的下载功能，我们也只需要把`DownloadCard`倒进来然后扔到layout里的合适位置即可。

这个页面的显示效果是这样的。

![DownloadPage-1.png](DownloadPage-1.png)

DownloadCard的结构如下，我的经验是每当要写一个界面类`XXX`时，把`XXX.widget`定义成一个`QWidget`，然后所有的组件都扔到`XXX.widget`里去。

<warning>
仅作演示用，由于一些很显而易见的问题，此段代码正等待重构……
</warning>

<code-block lang="python">
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
        ToolButton_SavePath = ToolButton()
        ToolButton_SavePath.setIcon(FIC.EDIT)
        ToolButton_SavePath.clicked.connect(self.getPath)
        self.layout.addWidget(ToolButton_SavePath, 1, 2)
        BodyLabel_3 = BodyLabel()
        BodyLabel_3.setText("注意您无法指定下载所得的文件名///准备妥当后点击右边按钮立即开始下载！👉")
        BodyLabel_4 = BodyLabel()
        BodyLabel_4.setText("下载过程中本程序进程可能被阻塞，如下载文件较大可能导致无响应，系正常现象，请勿惊慌😊")
        self.layout.addWidget(BodyLabel_3, 2, 0, 1, 2, alignment=Qt.AlignRight)
        self.layout.addWidget(BodyLabel_4, 3, 0, 1, 3)
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
</code-block>

大概就是这样，懂我意思就好……

## 翻译工具

翻译工具可以说是本来将要被扫进芒果的垃圾桶的芒果工具箱能够起死回生的直接契机。关于这段故事，请看[我的博客](https://mangofanfan.cn/2024/08/13/%e6%9a%91%e5%81%87%e7%94%9f%e6%b4%bb%e5%90%96/)……

为了这个翻译工具，我开拓了一些至关重要的前置科技，比如[多窗口亮暗主题切换](Global-Theme.md)和[多线程实现](QThread.md)……


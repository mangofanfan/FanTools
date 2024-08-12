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

### 滚动页面

滚动功能是我测试了很久才终于玩明白了一点的功能。

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

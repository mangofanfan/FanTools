import traceback

from qfluentwidgets import InfoBar, InfoBarPosition, FlyoutAnimationType, IndeterminateProgressRing


def msgTextIdError(self):
    InfoBar.error(title="错误",
                  content="尝试打开不存在的词条。",
                  isClosable=False,
                  duration=2000,
                  position=InfoBarPosition.TOP_RIGHT,
                  parent=self)

def msgNotImportProject(self):
    InfoBar.warning(title="警告",
                    content="先要导入项目工程文件才能开始干活哦~",
                    isClosable=False,
                    duration=2000,
                    position=InfoBarPosition.TOP_RIGHT,
                    parent=self)

def msgMultiLoading(self):
    bar = InfoBar.info(title="正在加载数据",
                       content="请等待本消息条消失后再开始工作诺！",
                       isClosable=False,
                       duration=-1,
                       position=InfoBarPosition.TOP_RIGHT,
                       parent=self)
    ring = IndeterminateProgressRing()
    ring.setFixedSize(40, 40)
    bar.addWidget(ring)
    return bar

def msgChooseImportProjectSuccess(self):
    InfoBar.success(title="选取成功",
                    content="文件名称校验正确，没有错误发生。现在您可以启动翻译器了。",
                    isClosable=True,
                    duration=2000,
                    position=InfoBarPosition.TOP_RIGHT,
                    parent=self)

def msgChooseImportProjectWarning_1(self):
    InfoBar.warning(title="潜在错误警告",
                    content="文件名称校验不完全正确，您确定选择了正确的文件吗？\n"
                            "详细信息：正确的文件后缀名应为 .ft-translateProject.txt，您选取的文件似乎与之不同。\n"
                            "如您确认无误，可以继续启动翻译器。",
                    isClosable=False,
                    duration=20000,
                    position=InfoBarPosition.TOP_RIGHT,
                    parent=self)

def msgChooseImportProjectWarning_2(self):
    InfoBar.warning(title="严重错误警告",
                    content="文件名称校验不正确，您确定选择了正确的文件吗？\n"
                            "详细信息：正确的文件后缀名应为 .ft-translateProject.txt，您选取的文件显然与之不同。\n"
                            "如果您是在恶作剧的话——若文件内容无误，翻译器仍然可以启动，但这样真的……好么？",
                    isClosable=False,
                    duration=20000,
                    position=InfoBarPosition.TOP_RIGHT,
                    parent=self)


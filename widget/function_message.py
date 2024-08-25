import traceback

from qfluentwidgets import InfoBar, InfoBarPosition, IndeterminateProgressRing

### 翻译工具 ###
class TranslateIB:
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

    def msgLoadingReady(self):
        InfoBar.success(title="翻译器加载完毕",
                        content="您现在可以开始工作了。",
                        isClosable=True,
                        duration=4000,
                        position=InfoBarPosition.TOP_RIGHT,
                        parent=self)

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
                        duration=4000,
                        position=InfoBarPosition.TOP_RIGHT,
                        parent=self)

    def msgChooseImportProjectWarning_2(self):
        InfoBar.warning(title="严重错误警告",
                        content="文件名称校验不正确，您确定选择了正确的文件吗？\n"
                                "详细信息：正确的文件后缀名应为 .ft-translateProject.txt，您选取的文件显然与之不同。\n"
                                "如果您是在恶作剧的话——若文件内容无误，翻译器仍然可以启动，但这样真的……好么？",
                        isClosable=False,
                        duration=4000,
                        position=InfoBarPosition.TOP_RIGHT,
                        parent=self)

    def msgMultiSameWindowWarning(self):
        InfoBar.warning(title="操作已阻止",
                        content="您已经打开一个翻译器了，不支持同时多开呢……",
                        isClosable=False,
                        duration=4000,
                        position=InfoBarPosition.TOP_RIGHT,
                        parent=self)

    def msgNoFileChosen(self):
        InfoBar.warning(title="未选中文件",
                        content="您似乎没有选中任何文件？\n"
                                "如果您真的选中了文件却看到此提示，请向开发者反馈……",
                        isClosable=False,
                        duration=4000,
                        position=InfoBarPosition.TOP_RIGHT,
                        parent=self)

    def msgNoAPIChosen(self):
        InfoBar.warning(title="未选择API",
                        content="调用API翻译之前，是不是应该先选择一个API来调用呢？\n"
                                "若您已经选择了API但仍看见此提示，请向开发者反馈……",
                        isClosable=False,
                        duration=4000,
                        position=InfoBarPosition.TOP_RIGHT,
                        parent=self)

    def msgNoInputName(self):
        InfoBar.error(title="未输入项目名称",
                      content="您需要指定一个项目名称，刚刚您什么都没输入。\n"
                              "再给你一次机会创建项目，记得输入名称哈。",
                      isClosable=False,
                      duration=4000,
                      position=InfoBarPosition.BOTTOM_RIGHT,
                      parent=self)

    def msgNameNotAllowed(self):
        InfoBar.error(title="未输入有效项目名称",
                      content="您需要指定一个有效项目名称，请重新输入。\n"
                              "项目名中可能包含非法字符，或名称与已存在项目重复。",
                      isClosable=False,
                      duration=4000,
                      position=InfoBarPosition.BOTTOM_RIGHT,
                      parent=self)
### 翻译工具结束 ###

### 下载工具 ###
class DownloadIB:
    def msgAria2cStart(self):
        InfoBar.info(title="Aria2c开始运行",
                     content="现在可以执行下载任务啦",
                     isClosable=True,
                     duration=4000,
                     position=InfoBarPosition.TOP_RIGHT,
                     parent=self)

    def msgAria2cKill(self):
        InfoBar.info(title="Aria2c运行结束",
                     content="下载功能已禁用",
                     isClosable=True,
                     duration=4000,
                     position=InfoBarPosition.TOP_RIGHT,
                     parent=self)

    def msgAria2cAlreadyStart(self):
        InfoBar.warning(title="Aria2c已经在运行中",
                        content="禁止重复启动",
                        isClosable=False,
                        duration=4000,
                        position=InfoBarPosition.TOP_RIGHT,
                        parent=self)

    def msgAria2cAlreadyKill(self):
        InfoBar.warning(title="Aria2c并未在运行中",
                        content="无法再次结束已结束的程序",
                        isClosable=False,
                        duration=4000,
                        position=InfoBarPosition.TOP_RIGHT,
                        parent=self)

    def msgDownloadStart(self):
        InfoBar.success(title="下载已经开始",
                        content="下载任务已经发送至 Aria2c，请耐心等待……",
                        isClosable=True,
                        duration=4000,
                        position=InfoBarPosition.TOP_RIGHT,
                        parent=self)

    def msgDownloadSuccess(self):
        InfoBar.success(title="下载成功",
                        content="下载任务已顺利完成！",
                        isClosable=True,
                        duration=4000,
                        position=InfoBarPosition.TOP_RIGHT,
                        parent=self)

    def msgDownloadFail(self):
        InfoBar.error(title="下载出现异常",
                      content="无法确定下载状态，请手动检查。",
                      isClosable=False,
                      duration=4000,
                      position=InfoBarPosition.TOP_RIGHT,
                      parent=self)

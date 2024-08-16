import logging
import sys

from PySide2 import QtCore
from PySide2.QtCore import QObject, Signal, QThread
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QHBoxLayout, QVBoxLayout, QButtonGroup, QApplication
from qfluentwidgets import FluentIcon as FIC, RadioButton, ToolTipFilter, qconfig, isDarkTheme, FluentTitleBar
from qfluentwidgets import VBoxLayout, PushButton, RoundMenu, Action, TitleLabel, BodyLabel, SingleDirectionScrollArea, \
    HeaderCardWidget, LineEdit, StrongBodyLabel
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow

import widget.function_translateMsg as IB
import widget.function_translate as funcT
from script.translate_rule import Rule
from widget.TranslateButtonCard import Card_Single, Card_Multi
from widget.TranslateMultiPage import Ui_Form as TranslateMultiPageUi
from widget.TranslateTextCard import Card as TranslateTextCard
from widget.TranslateToolPage import Ui_Form as TranslateToolPageUi
from widget.function import basicFunc
from widget.function_translate import TranslateText

logger = logging.getLogger("FanTools.TranslatePage")


class TranslateWindow(BackgroundAnimationWidget, FramelessWindow):
    def __init__(self, parent=None):
        self._isMicaEnabled = False
        self._lightBackgroundColor = QColor(243, 243, 243)
        self._darkBackgroundColor = QColor(32, 32, 32)
        super().__init__(parent=parent)

        self.setTitleBar(FluentTitleBar(self))

    def setMicaEffectEnabled(self, isEnabled: bool):
        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return

        self._isMicaEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self._normalBackgroundColor())

    def isMicaEffectEnabled(self):
        return self._isMicaEnabled

    def _onThemeChangedFinished(self):
        if self.isMicaEffectEnabled():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())


class TranslatePage(QObject):

    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.spacer = QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.scrollArea = SingleDirectionScrollArea()
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.widget)
        self.scrollArea.setObjectName("TranslatePage")
        self.scrollArea.setWidgetResizable(True)

        self.CardSingle = Card_Single()
        self.CardMulti = Card_Multi()

        self.Tool = TranslateToolPage()
        self.Multi = TranslateMultiPage()

        self.run()
        logger.debug("页面初始化完毕。")

    def addTextLine(self, text: str, labelType: str = "Body"):
        if labelType == "Title":
            label = TitleLabel()
        else:
            label = BodyLabel()
        label.setText(text)
        label.setWordWrap(True)
        self.layout.addWidget(label, 1)

    def run(self):
        self.addTextLine("翻译工具", "Title")
        self.addTextLine("工具箱提供两种翻译器可供选择，均支持调用外部API进行翻译（例如：百度通用文本翻译、有道文本翻译）（俗称机器翻译）。")
        self.addTextLine("请先在工具箱设置中配置对应的凭证，然后再尝试机器翻译。")

        # 一张标题内容卡片
        self.CardStart = HeaderCardWidget(self.widget)
        self.CardStart.setTitle("翻译项目设置")
        self.layout.addWidget(self.CardStart)

        self.CardStart_vBoxLayout = QVBoxLayout()
        self.CardStart.viewLayout.addLayout(self.CardStart_vBoxLayout)

        StrongBodyLabel_ImportProject = StrongBodyLabel()
        StrongBodyLabel_ImportProject.setText("导入翻译项目")
        self.CardStart_vBoxLayout.addWidget(StrongBodyLabel_ImportProject)
        BodyLabel_ImportProject = BodyLabel()
        BodyLabel_ImportProject.setText("您需要先将待翻译的工程文件导入此处，才能启动翻译工具哦！")
        self.CardStart_vBoxLayout.addWidget(BodyLabel_ImportProject)

        self.Layout_ImportProject = QHBoxLayout()
        self.CardStart_vBoxLayout.addLayout(self.Layout_ImportProject)
        self.LineEdit_ImportProject = LineEdit()
        self.LineEdit_ImportProject.setFixedHeight(30)
        self.Layout_ImportProject.addWidget(self.LineEdit_ImportProject)
        self.PushButton_ImportProject = PushButton()
        self.PushButton_ImportProject.setFixedHeight(30)
        self.PushButton_ImportProject.setText("选择文件")
        self.PushButton_ImportProject.clicked.connect(self.chooseImportProject)
        self.Layout_ImportProject.addWidget(self.PushButton_ImportProject)

        self.CardStart_vBoxLayout.addSpacing(20)

        StrongBodyLabel_MultiLimit = StrongBodyLabel()
        StrongBodyLabel_MultiLimit.setText("列表多项翻译工具的单次加载数量上限")
        self.CardStart_vBoxLayout.addWidget(StrongBodyLabel_MultiLimit)
        BodyLabel_MultiLimit = BodyLabel()
        BodyLabel_MultiLimit.setText("[可选]选择列表多项翻译工具一次显示的词条数量上限，单词条翻译工具不受影响。\n"
                                     "适当减小数量上限有助于提升工具启动速度，在启动工具后您可以前后翻页（每页数量上限不变）。")
        self.CardStart_vBoxLayout.addWidget(BodyLabel_MultiLimit)

        ButtonLayout = QHBoxLayout()
        self.CardStart_vBoxLayout.addLayout(ButtonLayout)
        self.ButtonGroup = QButtonGroup()
        self.Button_100 = RadioButton()
        self.Button_100.setText("100")
        self.Button_200 = RadioButton()
        self.Button_200.setText("200")
        self.Button_300 = RadioButton()
        self.Button_300.setText("300")
        self.Button_500 = RadioButton()
        self.Button_500.setText("500")
        self.Button_1000 = RadioButton()
        self.Button_1000.setText("1000")
        self.Button_ALL = RadioButton()
        self.Button_ALL.setText("全部")
        self.ButtonGroup.addButton(self.Button_100)
        self.ButtonGroup.addButton(self.Button_200)
        self.ButtonGroup.addButton(self.Button_300)
        self.ButtonGroup.addButton(self.Button_500)
        self.ButtonGroup.addButton(self.Button_1000)
        self.ButtonGroup.addButton(self.Button_ALL)
        self.ButtonGroup.setId(self.Button_100, 100)
        self.ButtonGroup.setId(self.Button_200, 200)
        self.ButtonGroup.setId(self.Button_300, 300)
        self.ButtonGroup.setId(self.Button_500, 500)
        self.ButtonGroup.setId(self.Button_1000, 1000)
        self.ButtonGroup.setId(self.Button_ALL, 0)
        ButtonLayout.addWidget(self.Button_100)
        ButtonLayout.addWidget(self.Button_200)
        ButtonLayout.addWidget(self.Button_300)
        ButtonLayout.addWidget(self.Button_500)
        ButtonLayout.addWidget(self.Button_1000)
        ButtonLayout.addWidget(self.Button_ALL)
        self.Button_100.setChecked(True)

        # 两张工具启动卡片
        self.layout.addWidget(self.CardSingle.widget)
        self.layout.addWidget(self.CardMulti.widget)

        self.CardSingle.button.clicked.connect(self.launchTool)
        self.CardMulti.button.clicked.connect(self.launchMulti)

        self.layout.addSpacerItem(self.spacer)

    def chooseImportProject(self):
        logger.debug("按下按钮，打开翻译项目工程文件选择器。")
        filePath, fileType = basicFunc.openFileDialog("请选择翻译工程文件（*.ft-translateProject.txt）",
                                                     basedPath=basicFunc.getHerePath() + "/file",
                                                     filter="*.ft-translateProject.txt;;*.txt;;*")
        logger.debug(f"用户选中下列文件作为翻译工程文件：{filePath} | {fileType}")
        if fileType == "*":
            IB.msgChooseImportProjectWarning_2(self.widget)
            logger.debug(f"由于文件类型选择为 {fileType}，已经展示严重错误警告。")
        elif fileType == "*.txt":
            IB.msgChooseImportProjectWarning_1(self.widget)
            logger.debug(f"由于文件类型选择为 {fileType}，已经展示潜在错误警告。")
        elif fileType == "*.ft-translateProject.txt":
            IB.msgChooseImportProjectSuccess(self.widget)
            logger.debug(f"由于文件类型选择为 {fileType}，已经展示鼓励信息。")
        else:
            IB.msgNoFileChosen(self.widget)
            logger.debug("由于未选中文件，已经展示错误提示信息。")
        self.LineEdit_ImportProject.setText(filePath)
        logger.info(f"选中文件 {filePath} 作为翻译工程文件。")

    def launchTool(self):
        if not self.Tool.isHidden() or not self.Multi.isHidden():
            IB.msgMultiSameWindowWarning(self.widget)
            logger.warning("尝试多开翻译器窗口，已经阻止操作并警告。")
            return None
        if not self.LineEdit_ImportProject.text():
            IB.msgNotImportProject(self.widget)
            logger.warning("未选择项目工程文件；已经阻止操作并警告。")
            return None
        self.Tool.show()
        self.Tool.setProject(self.LineEdit_ImportProject.text())
        logger.info("单词条翻译器已经启动。")

    def launchMulti(self):
        if not self.Tool.isHidden() or not self.Multi.isHidden():
            IB.msgMultiSameWindowWarning(self.widget)
            logger.warning("尝试多开翻译器窗口，已经阻止操作并警告。")
            return None
        if not self.LineEdit_ImportProject.text():
            IB.msgNotImportProject(self.widget)
            logger.warning("未选择项目工程文件；已经阻止操作并警告。")
            return None
        self.Multi.setProject(self.LineEdit_ImportProject.text(), self.ButtonGroup.checkedId())
        self.Multi.show()
        self.Multi.displayTextList()
        logger.info("列表多项翻译器已经启动。")


class TranslateToolPage(TranslateWindow):
    runSignal = Signal()

    def __init__(self, file: str = None, parent=None):
        self._isMicaEnabled = False
        self._lightBackgroundColor = QColor(243, 243, 243)
        self._darkBackgroundColor = QColor(32, 32, 32)

        super().__init__(parent=parent)
        self.setMicaEffectEnabled(True)
        qconfig.themeChangedFinished.connect(self._onThemeChangedFinished)

        self.ui = TranslateToolPageUi()
        self.ui.setupUi(self)
        self.setWindowTitle("翻译工具")

        self.logger = logging.getLogger("FanTools.TranslateToolPage")

        self.file = file
        self.currentId = 0
        self.project = funcT.TranslateProject()
        self.ui.PushButton_SaveProject.setIcon(FIC.SAVE)
        self.ui.PushButton_SaveProject.clicked.connect(lambda: self.project.saveProject(self.file))
        self.ui.PushButton_OneNext.setIcon(FIC.RIGHT_ARROW)
        self.ui.PushButton_OneNext.clicked.connect(lambda: self.displayText(self.getIdText(self.currentId + 1)))
        self.ui.PushButton_OneBefore.setIcon(FIC.LEFT_ARROW)
        self.ui.PushButton_OneBefore.clicked.connect(lambda: self.displayText(self.getIdText(self.currentId - 1)))
        self.ui.PrimaryPushButton_SaveAndContinue.setIcon(FIC.ACCEPT)
        self.ui.PrimaryPushButton_SaveAndContinue.clicked.connect(lambda: self.saveText(self.getIdText(self.currentId),
                                                                                        self.ui.TextEdit_TranslatedText.toPlainText(),
                                                                                        funcT.TranslateTag.human))
        self.ui.PrimaryPushButton_TranslateWithAPI.setIcon(FIC.APPLICATION)
        self.ui.PrimaryPushButton_TranslateWithAPI.clicked.connect(lambda: self.saveText(self.getIdText(self.currentId),
                                                                                         self.ui.TextEdit_API.toPlainText(),
                                                                                         funcT.TranslateTag.use_API))
        self.ui.ToolButton_CopyOriginalText.setIcon(FIC.COPY)
        self.ui.ToolButton_CopyOriginalText.clicked.connect(
            lambda: self.ui.TextEdit_TranslatedText.setPlainText(self.ui.TextEdit_OriginalText.toPlainText()))
        self.ui.ToggleButton_AutoTranslateWithAPI.setIcon(FIC.ROBOT)
        self.ui.PushButton_ViewProject.setIcon(FIC.BOOK_SHELF)
        self.ui.PushButton_EditAPIConfig.setIcon(FIC.EDIT)

        # 使用 API 翻译的下拉按钮
        self.ui.PrimarySplitPushButton_API.clicked.connect(
            lambda: self.translateWithAPI(self.getIdText(self.currentId).originalText))  # 点击使用默认翻译 API
        ButtonMenu_API = RoundMenu(parent=self.ui.PrimarySplitPushButton_API)
        ButtonMenu_API.addAction(Action(text="百度通用文本翻译API", triggered=lambda: self.translateWithAPI(
            self.getIdText(self.currentId).originalText, apiFunc=funcT.fanyi_baidu)))
        ButtonMenu_API.addAction(Action(text="有道文本翻译API", triggered=lambda: self.translateWithAPI(
            self.getIdText(self.currentId).originalText, apiFunc=funcT.fanyi_youdao)))
        self.ui.PrimarySplitPushButton_API.setFlyout(ButtonMenu_API)

        # 顶部右侧的下拉按钮
        ButtonMenu_Quick = RoundMenu(parent=self.ui.SplitPushButton)
        ButtonMenu_Quick.addAction(
            Action(icon=FIC.PLAY, text="从最靠前的未翻译词条开始", triggered=lambda: self.continueLastText()))
        ButtonMenu_Quick.addAction(Action(icon=FIC.ZOOM_OUT, text="格式化并导出翻译文本",
                                          triggered=lambda: self.project.dumpProject(funcT.FileType.JSON,
                                                                                     "output.json")))
        self.ui.SplitPushButton.setFlyout(ButtonMenu_Quick)

        # 为每个按钮都装备全新的工具提示
        buttons = [self.ui.PushButton_EditPrompt, self.ui.SplitPushButton, self.ui.PushButton_OneNext, self.ui.PushButton_OneBefore,
                   self.ui.PushButton_SaveProject, self.ui.PushButton_ViewProject, self.ui.PushButton_EditAPIConfig,
                   self.ui.PrimaryPushButton_MarkAndContinue, self.ui.PrimaryPushButton_SaveAndContinue, self.ui.PrimaryPushButton_TranslateWithAPI,
                   self.ui.ToolButton_Glossary, self.ui.ToolButton_SearchInWeb, self.ui.ToolButton_ClearTranslatedText, self.ui.ToolButton_CopyOriginalText,
                   self.ui.PrimarySplitPushButton_API, self.ui.ToggleButton_AutoTranslateWithAPI]
        for button in buttons:
            button.installEventFilter(ToolTipFilter(button))

        IB.msgLoadingReady(self)
        self.logger.info("单词条翻译工具初始化完毕。")

    def setProject(self, file: str):
        self.project.loadProject(file)
        firstText = self.getIdText(1)
        self.displayText(firstText)
        self.file = file
        self.logger.debug(f"已经将翻译项目设置为 {file}")
        return None

    def getIdText(self, id: int):
        for text in self.project.textList:
            text: funcT.TranslateText
            if text.id == id:
                self.logger.debug(f"成功获取ID为 {id} 的翻译词条对象。")
                return text
        IB.msgTextIdError(self)
        self.logger.error(f"尝试获取ID为 {id} 的翻译词条对象时失败，该ID可能超出了词条总数导致不存在。")
        return None

    def continueLastText(self):
        for text in self.project.textList:
            text: funcT.TranslateText
            if text.translatedText == "None":
                self.displayText(text)
                return None
        self.logger.info("所有条目均已翻译完毕。")
        return None

    def displayText(self, text: funcT.TranslateText):
        # 如果没有返回正确的 text，则不对 UI 进行任何操作。
        if not text:
            return None
        self.ui.SubtitleLabel.setText(
            f"共有 {self.project.n} 个翻译条目；当前条目ID：{text.id}；条目标签（Tag）：{text.translateTag}")
        self.ui.TextEdit_OriginalText.setText(text.originalText)
        if text.translatedText != "None":
            self.ui.TextEdit_TranslatedText.setText(text.translatedText)
        else:
            self.ui.TextEdit_TranslatedText.clear()
        self.ui.TextEdit_API.clear()
        self.currentId = text.id
        self.logger.debug(f"翻译器条目刷新完毕（{text.id}）。")

        # 检查是否重复，如果是的话则直接复制已有的翻译 TODO:要先弹出信息框进行询问！或在存在指定参数时才直接复制
        if self.ui.TextEdit_TranslatedText.toPlainText() == "":
            for text_ in self.project.textList:
                text_: funcT.TranslateText
                if text_.translatedText != "None":
                    if text_.originalText == text.originalText:
                        self.saveText(text, text_.translatedText, funcT.TranslateTag.repeat, False)
                        break
        return None

    def displayIDText(self, id: int):
        self.displayText(self.getIdText(id))
        return None

    def saveText(self, text: funcT.TranslateText, translatedText: str, translateTag: str, oneNext: bool = True):
        if translatedText != "":
            text.translatedText = translatedText
        else:
            text.translatedText = "None"
        if text.translateTag == "None":
            text.translateTag = f";{translateTag}"
        elif translateTag in text.translateTag:
            pass
        else:
            text.translateTag += f";{translateTag}"
        if oneNext:
            self.displayText(self.getIdText(self.currentId + 1))
        else:
            self.displayText(self.getIdText(self.currentId))
        self.logger.debug("保存翻译文本成功。")
        return None

    def translateWithAPI(self, originalText: str, originalLan: str = "en", targetLan: str = "zh",
                         displayInWindow: bool = True, apiFunc: staticmethod = funcT.fanyi_baidu):
        if self.ui.ToggleButton_AutoTranslateWithAPI.isChecked():
            self.logger.debug("用户启用了自动翻译，正在准备启动 AT 线程。")
            self.autoTranslate(originalLan, targetLan, apiFunc)
        else:
            rule = Rule()
            originalText = rule.translate_rule(originalText)
            targetText = apiFunc(originalText, originalLan, targetLan)
            targetText = rule.reborn_rule(targetText)
            if displayInWindow:
                self.ui.TextEdit_API.setText(targetText)
                self.logger.debug("已执行一次API调用翻译，并在屏幕上打印翻译结果，等待指示。")
                return None
            else:
                self.logger.debug("已执行一次API调用翻译，并以函数返回值形式返回翻译结果。")
                return targetText

    def autoTranslate(self, originalLan: str = "en", targetLan: str = "zh", apiFunc: staticmethod = funcT.fanyi_baidu):
        self.Thread_AT = QThread(self)
        self.Worker_AT = Worker_AutoTranslate(self.project, self.currentId, originalLan, targetLan, apiFunc)
        self.Worker_AT.moveToThread(self.Thread_AT)
        self.Worker_AT.targetIdSignal.connect(self.displayIDText)
        self.Worker_AT.targetTextSignal.connect(self.updateAPIText)
        self.runSignal.connect(self.Worker_AT.run)
        self.Thread_AT.start()
        self.runSignal.emit()

    def updateAPIText(self, targetText):
        if self.getIdText(self.currentId).translatedText != "None":
            self.logger.info(f"翻译已存在（{self.currentId}），跳过此条目。")
        else:
            self.ui.TextEdit_API.setText(targetText)
            self.saveText(self.getIdText(self.currentId), targetText, funcT.TranslateTag.use_API, False)
            self.logger.info(f"自动翻译结果（{self.currentId} | {targetText}）已应用并保存。")

        # 检测是否关闭自动翻译
        if not self.ui.ToggleButton_AutoTranslateWithAPI.isChecked():
            self.logger.info("用户取消自动翻译，当前翻译条目未应用。")
            self.Thread_AT.terminate()
            self.logger.debug("AT 线程已退出。")
        return None


class Worker_AutoTranslate(QObject):
    targetIdSignal = Signal(int)
    targetTextSignal = Signal(str)

    def __init__(self, project: funcT.TranslateProject, startId: int, originalLan: str = "en", targetLan: str = "zh",
                 apiFunc: staticmethod = funcT.fanyi_baidu):
        super().__init__()

        self.project = project
        self.originalLan = originalLan
        self.targetLan = targetLan
        self.startId = startId
        self.apiFunc = apiFunc

    def getIdText(self, id: int):
        for text in self.project.textList:
            text: funcT.TranslateText
            if text.id == id:
                return text
        raise

    def run(self):
        from time import sleep
        n = self.startId
        self.logger.info(f"自动翻译正在激活，准备从 {n} 开始翻译。")
        while True:
            if n > self.project.n:
                self.logger.info(f"自动翻译已结束（{n}）。")
                break
            rule = Rule()
            originalText = rule.translate_rule(self.getIdText(n).originalText)
            targetText = self.apiFunc(originalText, self.originalLan, self.targetLan)
            targetText = rule.reborn_rule(targetText)
            self.targetIdSignal.emit(n)
            self.targetTextSignal.emit(targetText)
            self.logger.info(f"已完成一次自动翻译（{n}）。")
            sleep(1)
            n += 1


class TranslateMultiPage(TranslateWindow):
    def __init__(self, parent=None):
        self._isMicaEnabled = False
        self._lightBackgroundColor = QColor(243, 243, 243)
        self._darkBackgroundColor = QColor(32, 32, 32)

        super().__init__(parent=parent)
        self.setMicaEffectEnabled(True)
        qconfig.themeChangedFinished.connect(self._onThemeChangedFinished)

        self.ui = TranslateMultiPageUi()
        self.ui.setupUi(self)
        self.setWindowTitle("列表多项翻译工具")
        self.logger = logging.getLogger("FanTools.TranslateMultiPage")

        self.cardList = []
        self.limit = 0
        self.start = 0
        self.file = None

        self.project = funcT.TranslateProject()
        self.List = QWidget()
        self.layout = VBoxLayout(parent=self.List)
        self.List.setLayout(self.layout)
        self.ui.SingleDirectionScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ui.SingleDirectionScrollArea.setWidget(self.List)
        self.ui.SingleDirectionScrollArea.setWidgetResizable(True)

        self.ui.PushButton_PageBefore.clicked.connect(lambda: self.displayTextList(self.start - self.limit))
        self.ui.PushButton_PageAfter.clicked.connect(lambda: self.displayTextList(self.start + self.limit))

    def setProject(self, file: str, limit: int):
        self.project.loadProject(file)
        self.file = file
        self.limit = limit
        n = len(self.project.textList)
        self.logger.debug(f"项目加载完毕，词条总数为 {n} （{file} | {limit}）")

    def displayTextList(self, start: int = 0):
        bar = IB.msgMultiLoading(self)

        self.start = start
        cList = list(range(len(self.layout.widgets)))
        cList.reverse()
        for i in cList:
            item = self.layout.itemAt(i)
            if item:
                if item.widget():
                    item.widget().deleteLater()
            QApplication.processEvents()
        self.logger.debug("已清空列表中的已存在词条。")

        if self.limit == 0:
            self.ui.PushButton_PageBefore.setDisabled(True)
            self.ui.PushButton_PageAfter.setDisabled(True)
            for text in self.project.textList:
                text: TranslateText
                w = TranslateTextCard(id=str(text.id), tags="None")
                w.setup(text.originalText, text.translatedText)
                w.update.connect(self.updateProjectText)
                self.layout.addWidget(w.widget)
                QApplication.processEvents()
            self.logger.debug("已在列表中显示全部词条。")
        elif self.limit > 0:
            self.ui.PushButton_PageBefore.setEnabled(True)
            self.ui.PushButton_PageAfter.setEnabled(True)
            end = start + self.limit
            for text in self.project.textList[start:end]:
                text: TranslateText
                w = TranslateTextCard(id=str(text.id), tags="None")
                w.setup(text.originalText, text.translatedText)
                w.update.connect(self.updateProjectText)
                self.layout.addWidget(w.widget)
                QApplication.processEvents()
            self.logger.debug(f"已在列表中显示部分词条：[{start}-{end}]")
        else:
            raise
        bar.close()
        IB.msgLoadingReady(self)
        self.logger.info("列表词条翻译器的列表加载完毕。")

    def getIdText(self, id: int):
        for text in self.project.textList:
            text: funcT.TranslateText
            if int(text.id) == int(id):
                self.logger.debug(f"成功获取ID为 {id} 的翻译词条对象。")
                return text
        IB.msgTextIdError(self)
        self.logger.error(f"尝试获取ID为 {id} 的翻译词条对象时失败，该ID可能超出了词条总数导致不存在。）")
        return None

    def updateProjectText(self, pack: tuple):
        text = self.getIdText(pack[0])
        text.translatedText = pack[1]
        logger.debug(f"已经更新ID为 {pack[0]} 的翻译词条。")

    def saveProject(self):
        self.project.saveProject(file=self.file)


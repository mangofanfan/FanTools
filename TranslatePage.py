import logging

from PySide2 import QtCore
from PySide2.QtCore import QObject, Signal, QThread
from PySide2.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QApplication, QHBoxLayout, QVBoxLayout, QButtonGroup
from qfluentwidgets import FluentIcon as FIC, RadioButton
from qfluentwidgets import VBoxLayout, PushButton, RoundMenu, Action, TitleLabel, BodyLabel, SingleDirectionScrollArea, \
    HeaderCardWidget, LineEdit, StrongBodyLabel

import widget.InfoBar as IB
import widget.function_translate as funcT
from script.translate_rule import Rule
from widget.TranslateButtonCard import Card_Single, Card_Multi
from widget.TranslateMultiPage import Ui_Form as TranslateMultiPageUi
from widget.TranslateTextCard import Card as TranslateTextCard
from widget.TranslateToolPage import Ui_Form as TranslateToolPageUi
from widget.function import basicFunc

logger = logging.getLogger("FanTools.TranslatePage")


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

        self.Multi.updateLoadingStatus.connect(self.updateMultiLoadingStatus)

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
                                     "多项翻译工具仍然会在启动前花费同样的时间初始化项目，时间长短由项目体量决定，不会随设置变化。")
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
        self.Button_300.setChecked(True)

        # 两张工具启动卡片
        self.layout.addWidget(self.CardSingle.widget)
        self.layout.addWidget(self.CardMulti.widget)

        self.CardSingle.button.clicked.connect(self.launchTool)
        self.CardMulti.button.clicked.connect(self.launchMulti)

        self.layout.addSpacerItem(self.spacer)

    def chooseImportProject(self):
        logger.debug("按下按钮，打开翻译项目工程文件选择器。")
        filePath, fileType = basicFunc.openFileDialog("请选择翻译工程文件（*.ft-translateProject.txt）",
                                                     basedPath=basicFunc.getHerePath(),
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
            raise
        self.LineEdit_ImportProject.setText(filePath)
        logger.info(f"选中文件 {filePath} 作为翻译工程文件。")

    def launchTool(self):
        if not self.LineEdit_ImportProject.text():
            IB.msgNotImportProject(self.widget)
            logger.warning("未选择项目工程文件；已经向用户显示警告。")
            return None
        self.Tool.show()
        self.Tool.setProject(self.LineEdit_ImportProject.text())
        logger.info("单词条翻译器已经启动。")

    def launchMulti(self):
        if not self.LineEdit_ImportProject.text():
            IB.msgNotImportProject(self.widget)
            logger.warning("未选择项目工程文件；已经向用户显示警告。")
            return None
        logger.info("开始加载列表多项翻译器。")
        self.Multi.setProject(self.LineEdit_ImportProject.text(), self.ButtonGroup.checkedId())
        self.Multi.show()
        self.Multi.displayTextList()
        logger.info("列表多项翻译器已经启动。")

    def updateMultiLoadingStatus(self, numberCount: tuple):
        if self.CardMulti.progressBar.isHidden():
            self.CardMulti.progressBar.setRange(0, 100)
            self.CardMulti.progressBar.setValue(0)
            self.CardMulti.progressBar.setHidden(False)

        value = (numberCount[0] / numberCount[1]) * 100
        self.CardMulti.progressBar.setValue(value)

        if value == 100:
            self.CardMulti.progressBar.setHidden(True)


class TranslateToolPage(QWidget):
    runSignal = Signal()

    def __init__(self, file: str = None, parent=None):
        QWidget.__init__(self, parent)

        self.ui = TranslateToolPageUi()
        self.ui.setupUi(self)
        self.setWindowTitle("翻译工具")

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

    def setProject(self, file: str):
        self.project.loadProject(file)
        firstText = self.getIdText(1)
        self.displayText(firstText)
        self.file = file

    def getIdText(self, id: int):
        for text in self.project.textList:
            text: funcT.TranslateText
            if text.id == id:
                return text
        IB.msgTextIdError(self)
        return None

    def continueLastText(self):
        for text in self.project.textList:
            text: funcT.TranslateText
            if text.translatedText == "None":
                self.displayText(text)
                return None
        print("好像都翻译完了，好耶~")
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
        return None

    def translateWithAPI(self, originalText: str, originalLan: str = "en", targetLan: str = "zh",
                         displayInWindow: bool = True, apiFunc: staticmethod = funcT.fanyi_baidu):
        if self.ui.ToggleButton_AutoTranslateWithAPI.isChecked():
            self.autoTranslate(originalLan, targetLan, apiFunc)
        else:
            rule = Rule()
            originalText = rule.translate_rule(originalText)
            targetText = apiFunc(originalText, originalLan, targetLan)
            targetText = rule.reborn_rule(targetText)
            if displayInWindow:
                self.ui.TextEdit_API.setText(targetText)
                return None
            else:
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
            print(f"翻译已存在（{self.currentId}），跳过此条目。")
        else:
            self.ui.TextEdit_API.setText(targetText)
            self.saveText(self.getIdText(self.currentId), targetText, funcT.TranslateTag.use_API, False)

        # 检测是否关闭自动翻译
        if not self.ui.ToggleButton_AutoTranslateWithAPI.isChecked():
            print("退出 AT 线程。")
            self.Thread_AT.terminate()
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
        logger.info(f"自动翻译正在激活，准备从 {n} 开始翻译。")
        while True:
            if n > self.project.n:
                logger.info(f"自动翻译已结束（{n}）。")
                break
            rule = Rule()
            originalText = rule.translate_rule(self.getIdText(n).originalText)
            targetText = self.apiFunc(originalText, self.originalLan, self.targetLan)
            targetText = rule.reborn_rule(targetText)
            self.targetIdSignal.emit(n)
            self.targetTextSignal.emit(targetText)
            logger.info(f"已完成一次自动翻译（{n}）。")
            sleep(1)
            n += 1


class TranslateMultiPage(QWidget):
    updateLoadingStatus = Signal(tuple)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.ui = TranslateMultiPageUi()
        self.ui.setupUi(self)
        self.setWindowTitle("列表多项翻译工具")

        self.cardList = []
        self.limit = 0

        self.project = funcT.TranslateProject()
        self.List = QWidget()
        self.layout = VBoxLayout(parent=self.List)
        self.List.setLayout(self.layout)
        self.ui.SingleDirectionScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ui.SingleDirectionScrollArea.setWidget(self.List)
        self.ui.SingleDirectionScrollArea.setWidgetResizable(True)

    def setProject(self, file: str, limit: int):
        self.project.loadProject(file)
        self.limit = limit

        n = len(self.project.textList)
        i = 1
        for text in self.project.textList:
            text: funcT.TranslateText
            card = TranslateTextCard(titleLabel=str(text.id))
            self.cardList.append(card)
            self.updateLoadingStatus.emit((i, n))
            i += 1
            QApplication.processEvents()

    def displayTextList(self, start: int = 0):
        for cardWidget in self.layout.widgets:
            self.layout.removeWidget(cardWidget)

        if self.limit == 0:
            self.ui.PushButton_PageBefore.setDisabled(True)
            self.ui.PushButton_PageAfter.setDisabled(True)
            for w in self.cardList:
                w: TranslateTextCard
                self.layout.addWidget(w.widget)
        elif self.limit > 0:
            self.ui.PushButton_PageBefore.setEnabled(True)
            self.ui.PushButton_PageAfter.setEnabled(True)
            end = start + self.limit
            for w in self.cardList[start:end]:
                w: TranslateTextCard
                self.layout.addWidget(w.widget)
        else:
            raise



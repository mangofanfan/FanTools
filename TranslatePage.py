import logging
from functools import partial
from pathlib import Path

from PySide2 import QtCore
from PySide2.QtCore import QObject, Signal, QThread, QSize
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QHBoxLayout, QVBoxLayout, QButtonGroup, QApplication, \
    QFrame, QListWidgetItem, QTableWidgetItem
from qfluentwidgets import FluentIcon as FIC, RadioButton, ToolTipFilter, TextEdit, SwitchSettingCard, ToolButton, \
    MessageBox
from qfluentwidgets import VBoxLayout, PushButton, RoundMenu, Action, TitleLabel, BodyLabel, SingleDirectionScrollArea, \
    HeaderCardWidget, LineEdit, StrongBodyLabel

import widget.function_translate as funcT
import widget.function_translateMsg as IB
from script.translate_rule import Rule
from widget import function_setting as funcS
from widget.TranslateButtonCard import Card_Single, Card_Multi, Card_Glossary
from widget.TranslateGlossary import Ui_Form as TranslateGlossaryUi
from widget.TranslateMultiPage import Ui_Form as TranslateMultiPageUi
from widget.TranslateTextCard import Card as TranslateTextCard
from widget.TranslateToolPage import Ui_Form as TranslateToolPageUi
from widget.TranslateCreateProject import Ui_Form as TranslateCreateProjectUi
from widget.Window import TranslateWindow, GlossaryTableWidget
from widget.function import basicFunc

logger = logging.getLogger("FanTools.TranslatePage")


class TranslatePage(QObject):

    def __init__(self):
        super().__init__()
        self.widget = QFrame()
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
        self.CardGlossary = Card_Glossary()

        self.history = funcT.history()
        self.historyMenu = RoundMenu()

        self.Tool = TranslateToolPage()
        self.Multi = TranslateMultiPage()
        self.Glossary = GlossaryWindow()
        self.Create = CreateProjectWindow(self.history)

        self.Tool.glossarySignal.connect(self.launchGlossary)
        self.Multi.glossarySignal.connect(self.launchGlossary)
        self.Create.newProjectSignal.connect(self.createProject)

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

        StrongBodyLabel_CreateProject = StrongBodyLabel()
        StrongBodyLabel_CreateProject.setText("创建翻译项目")
        self.CardStart_vBoxLayout.addWidget(StrongBodyLabel_CreateProject)
        BodyLabel_CreateProject = BodyLabel()
        BodyLabel_CreateProject.setText("根据源语言文件创建新的翻译项目。")
        self.CardStart_vBoxLayout.addWidget(BodyLabel_CreateProject)
        self.PushButton_CreateProject = PushButton()
        self.PushButton_CreateProject.setText("根据源语言文件创建项目")
        self.PushButton_CreateProject.setFixedHeight(30)
        self.PushButton_CreateProject.clicked.connect(self.launchCreate)
        self.CardStart_vBoxLayout.addWidget(self.PushButton_CreateProject)

        self.CardStart_vBoxLayout.addSpacing(20)

        StrongBodyLabel_ImportProject = StrongBodyLabel()
        StrongBodyLabel_ImportProject.setText("加载翻译项目")
        self.CardStart_vBoxLayout.addWidget(StrongBodyLabel_ImportProject)
        BodyLabel_ImportProject = BodyLabel()
        BodyLabel_ImportProject.setText("您需要先将翻译工程文件导入此处，才能启动翻译工具哦！")
        self.CardStart_vBoxLayout.addWidget(BodyLabel_ImportProject)

        self.Layout_ImportProject = QHBoxLayout()
        self.CardStart_vBoxLayout.addLayout(self.Layout_ImportProject)
        self.LineEdit_ImportProject = LineEdit()
        self.LineEdit_ImportProject.setFixedHeight(30)
        self.Layout_ImportProject.addWidget(self.LineEdit_ImportProject)
        self.PushButton_ImportProject = PushButton()
        self.PushButton_ImportProject.setFixedHeight(30)
        self.PushButton_ImportProject.setFixedWidth(100)
        self.PushButton_ImportProject.setText("选择文件")
        self.PushButton_ImportProject.clicked.connect(self.chooseImportProject)
        self.Layout_ImportProject.addWidget(self.PushButton_ImportProject)
        self.ToolButton_History = ToolButton()
        self.ToolButton_History.setIcon(FIC.HISTORY)
        self.ToolButton_History.setFixedHeight(30)
        self.ToolButton_History.clicked.connect(self.viewHistory)
        self.Layout_ImportProject.addWidget(self.ToolButton_History)

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

        # 三张工具启动卡片
        self.layout.addWidget(self.CardSingle.widget)
        self.layout.addWidget(self.CardMulti.widget)
        self.layout.addWidget(self.CardGlossary.widget)

        self.CardSingle.button.clicked.connect(self.launchTool)
        self.CardMulti.button.clicked.connect(self.launchMulti)
        self.CardGlossary.button.clicked.connect(self.launchGlossary)

        self.layout.addSpacerItem(self.spacer)
        return None

    def createProject(self, project: funcT.TranslateProject, name: str):
        self.history.add(project.projectFile, name)
        self.LineEdit_ImportProject.setText(project.projectFile)
        return None

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
        self.history.add(self.LineEdit_ImportProject.text())
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
        self.history.add(self.LineEdit_ImportProject.text())
        logger.info("列表多项翻译器已经启动。")
        return None

    def launchGlossary(self):
        if not self.LineEdit_ImportProject.text():
            IB.msgNotImportProject(self.widget)
            logger.warning("未选择项目工程文件；已经阻止操作并警告。")
            return None
        self.Glossary.setProjectFile(self.LineEdit_ImportProject.text().replace("ft-translateProject.txt", "ft-translateGlossary.txt"))
        self.Glossary.loadProjectFile()
        logger.info("术语表窗口启动。")
        self.history.add(self.LineEdit_ImportProject.text())
        self.Glossary.show()
        return None

    def launchCreate(self):
        logger.info("创建翻译工程窗口启动。")
        self.Create.show()

    def viewHistory(self):
        hList = self.history.get()
        self.historyMenu.clear()
        if not hList:
            self.historyMenu.addAction(Action(icon=FIC.CLOSE, text="还没有保存的历史记录……"))
        else:
            for h in hList:
                self.historyMenu.addAction(Action(icon=FIC.PLAY, text=f"{h[1]} - {h[0]}", triggered=partial(self.LineEdit_ImportProject.setText, h[0])))
            self.historyMenu.addAction(Action(icon=FIC.DELETE, text="清空历史记录", triggered=self.history.clear))

        self.historyMenu.popup(QCursor.pos())


class TranslateToolPage(TranslateWindow):
    runSignal = Signal()
    glossarySignal = Signal()

    def __init__(self, file: str = None, parent=None):
        super().__init__(parent=parent)

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
        self.ui.PrimaryPushButton_UseAPIText.setIcon(FIC.APPLICATION)
        self.ui.PrimaryPushButton_UseAPIText.clicked.connect(lambda: self.saveText(self.getIdText(self.currentId),
                                                                                         self.ui.TextEdit_API.toPlainText(),
                                                                                         funcT.TranslateTag.use_API))
        self.ui.ToolButton_CopyOriginalText.setIcon(FIC.COPY)
        self.ui.ToolButton_CopyOriginalText.clicked.connect(
            lambda: self.ui.TextEdit_TranslatedText.setPlainText(self.ui.TextEdit_OriginalText.toPlainText()))
        self.ui.ToggleButton_AutoTranslateWithAPI.setIcon(FIC.ROBOT)
        self.ui.PushButton_ViewProject.setIcon(FIC.BOOK_SHELF)
        self.ui.PushButton_Glossary.setIcon(FIC.EDIT)
        self.ui.PushButton_Glossary.clicked.connect(self.glossarySignal.emit)

        # 选择API的下拉按钮
        for api in funcT.TranslateAPI.apiList:
            self.ui.ComboBox_API.addItem(text=api.displayName, icon=api.icon, userData=api.apiFunc)
        self.ui.ComboBox_API.setPlaceholderText("请选择API接口")
        self.ui.ComboBox_API.setCurrentIndex(-1)

        self.ui.PrimaryPushButton_TranslateWithAPI.clicked.connect(self.translateWithAPI)

        # 顶部右侧的下拉按钮
        ButtonMenu_Quick = RoundMenu(parent=self.ui.SplitPushButton)
        ButtonMenu_Quick.addAction(
            Action(icon=FIC.PLAY, text="从最靠前的未翻译词条开始", triggered=lambda: self.continueLastText()))
        ButtonMenu_Quick.addAction(Action(icon=FIC.ZOOM_OUT, text="导出翻译文本",
                                          triggered=lambda: self.project.dumpProject(funcT.FileType.JSON,
                                                                                     "output.json")))
        self.ui.SplitPushButton.setFlyout(ButtonMenu_Quick)

        # 表格
        self.ui.TableWidget.setBorderVisible(True)
        self.ui.TableWidget.setBorderRadius(8)
        self.ui.TableWidget.setWordWrap(False)

        # 为每个按钮都装备全新的工具提示
        buttons = [self.ui.PushButton_EditPrompt, self.ui.SplitPushButton, self.ui.PushButton_OneNext, self.ui.PushButton_OneBefore,
                   self.ui.PushButton_SaveProject, self.ui.PushButton_ViewProject, self.ui.PrimaryPushButton_UseAPIText,
                   self.ui.PrimaryPushButton_MarkAndContinue, self.ui.PrimaryPushButton_SaveAndContinue, self.ui.PrimaryPushButton_TranslateWithAPI,
                   self.ui.PushButton_Glossary, self.ui.ToolButton_SearchInWeb, self.ui.ToolButton_ClearTranslatedText, self.ui.ToolButton_CopyOriginalText,
                   self.ui.ComboBox_API, self.ui.ToggleButton_AutoTranslateWithAPI]
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

    def translateWithAPI(self):
        originalLan = "en"
        targetLan = "zh"
        originalText = self.ui.TextEdit_OriginalText.toPlainText()
        apiFunc = self.ui.ComboBox_API.itemData(self.ui.ComboBox_API.currentIndex())

        if not apiFunc:
            IB.msgNoAPIChosen(self)
            return None

        if self.ui.ToggleButton_AutoTranslateWithAPI.isChecked():
            self.logger.debug("用户启用了自动翻译，正在准备启动 AT 线程。")
            self.autoTranslate(originalLan, targetLan, apiFunc)
        else:
            rule = Rule()
            originalText = rule.translate_rule(originalText)
            targetText = apiFunc(originalText, originalLan, targetLan)
            targetText = rule.reborn_rule(targetText)
            self.ui.TextEdit_API.setText(targetText)
            self.logger.info("完成一次API调用翻译。")


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
    glossarySignal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.ui = TranslateMultiPageUi()
        self.ui.setupUi(self)
        self.setWindowTitle("列表多项翻译工具")
        self.logger = logging.getLogger("FanTools.TranslateMultiPage")

        self.cardList = []
        self.limit = 0
        self.start = 0
        self.file = None
        self.n = 0
        self.end = 0

        self.project = funcT.TranslateProject()
        self.List = QWidget()
        self.layout = VBoxLayout(parent=self.List)
        self.List.setLayout(self.layout)
        self.ui.SingleDirectionScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ui.SingleDirectionScrollArea.setWidget(self.List)
        self.ui.SingleDirectionScrollArea.setWidgetResizable(True)

        self.ui.PushButton_PageBefore.clicked.connect(lambda: self.displayTextList(self.start - self.limit))
        self.ui.PushButton_PageAfter.clicked.connect(lambda: self.displayTextList(self.start + self.limit))

        for api in funcT.TranslateAPI.apiList:
            self.ui.ComboBox_API.addItem(text=api.displayName, icon=api.icon, userData=api.apiFunc)

        self.ui.ComboBox_API.setPlaceholderText("选择一个API接口")
        self.ui.ComboBox_API.setCurrentIndex(-1)

        self.ui.PushButton_Glossary.clicked.connect(self.glossarySignal.emit)

        self.logger.info("列表多项翻译工具初始化完毕。")

    def setProject(self, file: str, limit: int):
        self.project.loadProject(file)
        self.file = file
        self.limit = limit
        n = len(self.project.textList)
        self.n = n
        self.logger.debug(f"项目加载完毕，词条总数为 {n} （{file} | {limit}）")

    def displayTextList(self, start: int = 0):
        bar = IB.msgMultiLoading(self)

        self.start = start
        self.cardList.clear()

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
            end = self.n
            for text in self.project.textList:
                text: funcT.TranslateText
                w = TranslateTextCard(text=text)
                w.setup(text.originalText, text.translatedText)
                w.update.connect(self.updateProjectText)
                w.translateWithAPI.connect(self.translateWithAPI)
                self.layout.addWidget(w.widget)
                self.cardList.append(w)
                QApplication.processEvents()
            self.logger.debug("已在列表中显示全部词条。")
        elif self.limit > 0:
            self.ui.PushButton_PageBefore.setEnabled(True)
            self.ui.PushButton_PageAfter.setEnabled(True)
            end = start + self.limit
            if end > self.n:
                end = self.n
            for text in self.project.textList[start:end]:
                text: funcT.TranslateText
                w = TranslateTextCard(text=text)
                w.setup(text.originalText, text.translatedText)
                w.update.connect(self.updateProjectText)
                w.translateWithAPI.connect(self.translateWithAPI)
                self.layout.addWidget(w.widget)
                self.cardList.append(w)
                QApplication.processEvents()
            self.logger.debug(f"已在列表中显示部分词条：[{start}-{end}]")
        else:
            raise
        bar.close()
        IB.msgLoadingReady(self)
        self.end = end
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
        logger.debug(f"已经更新ID为 {pack[0]} 的翻译词条为 {pack[1]}。")
        return None

    def saveProject(self):
        self.project.saveProject(file=self.file)
        return None

    def translateWithAPI(self, id: int):
        card = None
        for card in self.cardList:
            card: TranslateTextCard
            if int(card.text.id) == id:
                break
        if not card:
            # TODO：消息条预备
            logger.error("未找到发送翻译信号的词条，这可能是程序内部存在的bug，请考虑将其提交给开发者！")
            return None

        originalText = card.text.originalText

        apiFunc = self.ui.ComboBox_API.itemData(self.ui.ComboBox_API.currentIndex())
        if not apiFunc:
            IB.msgNoAPIChosen(self)
            logger.error("尝试执行API翻译，但没有选中任何API接口。")
            return None

        targetText = apiFunc(originalText)
        card.text.translatedText = targetText
        card.updateText(targetText)
        logger.info(f"成功执行一次API翻译。（ID {id} | 原文 {originalText} | 译文 {targetText}）")
        return None


class GlossaryWindow(TranslateWindow):
    def __init__(self, projectFile: str = None, name: str = None, parent=None):
        super().__init__(parent=parent)
        self.ui = TranslateGlossaryUi()
        self.ui.setupUi(self)
        self.setWindowTitle("术语表设置")
        self.logger = logging.getLogger("FanTools.TranslateGlossary")
        self.projectFile = projectFile
        self.name = name

        self.Page_Global = SingleDirectionScrollArea()
        self.Page_Global_Widget = QWidget()
        self.Page_Global_Layout = VBoxLayout(self.Page_Global_Widget)
        self.Page_Global_Widget.setLayout(self.Page_Global_Layout)
        self.Page_Global.setWidget(self.Page_Global_Widget)
        self.Page_Global.setWidgetResizable(True)

        self.ListItemGlobal = None

        self.APIDirectory = {}

        TextEdit_Tip = TextEdit()
        TextEdit_Tip.setMarkdown(basicFunc.readFile("data/glossary_tip.md"))
        TextEdit_Tip.setFixedHeight(200)
        TextEdit_Tip.setEnabled(False)
        self.Page_Global_Layout.addWidget(TextEdit_Tip)

        self.ui.PrimaryPushButton_Save.clicked.connect(self.saveGlossaryTable)

        GlobalEnableGlossary = SwitchSettingCard(configItem=funcS.cfg.GlossaryEnable,
                                                 title="启用术语表",
                                                 content="全局启用术语表，在各翻译工具中均支持。也可以在工具箱设置中设置本项目。",
                                                 icon=FIC.ERASE_TOOL)
        self.Page_Global_Layout.addWidget(GlobalEnableGlossary)

        self.addSubPage(self.Page_Global, "术语表设置")

        self.addSecondPage()

        self.ui.PopUpAniStackedWidget.setCurrentWidget(self.Page_Global)
        self.ui.PopUpAniStackedWidget.setMinimumSize(800, 600)
        self.centerWindow()
        self.ui.ListWidget.setCurrentItem(self.ListItemGlobal)
        for api in funcT.TranslateAPI.apiList:
            self.addSubAPIPage(api)

        self.ui.ListWidget.itemSelectionChanged.connect(lambda: self.changedBySelection(self.ui.ListWidget.currentRow() + 1))

        self.logger.debug("翻译术语表初始化完毕")

    def setProjectFile(self, projectFile: str):
        self.projectFile = projectFile
        self.logger.debug(f"已经启动翻译术语表工程文件 {self.projectFile} .")
        return None

    def loadProjectFile(self):
        path = Path(self.projectFile)
        if not path.exists():
            return None

        Glossary_Global = funcT.GlossaryTable(self.projectFile)
        Glossary_Global.load(self.projectFile)
        TableWidget_Global: GlossaryTableWidget = self.APIDirectory["global"]
        TableWidget_Global.setRowCount(len(Glossary_Global.lineList))
        i = 0
        for line in Glossary_Global.lineList:
            item_1 = QTableWidgetItem(line[0])
            item_2 = QTableWidgetItem(line[1])
            TableWidget_Global.setItem(i, 0, item_1)
            TableWidget_Global.setItem(i, 1, item_2)
            i += 1
        self.logger.debug(f"加载了{i}个术语表词条。")
        return None

    def changedBySelection(self, current):
        self.logger.debug(f"切换到 {current} 。")
        self.ui.PopUpAniStackedWidget.setCurrentIndex(current)

    def addSubPage(self, page: QWidget, name: str):
        self.ui.PopUpAniStackedWidget.addWidget(page)
        item = QListWidgetItem(name)
        self.ui.ListWidget.addItem(item)
        if not self.ListItemGlobal:
            self.ListItemGlobal = item
        return None

    def addSecondPage(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)

        TextEdit_GlobalGlossary = TextEdit()
        TextEdit_GlobalGlossary.setMarkdown(basicFunc.readFile("data/glossary_global_tip.md"))
        TextEdit_GlobalGlossary.setFixedHeight(50)
        TextEdit_GlobalGlossary.setEnabled(False)
        layout.addWidget(TextEdit_GlobalGlossary)

        table = GlossaryTableWidget(self)

        layout.addWidget(table)
        self.APIDirectory["global"] = table
        self.addSubPage(page, "全局术语表")

    def addSubAPIPage(self, api: funcT.TranslateAPI.Api):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)

        table = GlossaryTableWidget(self)

        layout.addWidget(table)

        self.APIDirectory[api.name] = table
        self.addSubPage(page, api.displayName)

    def saveGlossaryTable(self):
        Table_Global: GlossaryTableWidget = self.APIDirectory["global"]
        Glossary_Global = funcT.GlossaryTable(self.projectFile)
        for i in range(Table_Global.rowCount()):
            Glossary_Global.add(Table_Global.item(i, 0).text(), Table_Global.item(i, 1).text())
        Glossary_Global.save()

class CreateProjectWindow(TranslateWindow):
    newProjectSignal = Signal(funcT.TranslateProject, str)

    def __init__(self, history: funcT.history, parent=None):
        super().__init__(parent=parent)
        self.ui = TranslateCreateProjectUi()
        self.ui.setupUi(self)
        self.setResizeEnabled(False)
        self.setFixedSize(QSize(600, 600))
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)
        self.setWindowTitle("创建翻译项目")
        self.update()

        self.history = history
        self.logger = logging.getLogger("FanTools.TranslateCreateProjectWindow")

        self.ui.SimpleCardWidget_Json.clicked.connect(lambda: self.ui.PopUpAniStackedWidget.setCurrentIndex(0))
        self.ui.SimpleCardWidget_Copy.clicked.connect(lambda: self.ui.PopUpAniStackedWidget.setCurrentIndex(1))

        self.ui.PopUpAniStackedWidget.setCurrentIndex(0)

        self.setUp()

    def setUp(self):
        self.ui.PlainTextEdit_Json_Example.setPlainText(basicFunc.readFile("/data/example/en_us.json"))
        self.ui.PushButton_Json_ImportFile.clicked.connect(self.chooseImportJson)
        self.ui.LineEdit_Json_ImportFile.setPlaceholderText("输入或从右侧按钮打开文件选择器……")
        self.ui.PrimaryPushButton_Json_Create.clicked.connect(lambda: self.createProject(funcT.FileType.JSON, self.ui.LineEdit_Json_ImportFile.text()))

    def chooseImportJson(self):
        self.logger.debug("按下按钮，打开Json文件选择器。")
        filePath, fileType = basicFunc.openFileDialog("请选择Json文件（*.json）",
                                                      basedPath=basicFunc.getHerePath() + "/file",
                                                      filter="*.json")
        if not filePath or not fileType:
            return None
        self.logger.debug(f"用户选中下列文件作为Json导入：{filePath} | {fileType}")
        self.ui.LineEdit_Json_ImportFile.setText(filePath)
        return None

    def createProject(self, fileType: funcT.FileType.Suffix, filePath: str):
        def create():
            name = w.LineEdit_InputProjectName.text()
            if not name:
                IB.msgNoInputName(self)
                return None
            for h in self.history.get():
                if name == h[1]:
                    IB.msgNameNotAllowed(self)
                    return None
            project = funcT.TranslateProject()
            project.startProject(fileType, filePath, name)
            self.newProjectSignal.emit(project, name)
            w.close()
            self.close()
            return None

        def cancel():
            w.close()

        w = MessageBox(title="为新的翻译项目取个名字吧！",
                       content="您需要为此新翻译项目取个独一无二的名字，翻译工具会将其作为项目工程文件的前缀名。",
                       parent=self)

        w.LineEdit_InputProjectName = LineEdit()
        w.LineEdit_InputProjectName.setPlaceholderText("请输入项目名称……")
        w.textLayout.addWidget(w.LineEdit_InputProjectName)
        w.yesButton.setText("确认创建项目")
        w.yesSignal.connect(create)
        w.cancelButton.setText("取消创建并返回")
        w.cancelSignal.connect(cancel)

        w.show()


        return None


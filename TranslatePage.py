from PySide2.QtCore import QObject, Signal, QThread
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QLabel, QSpacerItem, QSizePolicy
from qfluentwidgets import VBoxLayout, PushButton, RoundMenu, Action, TitleLabel, BodyLabel
from qfluentwidgets import FluentIcon as FIC

import webbrowser

from widget.function import basicFunc
import widget.function_translate as funcT
from widget.TranslateToolPage import Ui_Form as TranslateToolPageUi
from script.translate_rule import Rule


class TranslatePage:
    def __init__(self):
        self.widget = QWidget()
        self.widget.setObjectName("TranslatePage")
        self.layout = VBoxLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.spacer = QSpacerItem(1000, 1000, hData=QSizePolicy.Maximum, vData=QSizePolicy.Maximum)
        self.run()

    def addTextLine(self, text: str, labelType: str = "Body"):
        if labelType == "Title":
            label = TitleLabel()
        else:
            label = BodyLabel()
        label.setText(text)
        self.layout.addWidget(label)

    def run(self):
        self.addTextLine("翻译工具", "Title")
        self.addTextLine("测试中，点击下方按钮打开工具……")

        self.layout.addSpacerItem(self.spacer)

        PushButton_Run = PushButton(self.widget)
        PushButton_Run.setText("启动工具")
        PushButton_Run.clicked.connect(self.launch)
        self.layout.addWidget(PushButton_Run)

    def launch(self):
        global Tool
        Tool = TranslateToolPage()
        Tool.show()
        Tool.setProject("testAAA.txt")


class TranslateToolPage(QWidget):
    runSignal = Signal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.ui = TranslateToolPageUi()
        self.ui.setupUi(self)
        self.setWindowTitle("翻译工具")

        self.currentId = 0
        self.project = funcT.TranslateProject()
        self.ui.PushButton_SaveProject.setIcon(FIC.SAVE)
        self.ui.PushButton_SaveProject.clicked.connect(lambda: self.project.saveProject(file="testAAA.txt"))
        self.ui.PushButton_OneNext.setIcon(FIC.RIGHT_ARROW)
        self.ui.PushButton_OneNext.clicked.connect(lambda: self.displayText(self.getIdText(self.currentId + 1)))
        self.ui.PushButton_OneBefore.setIcon(FIC.LEFT_ARROW)
        self.ui.PushButton_OneBefore.clicked.connect(lambda: self.displayText(self.getIdText(self.currentId - 1)))
        self.ui.PrimaryPushButton_SaveAndContinue.setIcon(FIC.ACCEPT)
        self.ui.PrimaryPushButton_SaveAndContinue.clicked.connect(lambda: self.saveText(self.getIdText(self.currentId),
                                                                                        self.ui.PlainTextEdit_TranslatedText.toPlainText(),
                                                                                        funcT.TranslateTag.human))
        self.ui.PrimaryPushButton_TranslateWithAPI.setIcon(FIC.APPLICATION)
        self.ui.PrimaryPushButton_TranslateWithAPI.clicked.connect(lambda: self.saveText(self.getIdText(self.currentId),
                                                                                         self.ui.TextEdit_API.toPlainText(),
                                                                                         funcT.TranslateTag.use_API))
        self.ui.ToolButton_CopyOriginalText.setIcon(FIC.COPY)
        self.ui.ToolButton_CopyOriginalText.clicked.connect(lambda: self.ui.PlainTextEdit_TranslatedText.setPlainText(self.ui.PlainTextEdit_OriginalText.toPlainText()))
        self.ui.ToggleButton_AutoTranslateWithAPI.setIcon(FIC.ROBOT)
        self.ui.PushButton_ViewProject.setIcon(FIC.BOOK_SHELF)
        self.ui.PushButton_EditAPIConfig.setIcon(FIC.EDIT)

        # 使用 API 翻译的下拉按钮
        self.ui.PrimarySplitPushButton_API.clicked.connect(lambda: self.translateWithAPI(self.getIdText(self.currentId).originalText))  # 点击使用默认翻译 API
        ButtonMenu_API = RoundMenu(parent=self.ui.PrimarySplitPushButton_API)
        ButtonMenu_API.addAction(Action(text="百度通用文本翻译API", triggered=lambda: self.translateWithAPI(self.getIdText(self.currentId).originalText, apiFunc=funcT.fanyi_baidu)))
        ButtonMenu_API.addAction(Action(text="有道文本翻译API", triggered=lambda: self.translateWithAPI(self.getIdText(self.currentId).originalText, apiFunc=funcT.fanyi_youdao)))
        self.ui.PrimarySplitPushButton_API.setFlyout(ButtonMenu_API)

        # 顶部右侧的下拉按钮
        ButtonMenu_Quick = RoundMenu(parent=self.ui.SplitPushButton)
        ButtonMenu_Quick.addAction(Action(icon=FIC.PLAY, text="从最近的未翻译词条开始", triggered=lambda: self.continueLastText()))
        self.ui.SplitPushButton.setFlyout(ButtonMenu_Quick)


    def setProject(self, file: str):
        self.project.loadProject(file)
        firstText = self.getIdText(1)
        self.displayText(firstText)

    def getIdText(self, id: int):
        for text in self.project.textList:
            text: funcT.TranslateText
            if text.id == id:
                return text
        raise

    def continueLastText(self):
        for text in self.project.textList:
            text: funcT.TranslateText
            if text.translatedText == "None":
                self.displayText(text)
                return None
        print("好像都翻译完了，好耶~")
        return None

    def displayText(self, text: funcT.TranslateText):
        self.ui.SubtitleLabel.setText(f"共有 {self.project.n} 个翻译条目；当前条目ID：{text.id}；条目标签（Tag）：{text.translateTag}")
        self.ui.PlainTextEdit_OriginalText.setPlainText(text.originalText)
        if text.translatedText != "None":
            self.ui.PlainTextEdit_TranslatedText.setPlainText(text.translatedText)
        else:
            self.ui.PlainTextEdit_TranslatedText.clear()
        self.ui.TextEdit_API.clear()
        self.currentId = text.id

        # 检查是否重复，如果是的话则直接复制已有的翻译
        if self.ui.PlainTextEdit_TranslatedText.toPlainText() == "":
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

    def translateWithAPI(self, originalText: str, originalLan: str = "en", targetLan: str = "zh", displayInWindow: bool = True, apiFunc: staticmethod = funcT.fanyi_baidu):
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

    def __init__(self, project: funcT.TranslateProject, startId: int, originalLan: str = "en", targetLan: str = "zh", apiFunc: staticmethod = funcT.fanyi_baidu):
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
        print(f"从 {n} 开始翻译。")
        while True:
            if n > self.project.n:
                print(f"自动翻译已结束（{n}）。")
                break
            rule = Rule()
            originalText = rule.translate_rule(self.getIdText(n).originalText)
            targetText = self.apiFunc(originalText, self.originalLan, self.targetLan)
            targetText = rule.reborn_rule(targetText)
            self.targetIdSignal.emit(n)
            self.targetTextSignal.emit(targetText)
            print(f"已完成一次 API 翻译（{n}）。")
            sleep(1)
            n += 1


from PySide2.QtCore import QObject, Signal, QThread
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QWidget, QLabel, QSpacerItem, QSizePolicy
from qfluentwidgets import VBoxLayout, PushButton, setTheme, Theme, RoundMenu, Action
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

    def addTextLine(self, text: str, idName: str = None, alignment=Qt.AlignLeft):
        textLine = QLabel(text=text)
        if idName:
            textLine.setObjectName(idName)
        self.layout.addWidget(textLine, alignment=alignment)

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
        Tool.setProject("testAAA")


class TranslateToolPage(QWidget):
    runSignal = Signal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.ui = TranslateToolPageUi()
        self.ui.setupUi(self)
        self.setStyleSheet("")

        self.currentId = 0
        self.project = funcT.TranslateProject()
        self.ui.PushButton_SaveProject.clicked.connect(lambda: self.project.saveProject(file="testAAA"))
        self.ui.PushButton_OneNext.clicked.connect(lambda: self.displayText(self.getIdText(self.currentId + 1)))
        self.ui.PushButton_OneBefore.clicked.connect(lambda: self.displayText(self.getIdText(self.currentId - 1)))
        self.ui.PrimaryPushButton_SaveAndContinue.clicked.connect(lambda: self.saveText(self.getIdText(self.currentId),
                                                                                        self.ui.PlainTextEdit_TranslatedText.toPlainText(),
                                                                                        funcT.TranslateTag.human))
        self.ui.PrimarySplitPushButton_API.clicked.connect(lambda: self.translateWithAPI(self.getIdText(self.currentId).originalText))
        self.ui.PrimaryPushButton_TranslateWithAPI.clicked.connect(lambda: self.saveText(self.getIdText(self.currentId),
                                                                                         self.ui.TextEdit_API.toPlainText(),
                                                                                         funcT.TranslateTag.use_API))

        # 顶部右侧的下拉按钮
        ButtonMenu = RoundMenu(parent=self.ui.SplitPushButton)
        ButtonMenu.addAction(Action(icon=FIC.PLAY, text="从最近的未翻译词条开始", triggered=lambda: self.continueLastText()))
        self.ui.SplitPushButton.setFlyout(ButtonMenu)

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
        return None

    def displayIDText(self, id: int):
        self.displayText(self.getIdText(id))
        return None

    def saveText(self, text: funcT.TranslateText, translatedText: str, translateTag: str, oneNext: bool = True):
        text.translatedText = translatedText
        if text.translateTag == "None":
            text.translateTag = f";{translateTag}"
        elif translateTag in text.translateTag:
            pass
        else:
            text.translateTag += f";{translateTag}"
        if oneNext:
            self.displayText(self.getIdText(self.currentId + 1))
        return None

    def translateWithAPI(self, originalText: str, originalLan: str = "en", targetLan: str = "zh", displayInWindow: bool = True):
        if self.ui.ToggleButton_AutoTranslateWithAPI.isChecked():
            self.autoTranslate(originalLan, targetLan)
        else:
            rule = Rule()
            originalText = rule.translate_rule(originalText)
            targetText = funcT.fanyi_baidu(originalText, originalLan, targetLan)
            targetText = rule.reborn_rule(targetText)
            if displayInWindow:
                self.ui.TextEdit_API.setText(targetText)
                return None
            else:
                return targetText

    def autoTranslate(self, originalLan: str = "en", targetLan: str = "zh"):
        self.Thread_AT = QThread(self)
        self.Worker_AT = Worker_AutoTranslate(self.project, self.currentId, originalLan, targetLan)
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

    def __init__(self, project: funcT.TranslateProject, startId: int, originalLan: str = "en", targetLan: str = "zh"):
        super().__init__()

        self.project = project
        self.originalLan = originalLan
        self.targetLan = targetLan
        self.startId = startId

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
            targetText = funcT.fanyi_baidu(originalText, self.originalLan, self.targetLan)
            targetText = rule.reborn_rule(targetText)
            self.targetIdSignal.emit(n)
            self.targetTextSignal.emit(targetText)
            print(f"已完成一次 API 翻译（{n}）。")
            sleep(1)
            n += 1


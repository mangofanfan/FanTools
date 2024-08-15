import logging

from PySide2.QtCore import Signal, QObject
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QGridLayout, QWidget, QHBoxLayout
from qfluentwidgets import CardWidget, SubtitleLabel, BodyLabel, LineEdit, ToolButton, ToolTipFilter
from qfluentwidgets import FluentIcon as FIC

logger = logging.getLogger("FanTools.TranslateTextCard")

class Card(QObject):
    update = Signal(tuple)

    def __init__(self, parent: QWidget = None, id: str = "ID", tags: str = "None"):
        super().__init__()
        self.id = id
        self.tags = tags
        self.parent = parent
        self.widget = None

        self.run()

    def run(self):
        self.widget = CardWidget(self.parent)
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)

        Label_Title = SubtitleLabel(self.widget)
        Label_Title.setText(f"ID：{self.id}")
        self.layout.addWidget(Label_Title, 0, 0)

        BodyLabel_1 = BodyLabel(self.widget)
        BodyLabel_1.setText(f"标签：{self.tags}")
        self.layout.addWidget(BodyLabel_1, 0, 1)

        self.buttonLayout = QHBoxLayout()
        self.layout.addLayout(self.buttonLayout, 0, 2)

        ToolButton_CopyOriginalText = ToolButton()
        ToolButton_CopyOriginalText.setIcon(FIC.COPY)
        ToolButton_CopyOriginalText.setToolTip("将词条的待翻译文本直接复制到译文输入行内，然后再做修改。")
        ToolButton_CopyOriginalText.installEventFilter(ToolTipFilter(ToolButton_CopyOriginalText))
        self.buttonLayout.addWidget(ToolButton_CopyOriginalText)

        ToolButton_TranslateWithAPI = ToolButton()
        ToolButton_TranslateWithAPI.setIcon(FIC.ROBOT)
        ToolButton_TranslateWithAPI.setToolTip("调用翻译API对此词条执行翻译，译文将放入译文输入行内。")
        ToolButton_TranslateWithAPI.installEventFilter(ToolTipFilter(ToolButton_TranslateWithAPI))
        self.buttonLayout.addWidget(ToolButton_TranslateWithAPI)

        self.OriginalText_LineEdit = LineEdit()
        self.OriginalText_LineEdit.setEnabled(False)
        self.TranslatedText_LineEdit = LineEdit()
        self.TranslatedText_LineEdit.setClearButtonEnabled(True)
        self.layout.addWidget(self.OriginalText_LineEdit, 1, 0, 1, 3)
        self.layout.addWidget(self.TranslatedText_LineEdit, 2, 0, 1, 3)

    def setup(self, originalText: str, translatedText: str = ""):
        self.OriginalText_LineEdit.setText(originalText)
        if translatedText == "None":
            translatedText = ""
        self.TranslatedText_LineEdit.setText(translatedText)

        self.TranslatedText_LineEdit.editingFinished.connect(lambda: self.updateText(self.TranslatedText_LineEdit.text()))

    def updateText(self, translatedText: str):
        self.update.emit((self.id, translatedText))
        logger.debug(f"词条卡片已经发送更新信号。（{self.id} | {translatedText}）")

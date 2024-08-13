from PySide2.QtGui import Qt
from PySide2.QtWidgets import QGridLayout, QWidget
from qfluentwidgets import CardWidget, SubtitleLabel, BodyLabel, LineEdit, TextEdit


class Card:
    def __init__(self, parent: QWidget = None, titleLabel: str = "CaptionLabel", tags: str = "None"):
        self.titleLabel = titleLabel
        self.tags = tags

        self.parent = parent
        self.widget = CardWidget(parent)
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)

        Label_Title = SubtitleLabel(self.widget)
        Label_Title.setText(titleLabel)
        self.layout.addWidget(Label_Title, 0, 0)

        BodyLabel_1 = BodyLabel(self.widget)
        BodyLabel_1.setText(f"标签：{tags}")
        self.layout.addWidget(BodyLabel_1, 0, 1)

        self.OriginalText_LineEdit = LineEdit()
        self.TranslatedText_LineEdit = LineEdit()
        self.layout.addWidget(self.OriginalText_LineEdit, 1, 0, 1, 2)
        self.layout.addWidget(self.TranslatedText_LineEdit, 2, 0, 1, 2)

    def setup(self, originalText: str, translatedText: str = ""):
        self.OriginalText_LineEdit.setText(originalText)
        self.TranslatedText_LineEdit.setText(translatedText)

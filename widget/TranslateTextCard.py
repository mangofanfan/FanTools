from PySide2.QtGui import Qt
from PySide2.QtWidgets import QGridLayout, QWidget
from qfluentwidgets import CardWidget, SubtitleLabel, BodyLabel, LineEdit, TextEdit


class Card:
    def __init__(self, parent: QWidget = None, titleLabel: str = "CaptionLabel", tags: str = "None"):
        self.titleLabel = titleLabel
        self.tags = tags

        self.parent = parent
        self.widget = CardWidget()
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)
        self.widget.setMinimumWidth(600)
        self.widget.setMinimumHeight(60)

        Label_Title = SubtitleLabel(self.widget)
        Label_Title.setText(titleLabel)
        self.layout.addWidget(Label_Title, 0, 0)

        BodyLabel_1 = BodyLabel(self.widget)
        BodyLabel_1.setText(f"标签：{tags}")
        self.layout.addWidget(BodyLabel_1, 0, 1)

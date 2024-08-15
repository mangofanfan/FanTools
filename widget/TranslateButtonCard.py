from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import FluentIcon as FIC
from qfluentwidgets import CardWidget, BodyLabel, CaptionLabel, PushButton, ProgressBar, IconWidget


class Card_Single:
    def __init__(self):
        self.widget = CardWidget()
        self.basedLayout = QHBoxLayout()
        self.widget.setLayout(self.basedLayout)
        self.textLayout = QVBoxLayout()

        icon = IconWidget()
        icon.setIcon(FIC.UNIT)
        icon.setFixedSize(32, 32)
        self.basedLayout.addWidget(icon)

        label_1 = BodyLabel()
        label_1.setText("单词条翻译工具")
        label_2 = CaptionLabel()
        label_2.setText("每页显示一个词条，在套用API翻译结果前可以快捷修改。")
        self.textLayout.addWidget(label_1)
        self.textLayout.addWidget(label_2)
        self.basedLayout.addLayout(self.textLayout)

        self.button = PushButton()
        self.button.setFixedWidth(120)
        self.button.setText("启动")
        self.basedLayout.addWidget(self.button)


class Card_Multi:
    def __init__(self):
        self.widget = CardWidget()
        self.basedLayout = QHBoxLayout()
        self.textLayout = QVBoxLayout()
        self.widget.setLayout(self.basedLayout)

        icon = IconWidget()
        icon.setIcon(FIC.BOOK_SHELF)
        icon.setFixedSize(32, 32)
        self.basedLayout.addWidget(icon)

        label_1 = BodyLabel()
        label_1.setText("列表词条翻译工具")
        label_2 = CaptionLabel()
        label_2.setText("将大量词条同时显示在列表中，适合批量翻译。")
        self.textLayout.addWidget(label_1)
        self.textLayout.addWidget(label_2)
        self.basedLayout.addLayout(self.textLayout)

        self.button = PushButton()
        self.button.setFixedWidth(120)
        self.button.setText("启动")
        self.basedLayout.addWidget(self.button)


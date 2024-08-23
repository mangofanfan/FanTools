from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import FluentIcon as FIC
from qfluentwidgets import CardWidget, BodyLabel, CaptionLabel, PushButton, IconWidget


class baseCard:
    def __init__(self, iconPath, text_1: str, text_2: str, buttonText: str):
        self.widget = CardWidget()
        self.basedLayout = QHBoxLayout()
        self.textLayout = QVBoxLayout()
        self.widget.setLayout(self.basedLayout)
        self.widget.setFixedHeight(55)

        icon = IconWidget()
        icon.setIcon(iconPath)
        icon.setFixedSize(32, 32)
        self.basedLayout.addWidget(icon)

        label_1 = BodyLabel()
        label_1.setText(text_1)
        label_2 = CaptionLabel()
        label_2.setText(text_2)
        self.textLayout.addWidget(label_1)
        self.textLayout.addWidget(label_2)
        self.basedLayout.addLayout(self.textLayout)

        self.button = PushButton()
        self.button.setFixedWidth(120)
        self.button.setText(buttonText)
        self.basedLayout.addWidget(self.button)


class Card_Single(baseCard):
    def __init__(self):
        super().__init__(iconPath=FIC.UNIT,
                         text_1="单词条翻译工具",
                         text_2="每页显示一个词条，在套用API翻译结果前可以快捷修改。",
                         buttonText="启动")


class Card_Multi(baseCard):
    def __init__(self):
        super().__init__(iconPath=FIC.BOOK_SHELF,
                         text_1="列表词条翻译工具",
                         text_2="将大量词条显示在同一列表中，适合批量翻译。",
                         buttonText="启动")


class Card_Glossary(baseCard):
    def __init__(self):
        super().__init__(iconPath=FIC.EDIT,
                         text_1="术语表编辑器",
                         text_2="编辑翻译时加载的术语表，将在人工翻译时弹出提示，在自动翻译时自动应用。",
                         buttonText="启动")

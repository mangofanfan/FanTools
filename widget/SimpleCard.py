from typing import Union

from PySide2.QtCore import QSize, QEasingCurve, Qt
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QGridLayout, QVBoxLayout
from qfluentwidgets import CardWidget, ImageLabel, SubtitleLabel, BodyLabel, HyperlinkButton, HeaderCardWidget, \
    StrongBodyLabel, FlowLayout, CaptionLabel


class ToolCard(CardWidget):
    def __init__(self, image: Union[str, QPixmap, QImage], title: str, text: str, func: staticmethod = None, parent = None):
        super().__init__(parent=parent)
        self._layout = QGridLayout()
        self.setLayout(self._layout)

        self.image = ImageLabel()
        self.image.setImage(image)
        self.image.setFixedSize(QSize(64, 64))
        self._layout.addWidget(self.image, 0, 0, 2, 1)

        self.subtitle = SubtitleLabel()
        self.subtitle.setText(title)
        self._layout.addWidget(self.subtitle, 0, 1)

        self.body = BodyLabel()
        self.body.setText(text)
        self._layout.addWidget(self.body, 1, 1)

        self.clicked.connect(func)


class LinkCard(CardWidget):
    def __init__(self, image: Union[str, QPixmap, QImage], title: str, text: str, url: str, urlText: str, parent = None):
        super().__init__(parent=parent)
        self._layout = QGridLayout()
        self.setLayout(self._layout)

        self.image = ImageLabel()
        self.image.setImage(image)
        self.image.setFixedSize(QSize(48, 48))
        self.image.setContentsMargins(100, 0, 100, 0)
        self._layout.addWidget(self.image, 0, 0, 2, 1)

        self.subtitle = SubtitleLabel()
        self.subtitle.setText(title)
        self._layout.addWidget(self.subtitle, 0, 1)

        self.body = BodyLabel()
        self.body.setText(text)
        self._layout.addWidget(self.body, 1, 1)

        self.HyperlinkButton = HyperlinkButton()
        self.HyperlinkButton.setUrl(url)
        self.HyperlinkButton.setText(urlText)
        self.HyperlinkButton.setFixedWidth(180)
        self._layout.addWidget(self.HyperlinkButton, 0, 2, 2, 1)

class EndlessCard(HeaderCardWidget):
    def __init__(self, title: str, text: str, parent=None):
        super().__init__(parent=parent)
        self.setTitle(title)

        label = StrongBodyLabel()
        label.setText(text)
        self._layout = QVBoxLayout()
        self.viewLayout.addLayout(self._layout)
        self._layout.addWidget(label)
        self._layout.addSpacing(20)

        self.FlowLayout = FlowLayout(needAni=True)
        self._layout.addLayout(self.FlowLayout)
        self.FlowLayout.setAnimation(250, QEasingCurve.OutQuad)
        self.FlowLayout.setVerticalSpacing(20)
        self.FlowLayout.setHorizontalSpacing(10)

    def add(self, item: str, desc: str = None):
        card = CardWidget()
        card.setMinimumSize(QSize(120, 50))
        layout = QVBoxLayout()
        card.setLayout(layout)

        label = BodyLabel()
        label.setText(item)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        if desc:
            label_2 = CaptionLabel()
            label_2.setText(desc)
            label_2.setAlignment(Qt.AlignCenter)
            layout.addWidget(label_2)

        self.FlowLayout.addWidget(card)

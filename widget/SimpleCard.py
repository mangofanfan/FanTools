import logging

from typing import Union

from PySide2.QtCore import QSize, QEasingCurve, Qt, QUrl
from PySide2.QtGui import QPixmap, QImage, QDesktopServices
from PySide2.QtWidgets import QGridLayout, QVBoxLayout
from qfluentwidgets import CardWidget, ImageLabel, SubtitleLabel, BodyLabel, HyperlinkButton, HeaderCardWidget, \
    StrongBodyLabel, FlowLayout, CaptionLabel

from widget.function import basicFunc
from widget.function_hitokoto import yi_yan

logger = logging.getLogger("FanTools.SimpleCard")


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

    def add(self, item: str, desc: str = None, url: str = None):
        card = CardWidget()
        card.setFixedHeight(50)
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

        if url:
            card.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))

        self.FlowLayout.addWidget(card)
        return None


class YiYanCard(CardWidget):
    """
    一言卡片，创建后自动定时更新一言。
    """
    def __init__(self, parent = None):
        super().__init__(parent=parent)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.BodyLabel = BodyLabel()
        self.BodyLabel.setText("生命因何而沉睡，因为我们终将从梦中醒来。")
        self.BodyLabel.setWordWrap(True)
        self._layout.addWidget(self.BodyLabel)

        self.CaptionLabel = CaptionLabel()
        self.CaptionLabel.setText("流萤 - 崩坏·星穹铁道")
        self.CaptionLabel.setAlignment(Qt.AlignRight)
        self._layout.addWidget(self.CaptionLabel)

        self.url = basicFunc.getInfo()["au"]
        self.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(self.url)))

        self.YiYan = yi_yan()
        self.YiYan.GUIUpdateSignal.connect(self._getSignal)
        self.setup()

    def setup(self):
        self.YiYan.start()
        return None

    def _getSignal(self, data: dict):
        content = data["content"]
        origin = data["origin"]
        url = self.YiYan.dict["official"] + "?id=" + data["id"]
        self._setText(content, origin, url)
        return None

    def _setText(self, content: str, caption: str, url: str):
        self.BodyLabel.setText(content)
        self.CaptionLabel.setText(caption)
        self.url = url
        self.update()
        logger.info(f"一言卡片更新：{content} ——{caption} | {url}")
        return None

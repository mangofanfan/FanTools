import traceback

from qfluentwidgets import InfoBar, InfoBarPosition, FlyoutAnimationType


def msgTextIdError(self):
    InfoBar.error(title="错误",
                  content="尝试打开不存在的词条。",
                  isClosable=False,
                  duration=2000,
                  position=InfoBarPosition.TOP_RIGHT,
                  parent=self)


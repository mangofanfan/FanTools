import sys

from PySide2.QtCore import Signal
from PySide2.QtGui import QColor, QIcon
from PySide2.QtWidgets import QDesktopWidget
from qfluentwidgets import FluentWindow, MessageBox, FluentTitleBar, isDarkTheme
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow

from widget.function import basicFunc
from widget.function_setting import cfg, qconfig

import logging


class MainWindow(FluentWindow):
    logger = logging.getLogger("FanTools.MainWindow")
    closeWindow = Signal()

    def __init__(self, parent = None):
        super().__init__(parent=parent)

    def centerWindow(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def closeEvent(self, event):
        if not qconfig.get(cfg.ExitConfirm):
            self.logger.info("用户选择退出程序，正在执行退出操作。")
            self.logger.debug("为什么没有弹出确认？因为程序设置中已将退出确认关闭，将其打开可以重新显示退出确认（推荐）。")
            self.closeWindow.emit()
            return None
        self.logger.info("接收到退出程序信号。")

        def yes():
            self.logger.info("用户选择退出程序，正在执行退出操作。")
            self.closeWindow.emit()
            return None

        def cancel():
            self.logger.info("用户取消了退出程序操作。")
            return None

        w = MessageBox(title="确认退出程序？",
                       content="如确认，所有正在执行的线程将被立刻中断，所有子窗口将被关闭，然后完成退出。\n"
                               "如果程序正在执行负担较大的任务，此时退出程序可能导致程序窗口崩溃，但最终可以退出。\n"
                               "PS：您可以在设置中启用或关闭退出确认功能。",
                       parent=self)
        w.yesButton.setText("确认退出")
        w.yesSignal.connect(yes)
        w.cancelButton.setText("我还没准备好")
        w.cancelSignal.connect(cancel)
        w.show()

        event.ignore()


class FanTitleBar(FluentTitleBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setContentsMargins(20, 0, 0, 0)


class TranslateWindow(BackgroundAnimationWidget, FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isMicaEnabled = False
        self._lightBackgroundColor = QColor(243, 243, 243)
        self._darkBackgroundColor = QColor(32, 32, 32)
        self.setMicaEffectEnabled(True)
        qconfig.themeChangedFinished.connect(self._onThemeChangedFinished)
        self.setTitleBar(FanTitleBar(self))
        self.setWindowIcon(QIcon(basicFunc.getHerePath() + "/data/TranslateLogo.png"))

    def centerWindow(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def setMicaEffectEnabled(self, isEnabled: bool):
        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return

        self._isMicaEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self._normalBackgroundColor())

    def isMicaEffectEnabled(self):
        return self._isMicaEnabled

    def _onThemeChangedFinished(self):
        if self.isMicaEffectEnabled():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())

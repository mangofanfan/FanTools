import logging

from PySide2.QtCore import Signal
from PySide2.QtGui import QCursor, QKeyEvent
from PySide2.QtWidgets import QDesktopWidget, QTableWidgetItem, QHeaderView
from qfluentwidgets import MessageBox, TableWidget, RoundMenu, Action
from qfluentwidgets import FluentIcon as FIC

from widget.WindowBase import *
from widget import function_setting as funcS


class MainWindow(FanFluentWindow):
    logger = logging.getLogger("FanTools.MainWindow")
    closeWindow = Signal()

    def __init__(self, parent = None):
        super().__init__(parent=parent)
        self.setMicaEffectEnabled(True)
        if funcS.qconfig.get(funcS.cfg.WindowAcrylicEnable):
            self.setAcrylicEffectEnabled(True)

    def centerWindow(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def closeEvent(self, event):
        if not qconfig.get(funcS.cfg.ExitConfirm):
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
                       content="如确认，所有正在执行的线程、进程将被中断，所有子窗口将被关闭，然后完成退出。\n"
                               "由于技术原因，工具箱进程会在后台继续运行最多六十秒，以等待资源完成释放后再退出。\n"
                               "PS：您可以在设置中启用或关闭退出确认功能。",
                       parent=self)
        w.yesButton.setText("确认退出")
        w.yesSignal.connect(yes)
        w.cancelButton.setText("我还没准备好")
        w.cancelSignal.connect(cancel)
        w.show()

        event.ignore()


class TranslateWindow(BackgroundAnimationWidget, FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isMicaEnabled = False
        self._isAcrylicEnabled = False
        self._lightBackgroundColor_int = (243, 243, 243)
        self._darkBackgroundColor_int = (32, 32, 32)
        self._lightBackgroundColor = QColor(243, 243, 243)
        self._darkBackgroundColor = QColor(32, 32, 32)

        self.setMicaEffectEnabled(True)
        if funcS.qconfig.get(funcS.cfg.WindowAcrylicEnable):
            self.setAcrylicEffectEnabled(True)

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

    def getBackgroundColor(self, _hex: bool = False):
        if _hex:
            if isDarkTheme():
                return basicFunc.rgb_to_hex(self._darkBackgroundColor_int)
            else:
                return basicFunc.rgb_to_hex(self._lightBackgroundColor_int)
        else:
            return self.bgColorObject.backgroundColor

    def setAcrylicEffectEnabled(self, isEnabled: bool):
        self._isAcrylicEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setAcrylicEffect(self.winId(), self.getBackgroundColor(True))
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self.getBackgroundColor())

    def isAcrylicEffectEnabled(self):
        return self._isAcrylicEnabled

    def _onThemeChangedFinished(self):
        if self.isMicaEffectEnabled():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        if self.isAcrylicEffectEnabled():
            self.windowEffect.setAcrylicEffect(self.winId(), self.getBackgroundColor(True))


class GlossaryTableWidget(TableWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.logger = logging.getLogger("FanTools.GlossaryTable")

        # 右键菜单设置
        self.RightMenu = RoundMenu()
        self.RightMenu.addAction(Action(FIC.ADD, "增加新术语词条", triggered=self.addLine, shortcut="Ctrl+N"))
        self.RightMenu.addAction(Action(FIC.DELETE, "清除空行", triggered=self.deleteBlank))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.RightClickMenu)

        # 表格外观设置
        self.setBorderVisible(True)
        self.setBorderRadius(8)
        self.setWordWrap(True)
        self.setColumnCount(2)
        header_1 = QTableWidgetItem()
        header_1.setText("原文本")
        header_2 = QTableWidgetItem()
        header_2.setText("翻译文本")
        self.setHorizontalHeaderItem(0, header_1)
        self.setHorizontalHeaderItem(1, header_2)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def addLine(self):
        self.insertRow(self.rowCount())
        self.logger.debug("在术语表表格中添加一个新行。")
        return None

    def deleteBlank(self):
        l = list(range(self.rowCount()))
        l.reverse()

        # 判定空行并清除空行
        for i in l:
            b = False
            if self.item(i, 0) is not None:
                if self.item(i, 0).text() is not None and self.item(i, 0).text() != "":
                    b = True
            if self.item(i, 1) is not None:
                if self.item(i, 1).text() is not None and self.item(i, 1).text() != "":
                    b = True
            if b is False:
                self.removeRow(i)
            else:
                continue

        self.logger.debug("在术语表表格中删除所有空行。")
        return None


    def RightClickMenu(self):
        self.RightMenu.popup(QCursor.pos())

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_N and e.modifiers() == Qt.ControlModifier:
            self.addLine()


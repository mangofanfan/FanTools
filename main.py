import os
import sys, locale
import traceback

from PySide2.QtGui import QGuiApplication, Qt, QIcon
from PySide2.QtWidgets import QApplication
import PySide2.QtCore as QC
from qfluentwidgets import FluentWindow, setTheme, Theme, NavigationItemPosition, FluentTranslator, MessageBox
from qfluentwidgets import FluentIcon as FIC

from MainPage import MainPage
from DownloadPage import DownloadPage
from HashPage import HashPage
from TranslatePage import TranslatePage
from ConfigPage import ConfigPage

from widget.function import basicFunc
from widget.function_setting import cfg
import widget.function_error as funcE

locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")

QGuiApplication.setAttribute(QC.Qt.AA_EnableHighDpiScaling, True)
QGuiApplication.setAttribute(QC.Qt.AA_UseHighDpiPixmaps, True)
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

app = QApplication(sys.argv)
app.setStyleSheet(basicFunc.readFile(file="/data/global.qss"))
# app.setStyleSheet("")
translator = FluentTranslator()
app.installTranslator(translator)

window_MainPage = MainPage()
window_DownloadPage = DownloadPage()
window_HashPage = HashPage()
window_TranslatePage = TranslatePage()
window_ConfigPage = ConfigPage()


def showInfoBar(msfFunc):
    msfFunc()


class Main:
    def __init__(self):
        self.mainWindow = FluentWindow()
        self.mainWindow.setMinimumSize(QC.QSize(800, 600))
        self.mainWindow.setWindowTitle("🥭 芒果工具箱 🥭 FanTools  🥭")
        self.mainWindow.setWindowIcon(QIcon(basicFunc.getHerePath() + "\\data\\two_mango_es.png"))

    def addSubWindow(self):
        self.mainWindow.addSubInterface(interface=window_MainPage.scrollArea,
                                        icon=FIC.HOME,
                                        text="主页")
        self.mainWindow.addSubInterface(interface=window_DownloadPage.scrollArea,
                                        icon=FIC.DOWNLOAD,
                                        text="下载工具")
        self.mainWindow.addSubInterface(interface=window_HashPage.scrollArea,
                                        icon=FIC.ALBUM,
                                        text="哈希值校验工具")
        self.mainWindow.addSubInterface(interface=window_TranslatePage.scrollArea,
                                        icon=FIC.LANGUAGE,
                                        text="翻译工具")
        self.mainWindow.addSubInterface(interface=window_ConfigPage.scrollArea,
                                        icon=FIC.SETTING,
                                        position=NavigationItemPosition.BOTTOM,
                                        text="设置")

    def run(self):
        self.addSubWindow()
        self.mainWindow.show()


if __name__ == "__main__":
    main = Main()
    try:
        main.run()
    except Exception as e:
        def closeWindowAndLog():
            os.startfile(basicFunc.getHerePath() + r"\log")
            sys.exit(1)

        def close():
            sys.exit(1)

        w = MessageBox(title="启动过程中捕获到异常",
                       content="安全起见，程序将立即关闭。报错日志始终依照设置生成，您可以通过日志调试检查问题，或将日志与有关信息作为 issue 提交至 GitHub。\n"
                               f"下面是本次异常的控制台输出信息：{e}" +
                               traceback.format_exc(),
                       parent=main.mainWindow)
        w.yesButton.setText("关闭程序并查看日志文件夹")
        w.cancelButton.setText("关闭程序")
        w.yesButton.clicked.connect(closeWindowAndLog)
        w.cancelButton.clicked.connect(close)
        w.show()

    finally:
        sys.exit(app.exec_())

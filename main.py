import sys

from PySide2.QtGui import QGuiApplication, Qt, QIcon
from PySide2.QtWidgets import QApplication
import PySide2.QtCore as QC
from qfluentwidgets import FluentWindow, setTheme, Theme
from qfluentwidgets import FluentIcon as FIC

from MainPage import MainPage
from DownloadPage import DownloadPage
from HashPage import HashPage
from TranslatePage import TranslatePage

from widget.function import basicFunc

QGuiApplication.setAttribute(QC.Qt.AA_EnableHighDpiScaling, True)
QGuiApplication.setAttribute(QC.Qt.AA_UseHighDpiPixmaps, True)
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

app = QApplication(sys.argv)
app.setStyleSheet(basicFunc.readFile(file="/data/global.qss"))
# app.setStyleSheet("")

window_MainPage = MainPage()
window_DownloadPage = DownloadPage()
window_HashPage = HashPage()
window_TranslatePage = TranslatePage()


class Main:
    def __init__(self):
        self.mainWindow = FluentWindow()
        self.mainWindow.setMinimumSize(QC.QSize(800, 600))
        self.mainWindow.setWindowTitle("🥭 芒果工具箱 🥭 FanTools  🥭")
        self.mainWindow.setWindowIcon(QIcon(basicFunc.getHerePath() + "\\data\\two_mango_es.png"))

    def addSubWindow(self):
        self.mainWindow.addSubInterface(interface=window_MainPage.widget,
                                        icon=FIC.HOME,
                                        text="主页")
        self.mainWindow.addSubInterface(interface=window_DownloadPage.widget,
                                        icon=FIC.DOWNLOAD,
                                        text="下载工具")
        self.mainWindow.addSubInterface(interface=window_HashPage.widget,
                                        icon=FIC.ALBUM,
                                        text="哈希值校验工具")
        self.mainWindow.addSubInterface(interface=window_TranslatePage.widget,
                                        icon=FIC.LANGUAGE,
                                        text="翻译工具")

    def run(self):
        self.addSubWindow()
        self.mainWindow.show()
        setTheme(Theme.LIGHT)


if __name__ == "__main__":
    main = Main()
    main.run()

    sys.exit(app.exec_())

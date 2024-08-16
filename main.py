import os
import sys, locale
import traceback

from PySide2.QtGui import QGuiApplication, Qt, QIcon
from PySide2.QtWidgets import QApplication
import PySide2.QtCore as QC
from qfluentwidgets import setTheme, Theme, NavigationItemPosition, FluentTranslator, MessageBox, \
    SplashScreen, FluentWindow
from qfluentwidgets import FluentIcon as FIC
from qframelesswindow import AcrylicWindow

from widget.function import basicFunc
from widget.function_setting import cfg
import widget.function_error as funcE

import logging

# 首先加载日志模块

logger = logging.getLogger("FanTools")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

fh_1 = logging.FileHandler(basicFunc.getHerePath() + "/log/info.log", mode="w")
fh_1.setLevel(logging.INFO)
fh_1.setFormatter(formatter)
logger.addHandler(fh_1)

fh_2 = logging.FileHandler(basicFunc.getHerePath() + "/log/debug.log", mode="w")
fh_2.setLevel(logging.DEBUG)
fh_2.setFormatter(formatter)
logger.addHandler(fh_2)

logger.info("日志模块加载完毕，开始记录日志。")

locale.setlocale(locale.LC_ALL, "zh_CN.UTF-8")

QGuiApplication.setAttribute(QC.Qt.AA_EnableHighDpiScaling, True)
QGuiApplication.setAttribute(QC.Qt.AA_UseHighDpiPixmaps, True)
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

app = QApplication(sys.argv)
app.setStyleSheet(basicFunc.readFile(file="/data/global.qss"))
translator = FluentTranslator()
app.installTranslator(translator)

logger.debug("各前置模块加载完毕，开始实现窗口。")


class Main:
    def __init__(self):
        self.mainWindow = FluentWindow()
        self.mainWindow.setMinimumSize(QC.QSize(800, 600))
        self.mainWindow.setWindowTitle("🥭 芒果工具箱 🥭 FanTools  🥭")
        self.mainWindow.setWindowIcon(QIcon(basicFunc.getHerePath() + "\\data\\two_mango_es.png"))
        logger.debug("窗口参数设置完毕。")

        self.splashScreen =  SplashScreen(self.mainWindow.windowIcon(), self.mainWindow)
        self.splashScreen.setIconSize(QC.QSize(128, 128))
        self.mainWindow.show()
        QApplication.processEvents()
        logger.debug("启动页面已实现。")

    def addSubWindow(self):
        from MainPage import MainPage
        from DownloadPage import DownloadPage
        from HashPage import HashPage
        from TranslatePage import TranslatePage
        from ConfigPage import ConfigPage
        self.window_MainPage = MainPage()
        self.window_DownloadPage = DownloadPage()
        self.window_HashPage = HashPage()
        self.window_TranslatePage = TranslatePage()
        self.window_ConfigPage = ConfigPage()

        self.mainWindow.addSubInterface(interface=self.window_MainPage.scrollArea,
                                        icon=FIC.HOME,
                                        text="主页")
        self.mainWindow.addSubInterface(interface=self.window_DownloadPage.scrollArea,
                                        icon=FIC.DOWNLOAD,
                                        text="下载工具")
        self.mainWindow.addSubInterface(interface=self.window_HashPage.scrollArea,
                                        icon=FIC.ALBUM,
                                        text="哈希值校验工具")
        self.mainWindow.addSubInterface(interface=self.window_TranslatePage.scrollArea,
                                        icon=FIC.LANGUAGE,
                                        text="翻译工具")
        self.mainWindow.addSubInterface(interface=self.window_ConfigPage.scrollArea,
                                        icon=FIC.SETTING,
                                        position=NavigationItemPosition.BOTTOM,
                                        text="设置")
        logger.debug("窗口子页面全部添加。")

    def run(self):
        self.addSubWindow()
        self.splashScreen.finish()
        logger.info("启动页面隐藏，窗口已经实现。")


if __name__ == "__main__":
    main = Main()
    try:
        main.run()
    except Exception as e:
        def closeWindowAndLog():
            os.startfile(basicFunc.getHerePath() + r"\log")
            logger.error("启动异常，成功打开日志文件夹。程序将要退出。")
            sys.exit(1)

        def close():
            logger.error("启动异常，程序将要退出。")
            sys.exit(1)

        logger.exception("程序启动过程中出现严重异常，异常信息记录如下。")
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
        logger.error("已创建启动异常警告对话框。")

    finally:
        sys.exit(app.exec_())

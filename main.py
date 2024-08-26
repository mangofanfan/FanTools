import os
import sys, locale
import traceback
import pathlib
import time

from PySide2.QtGui import QGuiApplication, Qt, QIcon
from PySide2.QtWidgets import QApplication
import PySide2.QtCore as QC
from qfluentwidgets import NavigationItemPosition, FluentTranslator, MessageBox, SplashScreen
from qfluentwidgets import FluentIcon as FIC

from widget.function import basicFunc
from widget.Window import MainWindow

import logging

# 首先加载日志模块
log_dir = pathlib.Path(basicFunc.getHerePath() + "/log")
if not log_dir.exists():
    log_dir.mkdir()

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

logger.info(f"芒果工具箱🥭正在启动 | 当前版本 {basicFunc.getInfo()['v']}")
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
        self.mainWindow = MainWindow()
        self.mainWindow.setMinimumSize(QC.QSize(500, 400))
        self.mainWindow.resize(QC.QSize(900, 700))
        self.mainWindow.setWindowTitle("🥭 芒果工具箱 🥭 FanTools  🥭")
        self.mainWindow.setWindowIcon(QIcon(basicFunc.getHerePath() + "\\data\\two_mango_es.png"))
        self.mainWindow.centerWindow()
        logger.debug("窗口参数设置完毕。")

        self.splashScreen =  SplashScreen(self.mainWindow.windowIcon(), self.mainWindow)
        self.splashScreen.setIconSize(QC.QSize(128, 128))
        self.mainWindow.show()
        QApplication.processEvents()
        logger.debug("启动页面已实现。")

        self.mainWindow.closeWindow.connect(self.closeWindow)

    def addSubWindow(self):
        from Page.HomePage import HomePage
        from Page.DownloadPage import DownloadPage
        from Page.HashPage import HashPage
        from Page.TranslatePage import TranslatePage
        from Page.ConfigPage import ConfigPage
        from Page.AboutPage import AboutPage
        self.window_HomePage = HomePage()
        self.window_DownloadPage = DownloadPage()
        self.window_HashPage = HashPage()
        self.window_TranslatePage = TranslatePage()
        self.window_ConfigPage = ConfigPage()
        self.window_AboutPage = AboutPage()

        self.mainWindow.addSubInterface(interface=self.window_HomePage.bodyWidget,
                                        icon=FIC.HOME,
                                        text="主页")
        self.mainWindow.navigationInterface.addSeparator(position=NavigationItemPosition.TOP)
        self.mainWindow.addSubInterface(interface=self.window_DownloadPage.bodyWidget,
                                        icon=FIC.DOWNLOAD,
                                        text="下载工具")
        self.mainWindow.addSubInterface(interface=self.window_HashPage.bodyWidget,
                                        icon=FIC.ALBUM,
                                        text="哈希值校验工具")
        self.mainWindow.addSubInterface(interface=self.window_TranslatePage.bodyWidget,
                                        icon=FIC.LANGUAGE,
                                        text="翻译工具")
        self.mainWindow.navigationInterface.addSeparator(position=NavigationItemPosition.BOTTOM)
        self.mainWindow.addSubInterface(interface=self.window_ConfigPage.bodyWidget,
                                        icon=FIC.SETTING,
                                        position=NavigationItemPosition.BOTTOM,
                                        text="设置")
        self.mainWindow.addSubInterface(interface=self.window_AboutPage.bodyWidget,
                                        icon=FIC.DEVELOPER_TOOLS,
                                        position=NavigationItemPosition.BOTTOM,
                                        text="关于芒果工具箱")

        self.window_HomePage.ToolCard_Download.clicked.connect(
            lambda: self.mainWindow.switchTo(self.window_DownloadPage.scrollArea))
        self.window_HomePage.ToolCard_Hash.clicked.connect(
            lambda: self.mainWindow.switchTo(self.window_HashPage.scrollArea))
        self.window_HomePage.ToolCard_Translate.clicked.connect(
            lambda: self.mainWindow.switchTo(self.window_TranslatePage.scrollArea))

        logger.debug("窗口子页面全部添加。")

    def run(self):
        self.addSubWindow()
        self.splashScreen.finish()
        logger.info("启动页面隐藏，窗口已经实现。")

    def closeWindow(self):
        """
        关闭所有线程和进程，然后执行退出。
        :return: None
        """
        self.mainWindow.destroy()
        self.window_TranslatePage.Tool.destroy()
        self.window_TranslatePage.Multi.destroy()
        self.window_TranslatePage.Glossary.destroy()
        logger.info("已关闭所有程序窗口。")
        time.sleep(1)

        # 退出一言定时线程
        if self.window_HomePage.YiYanCard.YiYan.Thread_Timer.isRunning():
            self.window_HomePage.YiYanCard.YiYan.Worker_Timer.stopRunning()
            self.window_HomePage.YiYanCard.YiYan.Thread_Timer.quit()
            self.window_HomePage.YiYanCard.YiYan.Thread_Timer.wait()
        logger.info("一言定时线程已经退出。")

        # 确保下载工具 aria2c 已经退出
        self.window_DownloadPage.killAria2c()
        logger.info("Aria2c 下载工具已经退出。")

        QApplication.quit()
        return None


if __name__ == "__main__":
    main = Main()
    try:
        main.run()
        logger.debug("加载结束，开始事件循环。")
        returnCode = app.exec_()
        logger.debug(f"事件循环已经结束，准备终止程序。|获得退出代码 {returnCode}")
        logger.info("工具箱运行已退出，芒果帆帆感谢您的使用。😆")
        sys.exit(returnCode)
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
        main.splashScreen.finish()
        w.show()
        logger.error("已创建启动异常警告对话框。")
        app.exec_()

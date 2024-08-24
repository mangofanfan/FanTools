import logging

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QGridLayout, QWidget, QVBoxLayout, QHBoxLayout
from qfluentwidgets import CardWidget, LineEdit, ToolButton, PrimaryToolButton, BodyLabel, ProgressBar, PushButton, \
    ToolTipFilter, SubtitleLabel, IconInfoBadge, TextEdit, RangeSettingCard, SimpleCardWidget
from qfluentwidgets import FluentIcon as FIC

from widget.function import basicFunc
import widget.function_setting as funcS

logger = logging.getLogger("FanTools.DownloadCard")


class Aria2cManageCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        Label_1 = SubtitleLabel()
        Label_1.setText("Aria2c 状态管理器")
        self._layout.addWidget(Label_1)

        Label_2 = BodyLabel()
        Label_2.setText("此处管理 Aria2c 下载工具的状态，需要在工具启用时才能执行下载任务。"
                        "注意，您无法在此管理非工具箱内置的 Aria2c 实例。")
        Label_2.setWordWrap(True)
        self._layout.addWidget(Label_2)

        self._hLayout = QHBoxLayout()
        self._layout.addLayout(self._hLayout)
        self.PushButton_ON = PushButton()
        self.PushButton_ON.setText("启动 Aria2c")
        self.PushButton_ON.setToolTip("启动程序目录下绑定的 Aria2c 实例")
        self.PushButton_ON.installEventFilter(ToolTipFilter(self.PushButton_ON))
        self._hLayout.addWidget(self.PushButton_ON)
        self.PushButton_OFF = PushButton()
        self.PushButton_OFF.setText("关闭 Aria2c")
        self.PushButton_OFF.setToolTip("向 Aria2c 发送停止信号")
        self.PushButton_OFF.installEventFilter(ToolTipFilter(self.PushButton_OFF))
        self._hLayout.addWidget(self.PushButton_OFF)

        self._hLayout.addStretch()

        self.IconInfoBadge_ON = IconInfoBadge.success(FIC.APPLICATION, self._parent, self)
        self.IconInfoBadge_OFF = IconInfoBadge.error(FIC.CLOSE, self._parent, self)


    def setOn(self):
        self.IconInfoBadge_OFF.setVisible(False)
        self.IconInfoBadge_ON.show()
        self.update()
        logger.info("Aria2 进程已经启动。")
        return None

    def setOff(self):
        self.IconInfoBadge_ON.setVisible(False)
        self.IconInfoBadge_OFF.show()
        self.update()
        logger.info("Aria2 进程已经结束。")
        return None


class SingleDownloadCard:
    def __init__(self, parent: QWidget):
        self.parent = parent
        self.widget = SimpleCardWidget()

        self._layout = QVBoxLayout()
        self.widget.setLayout(self._layout)

        Subtitle = SubtitleLabel()
        Subtitle.setText("单文件下载任务提交")
        self._layout.addWidget(Subtitle)

        self.layout = QGridLayout()
        self._layout.addLayout(self.layout)

        BodyLabel_1 = BodyLabel()
        BodyLabel_1.setText("下载链接🔗：")
        self.layout.addWidget(BodyLabel_1, 0, 0)
        BodyLabel_2 = BodyLabel()
        BodyLabel_2.setText("保存路径📂：")
        self.layout.addWidget(BodyLabel_2, 1, 0)

        self.LineEdit_DownloadUrl = LineEdit()
        self.layout.addWidget(self.LineEdit_DownloadUrl, 0, 1, 1, 2)

        self.LineEdit_SavePath = LineEdit()
        self.layout.addWidget(self.LineEdit_SavePath, 1, 1)

        self.ToolButton_SavePath = ToolButton()
        self.ToolButton_SavePath.setIcon(FIC.EDIT)
        self.ToolButton_SavePath.clicked.connect(self._getPath)
        self.layout.addWidget(self.ToolButton_SavePath, 1, 2)

        BodyLabel_3 = BodyLabel()
        BodyLabel_3.setText("注意您无法指定下载所得的文件名///准备妥当后点击右边按钮立即开始下载！👉")
        BodyLabel_4 = BodyLabel()
        BodyLabel_4.setText("下载过程中无法重复提交更多下载，具体下载时长由很多因素决定，您可以稍作休息😊")
        self.layout.addWidget(BodyLabel_3, 2, 0, 1, 2, alignment=Qt.AlignRight)
        self.layout.addWidget(BodyLabel_4, 3, 0, 1, 3)

        self.PrimaryToolButton_Download = PrimaryToolButton()
        self.PrimaryToolButton_Download.setIcon(FIC.DOWNLOAD)
        self.layout.addWidget(self.PrimaryToolButton_Download, 2, 2)

        self.ProgressBar = ProgressBar()
        self.ProgressBar.setRange(0, 100)
        self.ProgressBar.setValue(100)
        self.layout.addWidget(self.ProgressBar, 4, 0, 1, 3)

    def _getPath(self):
        logger.debug("打开单个文件下载保存路径的选择对话框。")
        p = basicFunc.openDirDialog(caption="选择一个文件夹用来存放下载的文件叭😊", basedPath=basicFunc.getHerePath())
        if p:
            self.LineEdit_SavePath.setText(p)
            logger.info(f"选择路径 {p} 作为下载单个文件的保存路径。")
        else:
            logger.debug("未选择有效路径。")
        return None

    def setOff(self):
        self.PrimaryToolButton_Download.setDisabled(True)
        self.ToolButton_SavePath.setDisabled(True)
        self.LineEdit_DownloadUrl.setDisabled(True)
        self.LineEdit_SavePath.setDisabled(True)
        logger.debug("已禁用单文件下载卡片。")
        return None

    def setOn(self):
        self.PrimaryToolButton_Download.setEnabled(True)
        self.ToolButton_SavePath.setEnabled(True)
        self.LineEdit_DownloadUrl.setEnabled(True)
        self.LineEdit_SavePath.setEnabled(True)
        logger.debug("已启用单文件下载卡片。")
        return None


class StatsCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.viewLayout = QVBoxLayout()
        self.setLayout(self.viewLayout)
        label_title = SubtitleLabel()
        label_title.setText("Aria2 状态监控")
        self.viewLayout.addWidget(label_title)

        self._hLayout = QHBoxLayout()
        self.viewLayout.addLayout(self._hLayout)

        self.TextEdit_std = TextEdit()
        self.TextEdit_std.setReadOnly(True)
        self.TextEdit_std.setFixedWidth(380)
        self.TextEdit_std.setPlaceholderText("启动 aria2c 之后，这里会打印下载器的总体统计信息！~")
        self._hLayout.addWidget(self.TextEdit_std)

        self._vLayout = QVBoxLayout()
        self._hLayout.addLayout(self._vLayout)

        label_1 = BodyLabel()
        label_1.setText("此处可以管理状态面板的显示信息。")
        self._vLayout.addWidget(label_1)
        self._vLayout.addStretch()

        Card_TimeSleep = RangeSettingCard(configItem=funcS.cfg.DownloadStatsTimeSleep,
                                          title="数据刷新间隔时间（数值单位：0.1s）",
                                          content="控制状态面板与下载进度条的刷新间隔",
                                          icon=FIC.TILES)
        self.viewLayout.addWidget(Card_TimeSleep)

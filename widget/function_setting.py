from PySide2.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import (ConfigItem, BoolValidator,
                            ColorConfigItem, OptionsConfigItem, OptionsValidator,
                            QConfig, qconfig, RangeConfigItem, RangeValidator, ExpandGroupSettingCard, BodyLabel,
                            LineEdit, PushButton)
from qfluentwidgets import FluentIcon as FIC

from widget.function import basicFunc


class appConfig(QConfig):
    # 外观设置 Appearance
    ThemeMode = OptionsConfigItem("Appearance", "ThemeMode", "light",
                                  OptionsValidator(["light", "dark", "auto"]), restart=True)
    ThemeColor = ColorConfigItem("Appearance", "ThemeColor", "#006DCC")
    WindowAcrylicEnable = ConfigItem("Appearance", "WindowAcrylicEnable", False, BoolValidator())
    FontFamily = OptionsConfigItem("Appearance", "FontFamily", "Hei", OptionsValidator(["Hei", "XiangSu", "QingSong"]))

    # 功能设置 Function
    ExitConfirm = ConfigItem("Function", "ExitConfirm", True, BoolValidator())
    ProxyEnable = ConfigItem("Function", "ProxyEnable", False, BoolValidator())
    ProxyHttp = ConfigItem("Function", "ProxyHttp", "http://127.0.0.1:7890")
    ProxyHttps = ConfigItem("Function", "ProxyHttps", "http://127.0.0.1:7890")

    ## 一言设置
    YiYanEnable = ConfigItem("Function", "YiYanEnable", False, BoolValidator())
    YiYanAPI = OptionsConfigItem("Function", "YiYanAPI", "fan_mirror", OptionsValidator(["official", "fan_mirror"]))
    YiYanTypeA = OptionsConfigItem("Function", "YiYanTypeA", True, BoolValidator())
    YiYanTypeB = OptionsConfigItem("Function", "YiYanTypeB", True, BoolValidator())
    YiYanTypeC = OptionsConfigItem("Function", "YiYanTypeC", True, BoolValidator())
    YiYanTypeD = OptionsConfigItem("Function", "YiYanTypeD", True, BoolValidator())
    YiYanTypeE = OptionsConfigItem("Function", "YiYanTypeE", True, BoolValidator())
    YiYanTypeF = OptionsConfigItem("Function", "YiYanTypeF", True, BoolValidator())
    YiYanTypeG = OptionsConfigItem("Function", "YiYanTypeG", True, BoolValidator())
    YiYanTypeH = OptionsConfigItem("Function", "YiYanTypeH", True, BoolValidator())
    YiYanTypeI = OptionsConfigItem("Function", "YiYanTypeI", True, BoolValidator())
    YiYanTypeJ = OptionsConfigItem("Function", "YiYanTypeJ", True, BoolValidator())
    YiYanTypeK = OptionsConfigItem("Function", "YiYanTypeK", True, BoolValidator())
    YiYanTypeL = OptionsConfigItem("Function", "YiYanTypeL", True, BoolValidator())
    TimeSleep = RangeConfigItem("Function", "TimeSleep", 20, RangeValidator(5, 60))

    # 翻译工具独家设置
    BaiduAPPID = ConfigItem("Translate", "BaiduAPPID", "")
    BaiduKey = ConfigItem("Translate", "BaiduKey", "")
    YoudaoAPPKey = ConfigItem("Translate", "YoudaoAPPKey", "")
    YoudaoKey = ConfigItem("Translate", "YoudaoKey", "")
    GlossaryEnable = ConfigItem("Translate", "GlossaryEnable", False, BoolValidator())

    # 下载工具独家设置
    DownloadStatsTimeSleep = RangeConfigItem("Download", "TimeSleep", 10, RangeValidator(2, 50))


cfg = appConfig()

qconfig.load(basicFunc.getHerePath() + "/config/config.json", cfg)



# 下面是自制设置卡片
def expandCardAddWidget(label, widget):
    w = QWidget()
    layout = QHBoxLayout(w)
    w.setLayout(layout)
    w.setFixedHeight(50)

    widget.setMaximumWidth(200)
    layout.addWidget(label)
    layout.addWidget(widget)
    return w


class ProxySettingCard(ExpandGroupSettingCard):
    def __init__(self):
        super().__init__(icon=FIC.AIRPLANE, title="代理服务设置", content="设置此两项后才能启动代理")
        self.setup()

    def setup(self):
        BodyLabel_ProxyHttp = BodyLabel()
        BodyLabel_ProxyHttp.setText("HTTP代理")
        self.LineEdit_ProxyHttp = LineEdit()
        self.LineEdit_ProxyHttp.setFixedWidth(200)
        self.LineEdit_ProxyHttp.editingFinished.connect(lambda: qconfig.set(cfg.ProxyHttp, self.LineEdit_ProxyHttp.text()))
        self.LineEdit_ProxyHttp.setText(qconfig.get(cfg.ProxyHttp))
        BodyLabel_ProxyHttps = BodyLabel()
        BodyLabel_ProxyHttps.setText("HTTPS代理")
        self.LineEdit_ProxyHttps = LineEdit()
        self.LineEdit_ProxyHttps.setFixedWidth(200)
        self.LineEdit_ProxyHttps.editingFinished.connect(lambda: qconfig.set(cfg.ProxyHttps, self.LineEdit_ProxyHttps.text()))
        self.LineEdit_ProxyHttps.setText(qconfig.get(cfg.ProxyHttps))
        self.addGroupWidget(expandCardAddWidget(BodyLabel_ProxyHttp, self.LineEdit_ProxyHttp))
        self.addGroupWidget(expandCardAddWidget(BodyLabel_ProxyHttps, self.LineEdit_ProxyHttps))

        BodyLabel_Update = BodyLabel()
        BodyLabel_Update.setText("如果您刚刚在别处编辑过代理配置，此处可能没有及时同步配置项的更新，可以手动更新。")
        BodyLabel_Update.setWordWrap(True)
        PushButton_Update = PushButton()
        PushButton_Update.setText("更新")
        PushButton_Update.clicked.connect(self.update)
        self.addGroupWidget(expandCardAddWidget(BodyLabel_Update, PushButton_Update))
        return None

    def update(self):
        self.LineEdit_ProxyHttp.setText(qconfig.get(cfg.ProxyHttp))
        self.LineEdit_ProxyHttps.setText(qconfig.get(cfg.ProxyHttps))
        super().update()
        return None

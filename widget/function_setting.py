from PySide2.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import (ConfigItem, BoolValidator,
                            ColorConfigItem, OptionsConfigItem, OptionsValidator,
                            QConfig, qconfig, RangeConfigItem, RangeValidator, ExpandGroupSettingCard, BodyLabel,
                            LineEdit, PushButton, PasswordLineEdit, ToolTipFilter)
from qfluentwidgets import FluentIcon as FIC

from widget.function import basicFunc, PIC


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


class BaiDuAPISettingCard(ExpandGroupSettingCard):
    def __init__(self, parent):
        super().__init__(icon=PIC.IconBaiDu,
                         title="百度通用文本翻译API",
                         content="设置「百度通用文本翻译」的API参数以调用。",
                         parent=parent)
        BodyLabel_fanyi_baidu_appid = BodyLabel()
        BodyLabel_fanyi_baidu_appid.setText("APP ID")
        BodyLabel_fanyi_baidu_appid.setToolTip("可在百度翻译开放平台获取，需要开通通用文本翻译服务。")
        BodyLabel_fanyi_baidu_appid.installEventFilter(ToolTipFilter(BodyLabel_fanyi_baidu_appid))
        self.LineEdit_fanyi_baidu_appid = LineEdit()
        self.LineEdit_fanyi_baidu_appid.setFixedWidth(200)
        self.LineEdit_fanyi_baidu_appid.editingFinished.connect(
            lambda: qconfig.set(cfg.BaiduAPPID, self.LineEdit_fanyi_baidu_appid.text()))
        self.LineEdit_fanyi_baidu_appid.setText(qconfig.get(cfg.BaiduAPPID))
        self.addGroupWidget(expandCardAddWidget(BodyLabel_fanyi_baidu_appid, self.LineEdit_fanyi_baidu_appid))

        BodyLabel_fanyi_baidu_key = BodyLabel()
        BodyLabel_fanyi_baidu_key.setText("密钥")
        BodyLabel_fanyi_baidu_key.setToolTip(
            "可在百度翻译开放平台获取，请不要随意向他人展示。<br>翻译工具会将您的密钥保存在本地。")
        BodyLabel_fanyi_baidu_key.installEventFilter(ToolTipFilter(BodyLabel_fanyi_baidu_key))
        self.LineEdit_fanyi_baidu_key = PasswordLineEdit()
        self.LineEdit_fanyi_baidu_key.setFixedWidth(200)
        self.LineEdit_fanyi_baidu_key.editingFinished.connect(lambda: qconfig.set(cfg.BaiduKey, self.LineEdit_fanyi_baidu_key.text()))
        self.LineEdit_fanyi_baidu_key.setText(qconfig.get(cfg.BaiduKey))
        self.addGroupWidget(expandCardAddWidget(BodyLabel_fanyi_baidu_key, self.LineEdit_fanyi_baidu_key))

        BodyLabel_Update = BodyLabel()
        BodyLabel_Update.setText("如果您刚刚在别处编辑过此设置，此处可能没有及时同步配置项的更新，可以手动更新。")
        BodyLabel_Update.setWordWrap(True)
        PushButton_Update = PushButton()
        PushButton_Update.setText("更新")
        PushButton_Update.clicked.connect(self.update)
        self.addGroupWidget(expandCardAddWidget(BodyLabel_Update, PushButton_Update))

    def update(self):
        self.LineEdit_fanyi_baidu_appid.setText(qconfig.get(cfg.BaiduAPPID))
        self.LineEdit_fanyi_baidu_key.setText(qconfig.get(cfg.BaiduKey))
        super().update()
        return None


class YouDaoAPISettingCard(ExpandGroupSettingCard):
    def __init__(self, parent):
        super().__init__(icon=PIC.IconYouDao,
                         title="有道文本翻译API",
                         content="设置「有道文本翻译」的API参数以调用。",
                         parent=parent)
        BodyLabel_fanyi_youdao_appKey = BodyLabel()
        BodyLabel_fanyi_youdao_appKey.setText("APP Key")
        BodyLabel_fanyi_youdao_appKey.setToolTip("可在有道智云AI开放平台获取，需要开通文本翻译服务。")
        BodyLabel_fanyi_youdao_appKey.installEventFilter(ToolTipFilter(BodyLabel_fanyi_youdao_appKey))
        self.LineEdit_fanyi_youdao_appKey = LineEdit()
        self.LineEdit_fanyi_youdao_appKey.setFixedWidth(200)
        self.LineEdit_fanyi_youdao_appKey.editingFinished.connect(
            lambda: qconfig.set(cfg.YoudaoAPPKey, self.LineEdit_fanyi_youdao_appKey.text()))
        self.LineEdit_fanyi_youdao_appKey.setText(qconfig.get(cfg.YoudaoAPPKey))
        self.addGroupWidget(expandCardAddWidget(BodyLabel_fanyi_youdao_appKey, self.LineEdit_fanyi_youdao_appKey))

        BodyLabel_fanyi_youdao_key = BodyLabel()
        BodyLabel_fanyi_youdao_key.setText("密钥")
        BodyLabel_fanyi_youdao_key.setToolTip(
            "可在有道智云AI开放平台获取，请不要随意向他人展示。<br>翻译工具会将您的密钥保存在本地。")
        BodyLabel_fanyi_youdao_key.installEventFilter(ToolTipFilter(BodyLabel_fanyi_youdao_key))
        self.LineEdit_fanyi_youdao_key = PasswordLineEdit()
        self.LineEdit_fanyi_youdao_key.setFixedWidth(200)
        self.LineEdit_fanyi_youdao_key.editingFinished.connect(
            lambda: qconfig.set(cfg.YoudaoKey, self.LineEdit_fanyi_youdao_key.text()))
        self.LineEdit_fanyi_youdao_key.setText(qconfig.get(cfg.YoudaoKey))
        self.addGroupWidget(expandCardAddWidget(BodyLabel_fanyi_youdao_key, self.LineEdit_fanyi_youdao_key))

        BodyLabel_Update = BodyLabel()
        BodyLabel_Update.setText("如果您刚刚在别处编辑过此设置，此处可能没有及时同步配置项的更新，可以手动更新。")
        BodyLabel_Update.setWordWrap(True)
        PushButton_Update = PushButton()
        PushButton_Update.setText("更新")
        PushButton_Update.clicked.connect(self.update)
        self.addGroupWidget(expandCardAddWidget(BodyLabel_Update, PushButton_Update))

    def update(self):
        self.LineEdit_fanyi_youdao_appKey.setText(qconfig.get(cfg.YoudaoAPPKey))
        self.LineEdit_fanyi_youdao_key.setText(qconfig.get(cfg.YoudaoKey))
        super().update()
        return None

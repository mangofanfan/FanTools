from qfluentwidgets import (ConfigItem, BoolValidator,
                            ColorConfigItem, OptionsConfigItem, OptionsValidator,
                            QConfig, qconfig, RangeConfigItem, RangeValidator)

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

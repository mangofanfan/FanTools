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
    YiYanAPI = OptionsConfigItem("Appearance", "YiYanAPI", "fan_mirror", OptionsValidator(["official", "fan_mirror"]))

    # 功能设置 Function
    ExitConfirm = ConfigItem("Function", "ExitConfirm", True, BoolValidator())
    ProxyEnable = ConfigItem("Function", "ProxyEnable", False, BoolValidator())
    ProxyHttp = ConfigItem("Function", "ProxyHttp", "http://127.0.0.1:7890")
    ProxyHttps = ConfigItem("Function", "ProxyHttps", "http://127.0.0.1:7890")
    TimeSleep = RangeConfigItem("Function", "TimeSleep", 20, RangeValidator(5, 60))

    # API设置 API
    BaiduAPPID = ConfigItem("API", "BaiduAPPID", "")
    BaiduKey = ConfigItem("API", "BaiduKey", "")
    YoudaoAPPKey = ConfigItem("API", "YoudaoAPPKey", "")
    YoudaoKey = ConfigItem("API", "YoudaoKey", "")

    # 翻译术语表独家设置
    GlossaryEnable = ConfigItem("Translate", "GlossaryEnable", False, BoolValidator())

    # 下载工具独家设置
    DownloadStatsTimeSleep = RangeConfigItem("Download", "TimeSleep", 10, RangeValidator(2, 50))


cfg = appConfig()

qconfig.load(basicFunc.getHerePath() + "/config/config.json", cfg)

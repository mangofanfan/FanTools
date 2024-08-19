from qfluentwidgets import (ConfigItem, ConfigValidator, BoolValidator,
                            ColorConfigItem, ColorValidator,
                            OptionsConfigItem, OptionsValidator,
                            QConfig, qconfig)

try:
    from function import basicFunc
except:
    from widget.function import basicFunc


class appConfig(QConfig):
    # 外观设置 Appearance
    ThemeMode = OptionsConfigItem("Appearance", "ThemeMode", "light",
                                  OptionsValidator(["light", "dark", "auto"]), restart=True)
    ThemeColor = ColorConfigItem("Appearance", "ThemeColor", "#006DCC")
    ChildWindowAcrylicEnable = ConfigItem("Appearance", "ChildWindowAcrylicEnable", False, BoolValidator())

    # 功能设置 Function
    ExitConfirm = ConfigItem("Function", "ExitConfirm", True, BoolValidator())
    ProxyEnable = ConfigItem("Function", "ProxyEnable", False, BoolValidator())
    ProxyHttp = ConfigItem("Function", "ProxyHttp", "http://127.0.0.1:7890")
    ProxyHttps = ConfigItem("Function", "ProxyHttps", "http://127.0.0.1:7890")
    GlossaryEnable = ConfigItem("Function", "GlossaryEnable", False, BoolValidator())

    # API设置 API
    BaiduAPPID = ConfigItem("API", "BaiduAPPID", "")
    BaiduKey = ConfigItem("API", "BaiduKey", "")
    YoudaoAPPKey = ConfigItem("API", "YoudaoAPPKey", "")
    YoudaoKey = ConfigItem("API", "YoudaoKey", "")


cfg = appConfig()

qconfig.load(basicFunc.getHerePath() + "/config/config.json", cfg)
